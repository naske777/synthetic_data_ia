#{"name": "animal name","description": "animal description","id": "id","country": "country name"}

OLLAMA_URL = 'http://192.168.1.24:11434/api/generate'

LENGUAGE = 'es' # Si es 'en' se mantendran lo resultados generados por ollama en ingles
# Configuración de generación de elementos
# Tamaño del lote para la generación de datos. 
# Modificar este valor afectará cuántos elementos se generan en cada lote.
BATCH_SIZE = 100

# Número máximo de iteraciones sin progreso antes de detener la generación de datos.
# Modificar este valor afectará cuántas iteraciones se permiten sin progreso antes de detenerse.
MAX_NO_PROGRESS_ITERATIONS = 6

# Número de tareas paralelas para la generación de datos.
# Modificar este valor afectará cuántas tareas se ejecutan en paralelo.
NUM_TASKS = 2

# Configuración del modelo y generación de prompts

# Nombre del modelo a utilizar para la generación de datos.
MODEL_NAME = 'llama3.1'

GENERATE_DATA_ROLE = ("You are a highly specialized data miner. Your job is to generate information strictly from the provided context. "
                      "You are a wizard that returns lists of data in the specified format. "
                      "Ensure that each entry follows the format exactly as specified. "
                      "Avoid generating a single element or elements that are not correctly defined. "
                      "All elements must be properly formatted as specified.")

GENERATE_DATA_QUESTION_TEMPLATE = ("Generate {num_elements} elements in the following format: {format_prompt};{format_prompt};... "
                                   "For single attributes, separate each entry with a semicolon (;). "
                                   "For related data, format each entry as 'key1, key2, ..., keyN;' "
                                   "The response must be exclusively in the specified format without any additional text.")

# Opciones para la generación de datos.
GENERATE_DATA_OPTIONS = {
    "num_predict": 200,  # Número de predicciones a generar.
    "temperature": 0.5,  # Temperatura para la generación de datos.
    "penalize_newline": True,  # Penalización por nuevas líneas.
}

# Configuración para get_faker_function_IA.py

# Lista de funciones permitidas de la biblioteca 'faker'.
# Modificar esta lista cambiará las funciones de 'faker' que se pueden utilizar.
FAKER_ALLOWED_FUNCTIONS = [
    'user_name', 'password', 'name', 'address', 'email', 'phone_number', 
    'job', 'company', 'date', 'time', 'url', 'ipv4', 'sentence', 'word'
]

# Rol del modelo para la generación de código Python utilizando 'faker'.
GET_FAKER_FUNCTIO_ROLE = """
You are an advanced AI model capable of generating Python code. Your task is to create a Python script that uses the 'faker' library and 'random' module to generate a JSON object. Each element should have the following structure:
{{
    "key1": "random function or faker function (fake.function())",
    "key2": "random function or faker function" (fake.function()),
    "key3": "random function or faker function" (fake.function()),
    ...
}}
Do not chain multiple faker functions like fake.function1().function2().
Use only one faker function per key, for example: fake.name(), fake.address(), etc.
Ensure the generated code only includes the JSON structure without imports, comments, or any other code.
You can only use the following faker functions:
- {allowed_functions}

If a function is not in the provided list, use 'word' or 'sentence' instead.
Additionally, ensure that IDs are generated as random integers up to 1,000,000.
""".format(allowed_functions=', '.join(FAKER_ALLOWED_FUNCTIONS))

# Plantilla de preguntas para la generación de código Python utilizando 'faker'.
GET_FAKER_FUNCTION_QUESTION_TEMPLATE = "Generate Python code to create a JSON object with the following structure: {structure} using  data generated by 'faker' and 'random'. Only provide the dictionary content without any comments."

# Opciones para la generación de código Python utilizando 'faker'.
GET_FAKER_FUNCTION__MODEL_OPTIONS = {
    "temperature": 0.2, 
}

# Configuración para input_ui.py

INPUT_UI_PROMPT_JSON = "Por favor, introduzca el json a extender"

INPUT_UI_NO_INPUT_PROVIDED = "No se proporcionó entrada"

INPUT_UI_INVALID_JSON = "Entrada JSON inválida: {error}"

INPUT_UI_SELECT_KEYS_MESSAGE = "Selecciona las claves que desee generar con IA, si no hay ninguna presione Entrer para continuar"

INPUT_UI_EDIT_VALUE_PROMPT = "Valor actual para '{key}': {current_value}\nIngresa un nuevo valor:"

INPUT_UI_SELECT_RELATIONSHIPS_MESSAGE = "Selecciona las claves relacionadas, si no hay ninguna presione Entrer para continuar"