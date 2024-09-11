# generate_data_IA.py

Este archivo contiene funciones asincrónicas para generar datos basados en un formato específico y guardar los resultados en archivos JSON. A continuación se describen las funciones principales:

## Funciones

### `print_elapsed_time(start_time)`
Función asincrónica para imprimir el tiempo transcurrido cada 10 segundos.

- **Parámetros:**
  - `start_time` (float): Tiempo de inicio en segundos.
- **Retorna:**
  - None

### `generate_elements(format_string, num_elements)`
Función asincrónica para generar elementos basados en una cadena de formato y un número de elementos.

- **Parámetros:**
  - `format_string` (str): Cadena de formato en JSON.
  - `num_elements` (int): Número de elementos a generar.
- **Retorna:**
  - list: Lista de datos generados y limpiados.

#### Detalles del Proceso:
1. **Preparación del Prompt:**
   - Convierte la cadena de formato JSON en un diccionario.
   - Extrae las claves y valores del diccionario.
   - Prepara el prompt para la generación de datos.

2. **Solicitud HTTP:**
   - Envía una solicitud POST al modelo especificado en `OLLAMA_URL` con el prompt preparado.
   - Si la solicitud es exitosa, recibe y procesa la respuesta.

3. **Procesamiento de Datos:**
   - Divide los datos recibidos en elementos individuales.
   - Limpia y estructura los datos basados en el formato especificado.
   - Guarda los datos sin formato y los datos limpiados en archivos JSON en la carpeta `logs`.

4. **Manejo de Errores:**
   - Imprime un mensaje de error si la solicitud HTTP falla.

