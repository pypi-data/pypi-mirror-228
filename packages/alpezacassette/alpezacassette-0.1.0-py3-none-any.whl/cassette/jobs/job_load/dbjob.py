import os
import sqlite3


class DatabaseAlreadyExistsError(Exception):
    pass


def createDB(name):
    if os.path.exists(f"{name}.cst"):
        raise DatabaseAlreadyExistsError(f"El archivo {name}.cst ya existe.")

    conn = sqlite3.connect(f"{name}.cst")
    # Crear un cursor para ejecutar comandos SQL
    cursor = conn.cursor()

    # Sentencia SQL para crear la tabla Script
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Script (
        script_id INTEGER PRIMARY KEY,
        title TEXT,
        author TEXT,
        date_created DATE,
        description TEXT
    );
    ''')

    # Sentencia SQL para crear la tabla Scene
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Scene (
        scene_id INTEGER PRIMARY KEY,
        script_id INTEGER,
        scene_number TEXT,
        location TEXT,
        description TEXT,
        audioPath    TEXT,
        FOREIGN KEY (script_id) REFERENCES Script(script_id)
    );
    ''')

    # Sentencia SQL para crear la tabla Character
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Character (
        character_id INTEGER PRIMARY KEY,
        script_id INTEGER,
        name TEXT,
        FOREIGN KEY (script_id) REFERENCES Script(script_id)
    );
    ''')

    # Sentencia SQL para crear la tabla Dialogue
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Dialogue (
        dialogue_id INTEGER PRIMARY KEY,
        scene_id INTEGER,
        character_id INTEGER,
        text TEXT,
        audioPath TEXT,
        FOREIGN KEY (scene_id) REFERENCES Scene(scene_id),
        FOREIGN KEY (character_id) REFERENCES Character(character_id)
    );
    ''')

    # Sentencia SQL para crear la tabla Element
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Element (
        element_id INTEGER PRIMARY KEY,
        scene_id INTEGER,
        element_type TEXT,
        text TEXT,
        FOREIGN KEY (scene_id) REFERENCES Scene(scene_id)
    );
    ''')

    # Guardar los cambios y cerrar la conexión
    conn.commit()
    conn.close()
