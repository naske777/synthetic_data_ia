import json
from googletrans import Translator
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# Función para traducir una sola cadena de texto
def translate_text(text, src='es', dest='en'):
    translator = Translator()
    try:
        translated = translator.translate(text, src=src, dest=dest).text
        return translated
    except Exception as e:
        print(f"Error translating {text}: {e}")
        return text

# Función para contar el número de cadenas en una estructura de datos anidada
def count_strings(data):
    count = 0
    if isinstance(data, dict):
        for value in data.values():
            count += count_strings(value)
    elif isinstance(data, list):
        for item in data:
            count += count_strings(item)
    elif isinstance(data, str):
        count += 1
    return count

# Función para traducir todas las cadenas en una estructura de datos anidada
def translate(data, src='en', dest='es'):
    total_strings = count_strings(data)

    # Función auxiliar para recopilar todas las cadenas en la estructura de datos
    def translate_dict(d, futures, path=[]):
        for key, value in d.items():
            current_path = path + [key]
            if isinstance(value, dict):
                translate_dict(value, futures, current_path)
            elif isinstance(value, list):
                for index, item in enumerate(value):
                    if isinstance(item, dict):
                        translate_dict(item, futures, current_path + [index])
                    elif isinstance(item, str):
                        futures.append((current_path, index, item))
            elif isinstance(value, str):
                futures.append((current_path, None, value))

    futures = []
    translate_dict(data, futures)

    # Utilizar ThreadPoolExecutor para traducir cadenas concurrentemente
    with ThreadPoolExecutor() as executor:
        future_to_key = {executor.submit(translate_text, item[2], src, dest): item for item in futures}
        for future in tqdm(as_completed(future_to_key), total=total_strings, desc="Translating"):
            path, index, original_text = future_to_key[future]
            result = future.result()
            d = data
            for p in path[:-1]:
                d = d[p]
            if index is not None:
                d[path[-1]][index] = result
            else:
                d[path[-1]] = result

    return data

