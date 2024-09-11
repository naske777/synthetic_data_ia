import json
import sqlite3
import os

DB_PATH = 'db/data.db'

def create_connection():
    """Create a database connection to the SQLite database."""
    conn = None
    try:
        dir_path = os.path.dirname(DB_PATH)
        if not os.path.exists(dir_path):
            print(f"Directorio {dir_path} no existe. Creando...")
            os.makedirs(dir_path, exist_ok=True)
            print(f"Directorio {dir_path} creado.")
        else:
            print(f"Directorio {dir_path} ya existe.")
        
        conn = sqlite3.connect(DB_PATH)
        print(f"Conexión a la base de datos {DB_PATH} establecida.")
    except sqlite3.Error as e:
        print(f"Error al conectar con la base de datos: {e}")
    return conn

def create_table(table_name, keys):
    """Create a table with the given name and keys as columns if it doesn't exist."""
    conn = create_connection()
    if conn is not None:
        try:
            c = conn.cursor()
            columns = ', '.join([f"{key} TEXT" for key in keys])
            c.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} (
                            id INTEGER PRIMARY KEY,
                            {columns}
                        );''')
            conn.commit()
            print(f"Tabla '{table_name}' creada o ya existente con columnas: {keys}.")
        except sqlite3.Error as e:
            print(f"Error al crear la tabla {table_name}: {e}")
        finally:
            conn.close()
            print("Conexión a la base de datos cerrada.")

def insert_data_for_table(data, table_name):
    """Insert data into the specified table with keys as columns."""
    if not data:
        print("No hay datos para insertar.")
        return
    
    keys = data[0].keys()
    create_table(table_name, keys)  # Ensure the table exists with the correct columns
    
    conn = create_connection()
    if conn is not None:
        try:
            c = conn.cursor()
            columns = ', '.join(keys)
            placeholders = ', '.join(['?' for _ in keys])
            query = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'
            for item in data:
                values = tuple(item[key] for key in keys)
                c.execute(query, values)
            conn.commit()
            print(f"Datos insertados en la tabla '{table_name}'.")
        except sqlite3.Error as e:
            print(f"Error al insertar datos en la tabla {table_name}: {e}")
        finally:
            conn.close()
            print("Conexión a la base de datos cerrada.")

def get_data_from_table(table_name):
    """Fetch all data from the specified table and return it, excluding the ID column."""
    conn = create_connection()
    data = []
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute(f'SELECT * FROM {table_name}')
            rows = c.fetchall()
            for row in rows:
                data.append(dict(zip([desc[0] for desc in c.description[1:]], row[1:])))
        except sqlite3.Error as e:
            print(f"Error al recuperar todos los datos de la tabla {table_name}: {e}")
        finally:
            conn.close()
            print("Conexión a la base de datos cerrada.")
    return data
