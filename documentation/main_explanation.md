# Explicación de main.py

El script `main.py` sirve como el punto de entrada para el proyecto. Orquesta todo el proceso de generación de datos sintéticos utilizando la biblioteca Faker y datos generados por la API de Ollama. A continuación se presenta una explicación detallada de su funcionamiento:

## Resumen

El script realiza las siguientes tareas principales:
1. **Entrada del Usuario**: Solicita al usuario que ingrese una estructura JSON.
2. **Selección de Claves**: Permite al usuario seleccionar claves para las cuales se generarán datos.
3. **Generación de Datos**: Genera datos utilizando la API de Ollama y la biblioteca Faker.
4. **Traducción de Datos**: Traduce los datos generados al idioma especificado en el config.
5. **Generación de Código**: Genera código Python para producir los datos sintéticos.
6. **Ejecución**: Ejecuta el código generado para producir los datos finales.

## Pasos Detallados

### 1. Entrada del Usuario

El script comienza solicitando al usuario que ingrese una estructura JSON. Esto se hace utilizando el mensaje `INPUT_UI_PROMPT_JSON` definido en [config.py](config.py).

### 2. Selección de Claves

Una vez proporcionada la entrada JSON, el script permite al usuario seleccionar claves para las cuales se generarán datos. Esto se facilita mediante los mensajes `INPUT_UI_SELECT_KEYS_MESSAGE` y `INPUT_UI_SELECT_RELATIONSHIPS_MESSAGE` de [config.py](config.py).

### 3. Generación de Datos

El script genera datos utilizando dos fuentes principales:
- **API de Ollama**: Genera datos basados en el contexto y formato proporcionados. La URL de la API y otras configuraciones están definidas en [config.py](config.py).
- **Biblioteca Faker**: Genera datos sintéticos realistas para las claves seleccionadas utilizando las funciones permitidas listadas en [config.py](config.py).

### 4. Traducción de Datos

Los datos generados se traducen  utilizando la biblioteca Googletrans. Esto asegura que los datos estén disponibles en el idioma deseado.

### 5. Generación de Código

El script genera código Python para producir los datos sintéticos. Este código se basa en plantillas y configuraciones definidas en [config.py](config.py). El código generado se escribe sobreescribiendo `code.txt` y guardandolo en el archivo `code_to_execute.py`.

### 6. Ejecución

Finalmente, el script ejecuta el código generado ejecutando `code_to_execute.py`. Esto produce los datos sintéticos finales, que se guardan en archivos JSON en el directorio `output`.

## Configuración

El comportamiento de `main.py` está controlado por varias configuraciones definidas en [config.py](config.py). Las configuraciones clave incluyen:
- `OLLAMA_URL`: URL para la API de Ollama.
- `BATCH_SIZE`: Número de elementos a generar por lote.
- `MAX_NO_PROGRESS_ITERATIONS`: Máximo de iteraciones sin progreso antes de detenerse.
- `NUM_TASKS`: Número de tareas paralelas para la generación de datos.
- `FAKER_ALLOWED_FUNCTIONS`: Lista de funciones permitidas de Faker.

## Conclusión

El script `main.py` es una herramienta integral para generar datos sintéticos. Aprovecha la API de Ollama y la biblioteca Faker para producir datos realistas, los traduce y ejecuta el código generado para producir el resultado final.

