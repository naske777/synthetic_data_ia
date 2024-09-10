import json
import asyncio
import os
from tqdm import tqdm
from googletrans import Translator
from lib.generate_data_IA import generate_elements
from lib.input_ui import select_keys, edit_values, select_and_define_relationships
from config import BATCH_SIZE, MAX_NO_PROGRESS_ITERATIONS, NUM_TASKS  # Importar configuraciones
from lib.database_handler import  get_data_from_table, insert_data_for_table  # Importar función para leer datos de la base de datos
import re

# Convertir loss values de un json al nombre  de una tabla
def convert_values_to_table_name(values):
    """Convierte los valores de un diccionario a un nombre de tabla."""
    # Extraer los valores del diccionario
    valores = list(values.values())
    
    # Convertir los valores a una cadena separada por guiones bajos
    table_name = '_'.join(map(str, valores))
    
    # Reemplazar caracteres no permitidos (por ejemplo, espacios y caracteres especiales)
    table_name = re.sub(r'\W+', '_', table_name)
    
    return table_name

# Función asincrónica para seleccionar y editar claves en los datos JSON
async def select_and_edit_keys(json_data):
    selected_keys = select_keys(json_data)  # Seleccionar claves del JSON
    
    if not selected_keys:
        return None, None
    
    edited_values = edit_values(json_data, selected_keys)  # Editar valores de las claves seleccionadas
    related_keys = select_and_define_relationships(selected_keys)  # Definir relaciones entre claves
    return edited_values, related_keys

# Función para traducir los valores editados
def translate_values(edited_values, related_keys):
    all_keys = related_keys['relationships'] + [[key] for key in related_keys['unrelated_keys']]
    translated_values = {}
    translator = Translator()

    # Traducir los valores de las claves relacionadas
    for relationship in all_keys:
        values = {key: edited_values[key] for key in relationship}
        translated_values[tuple(relationship)] = {key: translator.translate(value, src='es', dest='en').text for key, value in values.items()}
    
    return translated_values

# Función para solicitar al usuario el número de elementos a generar para cada relación
def request_num_elements(translated_values):
    num_elements_dict = {}
    for relationship in translated_values.keys():
        num_elements = int(input(f"Escriba el numero de elementos a generar para {relationship}: "))
        num_elements_dict[relationship] = num_elements
    return num_elements_dict

# Función asincrónica para generar elementos para las claves traducidas
async def generate_elements_for_keys(translated_values, num_elements_dict):
    all_results = {}

    for relationship, values in translated_values.items():
        format_string = json.dumps([{key: values[key] for key in relationship}])
        table_name = convert_values_to_table_name(values)
        results = []
        unique_elements = set()
        no_progress_iterations = 0
        previous_length = 0
        num_elements = num_elements_dict[relationship]

        # Consultar la base de datos para obtener datos existentes
        existing_data = get_data_from_table(table_name)
        print(f"Existing data for {relationship}: {len(existing_data)}")
        
        # Analizar la cadena de formato para extraer valores
        format_string_keys = list(json.loads(format_string)[0].keys())
    
        for data in existing_data:
            if (list(data.keys()) == format_string_keys):
                results.append(data)
                unique_elements.add(tuple(data.items()))
                if len(results) >= num_elements:
                    break

        # Mostrar barra de progreso durante la generación de elementos
        with tqdm(total=num_elements, desc=f"Generating {relationship}") as pbar:
            print(f"Initial results length: {len(results)}")
            previous_length = len(results)
            pbar.update(previous_length)  # Actualizar la barra de progreso con los datos existentes
            while len(results) < num_elements:
                tasks = [generate_elements(format_string, BATCH_SIZE) for _ in range(NUM_TASKS)]
                
                for future in asyncio.as_completed(tasks):
                    generated_elements = await future
                    
                    if isinstance(generated_elements, list):
                        for element in generated_elements:
                            if isinstance(element, dict):
                                element_tuple = tuple(element.items())
                                if element_tuple not in unique_elements:
                                    unique_elements.add(element_tuple)
                                    results.append(element)
                                    pbar.update(1)
                                    if len(results) >= num_elements:
                                        break
                            else:
                                print(f"Discarding invalid element: {element}")
                    
                    if len(results) == previous_length:
                        no_progress_iterations += 1
                    else:
                        no_progress_iterations = 0
                        previous_length = len(results)
                    
                    if no_progress_iterations >= MAX_NO_PROGRESS_ITERATIONS:
                        print(f"No progress after {MAX_NO_PROGRESS_ITERATIONS} iterations for keys '{relationship}'. Stopping early.")
                        break
                
                if no_progress_iterations >= MAX_NO_PROGRESS_ITERATIONS:
                    break
        
        all_results[relationship] = results
        print(f"Generated {len(results)} elements for keys '{relationship}'")
        
        # Insertar los nuevos datos generados en la base de datos
        new_data = []
        for result in results:
           element_tuple = tuple(result.items())
           if result not in existing_data:
              new_data.append(result)
        
        print(f"New data to insert for {values}: {new_data}")
        insert_data_for_table(new_data, table_name)
    
    return all_results# Función para guardar los resultados generados en un archivo JSON
def save_results(translated_results):
    # Crear la carpeta 'logs' si no existe
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Guardar los datos en un archivo JSON en la carpeta 'logs'
    with open('logs/generated_data.json', 'w', encoding='utf-8') as json_file:
        json.dump({str(k): v for k, v in translated_results.items()}, json_file, ensure_ascii=False, indent=4)
    print("Data saved in logs/generated_data.json")