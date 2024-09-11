import os
import subprocess
import json
import copy
from lib.get_faker_function_IA import generate_python_code_for_json

# Función para leer datos generados desde un archivo JSON
def read_generated_data(file_path='../generated_data.json'):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Función para comparar y eliminar claves de la estructura original
def get_variables_and_faker_structure(structure, translated_results):
    keys_to_remove = {}
    variables_to_add = {}
    
    for index, key in enumerate(structure.keys()):
        for gen_key in translated_results.keys():
            if isinstance(gen_key, tuple) and key in gen_key:
                keys_to_remove[key] = index
                variables_to_add[key] = translated_results[gen_key]

    # Hacer una copia de la estructura original
    faker_structure = copy.deepcopy(structure)
    
    #Eliminar las keys generadas con ia
    for key in keys_to_remove.keys():
        del faker_structure[key]

    return variables_to_add, faker_structure

# Función para modificar el código generado
def modify_generated_code(faker_function, structure, variables_to_add):

    for key in structure.keys():
        if key in variables_to_add:
            random_selection_function = f'"{key}": {key}[index % len({key})]["{key}"]'
            faker_function = faker_function.rstrip('}') + f', {random_selection_function}' + '}'
    return faker_function

# Función para modificar el contenido de code.txt con el código generado
def modify_code_txt_with_generated_code(code, variables_to_add):
    with open('lib/code.txt', 'r', encoding='utf-8') as file:
        code_txt_content = file.read()

    for key, values in variables_to_add.items():
        variable_declaration = f"{key} = {values}\n"
        code_txt_content = code_txt_content.replace('fake = Faker()\n', f'fake = Faker()\n{variable_declaration}')

    modified_code_txt_content = code_txt_content.replace('return {}', f'return {code}')

    # Crear la carpeta 'logs' si no existe
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Guardar el código modificado en un archivo dentro de la carpeta 'logs'
    with open('logs/code_to_execute.py', 'w', encoding='utf-8') as file:
        file.write(modified_code_txt_content)

# Función para ejecutar el código modificado
def execute_modified_code():
    result = subprocess.run(['python', 'logs/code_to_execute.py'], text=True)
    if result.returncode == 0:
        print("Code executed successfully.")
    else:
        print(f"Error executing code: {result.stderr}")

