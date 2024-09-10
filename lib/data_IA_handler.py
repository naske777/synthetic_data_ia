import json
import asyncio
import os
from tqdm import tqdm
from googletrans import Translator
from lib.generate_data_IA import generate_elements
from lib.input_ui import select_keys, edit_values, select_and_define_relationships
from config import BATCH_SIZE, MAX_NO_PROGRESS_ITERATIONS, NUM_TASKS
from lib.database_handler import get_data_from_table, insert_data_for_table
import re

# Convierte los valores de un diccionario a un nombre de tabla.
def convert_values_to_table_name(values):
    valores = list(values.values())
    table_name = '_'.join(map(str, valores))
    table_name = re.sub(r'\W+', '_', table_name)
    return table_name

# Traduce los valores editados.
def translate_values(edited_values, related_keys):
    all_keys = related_keys['relationships'] + [[key] for key in related_keys['unrelated_keys']]
    translated_values = {}
    translator = Translator()
    for relationship in all_keys:
        values = {key: edited_values[key] for key in relationship}
        translated_values[tuple(relationship)] = {key: translator.translate(value, src='es', dest='en').text for key, value in values.items()}
    return translated_values

# Solicita al usuario el número de elementos a generar para cada relación.
def request_num_elements(translated_values):
    num_elements_dict = {}
    for relationship in translated_values.keys():
        num_elements = int(input(f"Escriba el numero de elementos a generar para {relationship}: "))
        num_elements_dict[relationship] = num_elements
    return num_elements_dict

# Consultar la base de datos para obtener datos existentes
def fetch_existing_data(table_name, format_string, num_elements):
    existing_data = get_data_from_table(table_name)
    print(f"Existing data: {len(existing_data)}")
    
# Analizar la cadena de formato para extraer valores
    format_string_keys = list(json.loads(format_string)[0].keys())
    results = set()
    
    for data in existing_data:
        if list(data.keys()) == format_string_keys:
            results.add(tuple(data.items()))
            if len(results) >= num_elements:
                break
    
    return results, existing_data

# Insertar los nuevos datos generados en la base de datos
def insert_new_data(results, existing_data, table_name, values):
    new_data = [dict(result) for result in results if dict(result) not in existing_data]
    print(f"New data to insert for {values}: {new_data}")
    insert_data_for_table(new_data, table_name)

# Mostrar barra de progreso durante la generación de elementos
async def generate_elements_with_progress(format_string, num_elements, results):
    no_progress_iterations = 0
    previous_length = len(results)
    
    with tqdm(total=num_elements, desc=f"Generating elements") as pbar:
        print(f"Initial results length: {len(results)}")
        pbar.update(previous_length)  # Actualizar la barra de progreso con los datos existentes
        
        while len(results) < num_elements:
            tasks = [generate_elements(format_string, BATCH_SIZE) for _ in range(NUM_TASKS)]
            
            for future in asyncio.as_completed(tasks):
                generated_elements = await future
                
                if isinstance(generated_elements, list):
                    for element in generated_elements:
                        if isinstance(element, dict):
                            element_tuple = tuple(element.items())


                            if element_tuple not in results:
                                results.add(element_tuple)
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
                    print(f"No progress after {MAX_NO_PROGRESS_ITERATIONS} iterations. Stopping early.")
                    break
            
            if no_progress_iterations >= MAX_NO_PROGRESS_ITERATIONS:
                break
    
    return results

# Genera elementos para las claves
async def generate_elements_for_keys(translated_values, num_elements_dict):
    all_results = {}

    for relationship, values in translated_values.items():
        format_string = json.dumps([{key: values[key] for key in relationship}])
        table_name = convert_values_to_table_name(values)
        num_elements = num_elements_dict[relationship]

        # Obtener datos existentes y resultados iniciales
        results, existing_data = fetch_existing_data(table_name, format_string, num_elements)

        # Generar nuevos elementos
        results = await generate_elements_with_progress(format_string, num_elements, results)
        
        all_results[relationship] = [dict(element) for element in results]
        print(f"Generated {len(results)} elements for keys '{relationship}'")
        
        # Insertar los nuevos datos generados en la base de datos
        insert_new_data(results, existing_data, table_name, values)
    
    return all_results

# Guarda los resultados generados en un archivo JSON.
def save_results(translated_results):
    if not os.path.exists('logs'):
        os.makedirs('logs')
    with open('logs/generated_data.json', 'w', encoding='utf-8') as json_file:
        json.dump({str(k): v for k, v in translated_results.items()}, json_file, ensure_ascii=False, indent=4)
    print("Data saved in logs/generated_data.json")