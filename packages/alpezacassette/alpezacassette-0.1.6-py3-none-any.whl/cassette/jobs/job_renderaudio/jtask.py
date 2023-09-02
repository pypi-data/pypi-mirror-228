import os
import sqlite3
import logging
from ...lib.character import CharacterAudioRender


def run(params):
    logger = logging.getLogger(__name__)

    # 1. Mira si existe el directorio indicado en `params['storepath']`.
    # Si no existe, créalo y notifica con un logger.debug que lo ha creado.
    storepath = params['storepath']
    if not os.path.exists(storepath):
        os.makedirs(storepath)
        logger.debug(f"Created directory: {storepath}")

    # 2. Dentro de este directorio crea una carpeta llamada `characters`
    characters_dir = os.path.join(storepath, "characters")
    if not os.path.exists(characters_dir):
        os.makedirs(characters_dir)

    # 3. Se conecta a la sqlite3 especificada en `params['pname']`.
    db_file = f"{params['pname']}.cst"
    if not os.path.exists(db_file):
        logger.error(f"The project {db_file} does not exist.")
        return

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # 4. Obtiene el `character_id` de todos los personajes.
    cursor.execute('SELECT character_id FROM Character;')
    character_ids = cursor.fetchall()
    conn.close()

    for character_id in character_ids:
        character_id = character_id[0]
        output_dir = os.path.join(characters_dir, str(character_id))
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        renderer = CharacterAudioRender.CharacterAudioRender(
            character_id, db_file)
        renderer.renderAllDialogs(output_dir)


"""
if __name__ == "__main__":
    # Example usage:
    params = {
        'storepath': "/path/to/store",
        'pname': "/path/to/project.db"
    }
    run(params)
"""
