import json
import sys
import inquirer
import tkinter as tk
from tkinter import simpledialog
from config import (
    INPUT_UI_PROMPT_JSON, INPUT_UI_NO_INPUT_PROVIDED, INPUT_UI_INVALID_JSON,
    INPUT_UI_SELECT_KEYS_MESSAGE, INPUT_UI_EDIT_VALUE_PROMPT, INPUT_UI_SELECT_RELATIONSHIPS_MESSAGE
)

# Función para leer JSON desde una interfaz gráfica
def read_json_from_gui():
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal
    input_data = simpledialog.askstring("Entrada", INPUT_UI_PROMPT_JSON)
    if not input_data:
        print(INPUT_UI_NO_INPUT_PROVIDED)
        sys.exit(1)
    try:
        json_data = json.loads(input_data)
        if not isinstance(json_data, dict):
            raise ValueError("La entrada JSON debe ser un objeto")
        return json_data
    except (json.JSONDecodeError, ValueError) as e:
        print(INPUT_UI_INVALID_JSON.format(error=e))
        sys.exit(1)

# Función para seleccionar claves del JSON
def select_keys(json_data):
    keys = list(json_data.keys())
    questions = [
        inquirer.Checkbox(
            'selected_keys',
            message=INPUT_UI_SELECT_KEYS_MESSAGE,
            choices=keys,
        ),
    ]
    answers = inquirer.prompt(questions)
    return answers['selected_keys']

# Función para editar valores de las claves seleccionadas
def edit_values(json_data, selected_keys):
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal
    edited_values = {}
    for key in selected_keys:
        current_value = json_data[key]
        new_value = simpledialog.askstring("Editar Valor", INPUT_UI_EDIT_VALUE_PROMPT.format(key=key, current_value=current_value), initialvalue=current_value)
        if new_value is not None:
            edited_values[key] = new_value
        else:
            edited_values[key] = current_value
    return edited_values

# Selecciona y edita claves en los datos JSON.
async def select_and_edit_keys(json_data):
    selected_keys = select_keys(json_data)
    if not selected_keys:
        return None, None
    edited_values = edit_values(json_data, selected_keys)
    related_keys = select_and_define_relationships(selected_keys)
    return edited_values, related_keys

# Función para seleccionar y definir relaciones entre claves
def select_and_define_relationships(selected_keys):
    relationships = []
    while True:
        questions = [
            inquirer.Checkbox(
                'final_selected_keys',
                message=INPUT_UI_SELECT_RELATIONSHIPS_MESSAGE,
                choices=selected_keys,
            ),
        ]
        answers = inquirer.prompt(questions)
        final_selected_keys = answers['final_selected_keys']
        
        # Si hay menos de dos claves seleccionadas, salir del bucle
        if len(final_selected_keys) < 2:
            break
        
        # Agregar las claves relacionadas a la lista de relaciones
        relationships.append(final_selected_keys)
        # Eliminar las claves seleccionadas de la lista de claves disponibles
        selected_keys = [key for key in selected_keys if key not in final_selected_keys]
        
        # Si hay menos de dos claves disponibles, salir del bucle
        if len(selected_keys) < 2:
            break
    
    return {
        "relationships": relationships,
        "unrelated_keys": selected_keys
    }