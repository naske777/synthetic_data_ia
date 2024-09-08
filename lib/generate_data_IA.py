import aiohttp
import asyncio
import json
import re
import time
import os
from config import (MODEL_NAME, GENERATE_DATA_ROLE, 
                    GENERATE_DATA_QUESTION_TEMPLATE, GENERATE_DATA_OPTIONS)  # Importar configuraciones

# Función asincrónica para imprimir el tiempo transcurrido cada 10 segundos
async def print_elapsed_time(start_time):
    while True:
        await asyncio.sleep(10)
        elapsed_time = time.time() - start_time
        print(f"Elapsed time: {elapsed_time:.2f} seconds")

# Función asincrónica para generar elementos basados en una cadena de formato y un número de elementos
async def generate_elements(format_string, num_elements):
    print(format_string)
    format_string = json.loads(format_string)
    # Analizar la cadena de formato para extraer valores
    keys = list(format_string[0].keys())
    values = list(format_string[0].values())
    keysCount = len(keys)
    
    # Convertir la cadena de formato al formato esperado para el prompt
    format_prompt = ', '.join(values)
    
    question = GENERATE_DATA_QUESTION_TEMPLATE.format(num_elements=num_elements, format_prompt=format_prompt)
    
    prompt = f"Question: {question}"
    
    data = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "system": GENERATE_DATA_ROLE,
        "stream": False,
        "options": GENERATE_DATA_OPTIONS  # Usar el objeto OPTIONS completo
    }
    
    url = 'http://192.168.1.24:11434/api/generate'
    
    start_time = time.time()
    async with aiohttp.ClientSession() as session:
        elapsed_time_task = asyncio.create_task(print_elapsed_time(start_time))
        async with session.post(url, json=data) as response:
            elapsed_time_task.cancel()
            
            if response.status == 200:
                data_response = await response.json()
                data = data_response.get('response')
                if not data:
                    print("Error: No response data received.")
                    return []
                
                # Crear la carpeta 'logs' si no existe
                if not os.path.exists('logs'):
                    os.makedirs('logs')
                
                # Guardar los datos en un archivo JSON en la carpeta 'logs'
                with open('logs/data_response_unformatted.json', 'w', encoding='utf-8') as json_file:
                    json.dump(data, json_file, ensure_ascii=False, indent=4)
                
                # Extraer datos basados en el nuevo formato
                if ',' in format_prompt:
                    # Formato de datos relacionados
                    items = data.split(';')
                    cleaned_data = []
                    for item in items:
                        if item.strip():
                            parts = item.split(',')
                            if len(parts) == keysCount:
                                cleaned_data.append({keys[i]: parts[i].strip() for i in range(keysCount)})
                else:
                    # Formato de atributo único
                    items = data.split(';')
                    cleaned_data = [{keys[0]: item.strip()} for item in items if item.strip()]

                # Guardar los datos limpiados en un archivo JSON en la carpeta 'logs'
                with open('logs/data_response_Json.json', 'w', encoding='utf-8') as json_file:
                    json.dump(cleaned_data, json_file, ensure_ascii=False, indent=4)
                
                return cleaned_data
            else:
                print(f"Request failed with status code: {response.status}")
                return "Error"

if __name__ == "__main__":
    # Ejemplo de uso
    format_string = '[{"name": "animal name","description": "animal description"}]'
    num_elements = 30
    asyncio.run(generate_elements(format_string, num_elements))