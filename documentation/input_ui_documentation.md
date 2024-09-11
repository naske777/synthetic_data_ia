# Documentación de input_ui.py

## Descripción general
Este módulo proporciona un conjunto de funciones para interactuar con datos JSON a través de una interfaz gráfica de usuario (GUI) y mensajes en la línea de comandos. Permite a los usuarios leer datos JSON, seleccionar y editar claves, y definir relaciones entre claves.

## Funciones

### `read_json_from_gui()`
Lee datos JSON desde un cuadro de diálogo de entrada GUI.

- **Retorna**: 
  - `dict`: Los datos JSON analizados.
- **Excepciones**:
  - Sale del programa si no se proporciona entrada o si la entrada no es JSON válido.

### `select_keys(json_data)`
Solicita al usuario que seleccione claves de los datos JSON proporcionados.

- **Parámetros**:
  - `json_data` (`dict`): Los datos JSON de los cuales se seleccionarán las claves.
- **Retorna**:
  - `list`: Una lista de claves seleccionadas.

### `edit_values(json_data, selected_keys)`
Solicita al usuario que edite los valores de las claves seleccionadas.

- **Parámetros**:
  - `json_data` (`dict`): Los datos JSON que contienen las claves y valores.
  - `selected_keys` (`list`): Las claves cuyos valores se van a editar.
- **Retorna**:
  - `dict`: Un diccionario de valores editados.

### `select_and_edit_keys(json_data)`
Selecciona y edita claves en los datos JSON de manera asincrónica.

- **Parámetros**:
  - `json_data` (`dict`): Los datos JSON a procesar.
- **Retorna**:
  - `tuple`: Una tupla que contiene los valores editados y las claves relacionadas.

### `select_and_define_relationships(selected_keys)`
Solicita al usuario que defina relaciones entre las claves seleccionadas.

- **Parámetros**:
  - `selected_keys` (`list`): Las claves de las cuales se definirán las relaciones.
- **Retorna**:
  - `dict`: Un diccionario que contiene las relaciones y las claves no relacionadas.