import sqlite3
import yaml
import json


def load_tags(name, yaml_data):
    conn = sqlite3.connect(name)
    cursor = conn.cursor()

    for key, value in yaml_data.get("tags", {}).items():
        cursor.execute(
            "INSERT INTO Tags (name, value) VALUES (?, ?);", (key, value))

    conn.commit()
    conn.close()


def load_characters(name, yaml_data):
    conn = sqlite3.connect(name)
    cursor = conn.cursor()

    for character in yaml_data.get("characters", []):
        character_id = character.get("id")
        tts = json.dumps(character)
        cursor.execute(
            "INSERT INTO CharacterDescriptor (character_id, tts) VALUES (?, ?);", (character_id, tts))

    conn.commit()
    conn.close()


def load_timeline(name, yaml_data):
    conn = sqlite3.connect(name)
    cursor = conn.cursor()

    timeline = yaml_data.get("timeline", [])
    for sequence_id, item in enumerate(timeline):
        sequence_type = item.get("type")
        content = json.dumps(item)
        cursor.execute("INSERT INTO Timeline (sequence_id, type, content) VALUES (?, ?, ?);",
                       (sequence_id, sequence_type, content))

    conn.commit()
    conn.close()


def runloader(timeline_file, pname):

    # Cargar datos desde el archivo YAML
    nombre_base_de_datos = f"{pname}.cst"
    yaml_file = timeline_file

    with open(yaml_file, 'r') as f:
        yaml_data = yaml.safe_load(f)

    # Cargar los datos en las tablas
    load_tags(nombre_base_de_datos, yaml_data)
    load_characters(nombre_base_de_datos, yaml_data)
    load_timeline(nombre_base_de_datos, yaml_data)
