# Documentación de database_handler.py

## Descripción general
Este módulo proporciona funciones para manejar una base de datos SQLite, incluyendo la creación de conexiones, tablas, inserción de datos y recuperación de datos. Utiliza la biblioteca `sqlite3` para interactuar con la base de datos y `os` para manejar el sistema de archivos.

## Funciones

### `create_connection()`
Crea una conexión a la base de datos SQLite especificada en `DB_PATH`.

- **Retorna**:
  - `sqlite3.Connection`: Un objeto de conexión a la base de datos.
- **Excepciones**:
  - Imprime un mensaje de error si ocurre una excepción durante la conexión.

### `create_table(table_name, keys)`
Crea una tabla con el nombre y las claves especificadas como columnas si no existe.

- **Parámetros**:
  - `table_name` (`str`): El nombre de la tabla a crear.
  - `keys` (`list`): Una lista de claves que se utilizarán como columnas en la tabla.
- **Retorna**:
  - `None`
- **Excepciones**:
  - Imprime un mensaje de error si ocurre una excepción durante la creación de la tabla.

### `insert_data_for_table(data, table_name)`
Inserta datos en la tabla especificada con claves como columnas.

- **Parámetros**:
  - `data` (`list`): Una lista de diccionarios que contienen los datos a insertar.
  - `table_name` (`str`): El nombre de la tabla en la que se insertarán los datos.
- **Retorna**:
  - `None`
- **Excepciones**:
  - Imprime un mensaje de error si ocurre una excepción durante la inserción de datos.

### `get_data_from_table(table_name)`
Recupera todos los datos de la tabla especificada y los retorna, excluyendo la columna ID.

- **Parámetros**:
  - `table_name` (`str`): El nombre de la tabla de la cual se recuperarán los datos.
- **Retorna**:
  - `list`: Una lista de diccionarios que contienen los datos recuperados.
- **Excepciones**:
  - Imprime un mensaje de error si ocurre una excepción durante la recuperación de datos.

