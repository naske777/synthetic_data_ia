import asyncio
from lib.get_faker_function_IA import generate_python_code_for_json
from lib.input_ui import read_json_from_gui, select_and_edit_keys
from lib.data_IA_handler import translate_values, request_num_elements, generate_elements_for_keys, save_results
from lib.translate import translate
from lib.generate_code import filter_and_extract_keys, execute_modified_code, modify_code_txt_with_generated_code, modify_generated_code

async def main():
    # Leer el JSON desde la interfaz gráfica
    structure = read_json_from_gui()
    
    faker_structure = structure
    variables_to_add = {}

    # Seleccionar y editar claves del JSON
    edited_values, related_structure = await select_and_edit_keys(structure)
    
    if edited_values:
        # Traducir los valores editados
        related_structure = translate_values(edited_values, related_structure)

        # Solicitar al usuario el número de elementos a generar para cada relación
        num_elements_dict = request_num_elements(related_structure)

        # Generar elementos para las claves traducidas
        all_results = await generate_elements_for_keys(related_structure, num_elements_dict)

        # Traducir los resultados generados del inglés al español
        translated_results = translate(all_results, src='en', dest='es')

        # Guardar los resultados traducidos en un archivo
        save_results(translated_results)
  
        # Comparar y eliminar claves del JSON original con los resultados traducidos
        variables_to_add, faker_structure = filter_and_extract_keys(structure, translated_results)
  
    # Generar código Python a partir del JSON modificado
    faker_function = generate_python_code_for_json(faker_structure)
  
    # Modificar el código generado para incluir la función de selección aleatoria
    complete_code = modify_generated_code(faker_function, structure, variables_to_add)
  
    # Modificar el archivo code.txt con el código generado y las variables añadidas
    modify_code_txt_with_generated_code(complete_code, variables_to_add)
    
    # Ejecutar el código modificado
    execute_modified_code()
    
if __name__ == "__main__":
    # Ejecutar la función principal de manera asíncrona
    asyncio.run(main())