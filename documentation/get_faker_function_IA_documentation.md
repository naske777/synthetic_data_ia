# get_faker_function_IA.py

Este archivo contiene funciones para generar código Python que crea un objeto JSON con datos realistas utilizando la librería `Faker`. A continuación se describen las funciones principales:

## Funciones

### `extract_code_inside_braces(generated_code)`
Extrae el contenido entre llaves `{}` de un código generado.

- **Parámetros:**
  - `generated_code` (str): Código generado que contiene llaves `{}`.
- **Retorna:**
  - str: Contenido extraído entre las llaves `{}`.
- **Lanza:**
  - `ValueError`: Si no se encuentran llaves en el código generado.

### `generate_python_code_for_json(structure)`
Genera código Python que crea un objeto JSON con datos realistas basado en una estructura dada.

- **Parámetros:**
  - `structure` (str): Estructura en formato JSON para la cual se generará el código Python.
- **Retorna:**
  - str: Código Python generado.
- **Proceso:**
  1. **Preparación del Prompt:**
     - Formatea una pregunta utilizando la plantilla `GET_FAKER_FUNCTION_QUESTION_TEMPLATE`.
     - Prepara los datos para la solicitud HTTP al modelo especificado en `OLLAMA_URL`.

  2. **Solicitud HTTP:**
     - Envía una solicitud POST al modelo con el prompt preparado.
     - Si la solicitud es exitosa, recibe y procesa la respuesta.

  3. **Procesamiento del Código:**
     - Extrae el código Python dentro de las llaves `{}`.
     - Reemplaza 'faker' por 'fake' en el código extraído.
     - Valida que solo se usen funciones permitidas de `Faker` y que no se concatenen con otros métodos.
     - Si una función no está permitida, se reemplaza por `fake.word()`.

  4. **Guardar el Código:**
     - Crea la carpeta `logs` si no existe.
     - Guarda el código generado en un archivo `logs/faker_code.py`.

  5. **Manejo de Errores:**
     - Imprime un mensaje de error y reintenta la generación de datos si ocurre una excepción.

