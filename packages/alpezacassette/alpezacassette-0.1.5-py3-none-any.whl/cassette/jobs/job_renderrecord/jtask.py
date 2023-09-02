import os
import sqlite3
import logging
import json
from ...lib.mixer import AudioMixer


def extract_content(dictionary_list):
    content_list = []
    for item in dictionary_list:
        if 'content' in item:
            content_list.append(item['content'])
    return content_list


def run(params):
    logger = logging.getLogger(__name__)

    # 1. Mira si existe el directorio indicado en `params['storepath']`.
    # Si no existe, créalo y notifica con un logger.debug que lo ha creado.
    storepath = params['storepath']
    if not os.path.exists(storepath):
        os.makedirs(storepath)
        logger.debug(f"Created directory: {storepath}")

    # 2. Dentro de este directorio crea una carpeta llamada `film`
    film_dir = os.path.join(storepath, "film")
    if not os.path.exists(film_dir):
        os.makedirs(film_dir)

    # 3. Se conecta a la sqlite3 especificada en `params['pname']`.
    db_file = f"{params['pname']}.cst"
    if not os.path.exists(db_file):
        logger.error(f"The project {db_file} does not exist.")
        return

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # 4. Recupera el contenido de la tabla Tags y monta un diccionario name:value
    tags_dict = {}
    cursor.execute("SELECT name, value FROM Tags")
    for row in cursor.fetchall():
        name, value = row
        tags_dict[name] = value

    # 5. Recupera el contenido de la tabla Timeline
    timeline_entries = []
    cursor.execute("SELECT type, content FROM Timeline")
    for row in cursor.fetchall():
        entry_type, content_json = row
        content_dict = json.loads(content_json)
        timeline_entries.append({"type": entry_type, "content": content_dict})

    # 6. Itera sobre los elementos del array y realiza las sustituciones
    for entry in timeline_entries:
        if entry["type"] == "scene":
            scene_id = entry["content"]["scene_id"]
            cursor.execute(
                "SELECT audioPath FROM Scene WHERE scene_id=?", (scene_id,))
            audio_path = cursor.fetchone()
            if audio_path:
                entry["content"]["scene_id"] = audio_path[0]
            if 'background' in entry["content"]:
                entry["content"]["background"] = tags_dict[entry["content"]["background"]]
        elif entry["type"] == "sound":
            track = entry["content"].get("track")
            if track in tags_dict:
                entry["content"]["track"] = tags_dict[track]

    mixer = AudioMixer.VoiceLayer()
    mixer.load_timeline(extract_content(timeline_entries))
    mixer.mix_audio()
    mixer.export_mixed_audio(film_dir + "/" + params['pname'] + ".mp3")


"""
if __name__ == "__main__":
    # Example usage:
    params = {
        'storepath': "/path/to/store",
        'pname': "/path/to/project.db"
    }
    run(params)
"""
