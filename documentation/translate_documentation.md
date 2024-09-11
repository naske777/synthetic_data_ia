# Documentación de translate.py

## Descripción general
Este módulo proporciona funciones para traducir cadenas de texto dentro de estructuras de datos anidadas utilizando la biblioteca `googletrans`. Utiliza `ThreadPoolExecutor` para realizar traducciones concurrentes y `tqdm` para mostrar una barra de progreso.

## Funciones

### `translate_text(text, src='es', dest='en')`
Traduce una sola cadena de texto de un idioma a otro.

- **Parámetros**:
  - `text` (`str`): La cadena de texto a traducir.
  - `src` (`str`, opcional): El código del idioma de origen (por defecto es 'es').
  - `dest` (`str`, opcional): El código del idioma de destino (por defecto es 'en').
- **Retorna**:
  - `str`: La cadena de texto traducida.
- **Excepciones**:
  - Imprime un mensaje de error y retorna el texto original si ocurre una excepción durante la traducción.

### `count_strings(data)`
Cuenta el número de cadenas de texto en una estructura de datos anidada.

- **Parámetros**:
  - `data` (`dict` | `list` | `str`): La estructura de datos que contiene las cadenas de texto.
- **Retorna**:
  - `int`: El número total de cadenas de texto en la estructura de datos.

### `translate(data, src='en', dest='es')`
Traduce todas las cadenas de texto en una estructura de datos anidada de un idioma a otro.

- **Parámetros**:
  - `data` (`dict` | `list`): La estructura de datos que contiene las cadenas de texto a traducir.
  - `src` (`str`, opcional): El código del idioma de origen (por defecto es 'en').
  - `dest` (`str`, opcional): El código del idioma de destino (por defecto es 'es').
- **Retorna**:
  - `dict` | `list`: La estructura de datos con las cadenas de texto traducidas.

