import os
import re
import requests
import json
from faker import Faker
from config import (
    MODEL_NAME, GET_FAKER_FUNCTIO_ROLE, GET_FAKER_FUNCTION_QUESTION_TEMPLATE, GET_FAKER_FUNCTION__MODEL_OPTIONS, FAKER_ALLOWED_FUNCTIONS, OLLAMA_URL
)

fake = Faker()

# Función para extraer el contenido entre llaves {}
def extract_code_inside_braces(generated_code):
    # Extraer el contenido entre las llaves {}
    match = re.search(r'\{(.*)\}', generated_code, re.DOTALL)
    if match:
        return '{' + match.group(1) + '}'
    else:
        print("Faker code: ", generated_code)
        raise ValueError("No se encontraron llaves en el código generado")
    
# Función para generar código Python que crea un objeto JSON con datos realistas
def generate_python_code_for_json(structure):
    question = GET_FAKER_FUNCTION_QUESTION_TEMPLATE.format(structure=structure)
    
    prompt = f"Question: {question}"
    data = {
        "model": MODEL_NAME,
        "prompt": prompt ,
        "system": GET_FAKER_FUNCTIO_ROLE,
        "stream": False,
        "options": GET_FAKER_FUNCTION__MODEL_OPTIONS
    }
    print("Generando funciones de faker...")
    while True:
        try:
            response = requests.post(OLLAMA_URL, headers={}, data=json.dumps(data))
            
            if response.status_code != 200:
                print(f"Request failed with status code: {response.status_code}")
                print("Reintentando generar los datos...")
                continue
            
            data_response = response.json()
            
            # Obtener el código Python de la respuesta
            python_code = data_response.get('response')
            
            # Extraer el código dentro de las llaves
            python_code = extract_code_inside_braces(python_code)
            
            # Reemplazar 'faker' por 'fake' en el código extraído
            python_code = python_code.replace('faker', 'fake').replace('Faker', 'fake')
        
            # Validar que solo se usen funciones permitidas y no se concatenen con otros métodos
            lines = python_code.split('\n')
            for i, line in enumerate(lines):
                matches = re.findall(r'fake\.(\w+)\(\)', line)
                for match in matches:
                    if match not in FAKER_ALLOWED_FUNCTIONS:
                        lines[i] = re.sub(r'fake\.\w+\(\)', 'fake.word()', line)
                    else:
                        # Asegurarse de que no haya concatenaciones como .name()
                        lines[i] = re.sub(rf'fake\.{match}\(\)\.\w+', f'fake.{match}()', line)
            
            python_code = '\n'.join(lines)        
            
            # Crear la carpeta 'logs' si no existe
            if not os.path.exists('logs'):
                os.makedirs('logs')
            
            # Guardar el código generado en un archivo dentro de la carpeta 'logs'
            with open('logs/faker_code.py', 'w', encoding='utf-8') as python_file:
                python_file.write(python_code)
        
            return python_code
        
        except Exception as e:
            print(f"Error: {e}")
            print("Reintentando generar los datos...")

