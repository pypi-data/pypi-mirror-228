import os
import sqlite3
import logging
import sys
from ...lib.scene import SceneAudioRender


def run(params):
    logger = logging.getLogger(__name__)

    # 1. Mira si existe el directorio indicado en `params['storepath']`.
    # Si no existe, créalo y notifica con un logger.debug que lo ha creado.
    storepath = params['storepath']
    if not os.path.exists(storepath):
        os.makedirs(storepath)
        logger.debug(f"Created directory: {storepath}")

    # 2. Dentro de este directorio crea una carpeta llamada `scenes`
    scenes_dir = os.path.join(storepath, "secenes")
    if not os.path.exists(scenes_dir):
        os.makedirs(scenes_dir)

    # 3. Se conecta a la sqlite3 especificada en `params['pname']`.
    db_file = f"{params['pname']}.cst"
    if not os.path.exists(db_file):
        logger.error(f"The project {db_file} does not exist.")
        return

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # 4. Obtiene el `scene_id` de todos los personajes.
    cursor.execute('SELECT scene_id FROM Scene;')
    scene_ids = cursor.fetchall()
    conn.close()

    for scene_id in scene_ids:
        scene_name = f"scene_{str(scene_id[0])}"
        scene_id = scene_id[0]
        output_dir = os.path.join(scenes_dir, str(scene_name))
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        renderer = SceneAudioRender.SceneAudioRender(
            scene_id, db_file)
        if renderer.isDialogueRendered():
            renderer.renderScene(output_dir)
        else:
            print(
                f"Error, los dialogos de la scena {str(scene_id)} no se han renderizado. Revise si se han renderizado los dialogos ")
            sys.exit(1)


"""
if __name__ == "__main__":
    # Example usage:
    params = {
        'storepath': "/path/to/store",
        'pname': "/path/to/project.db"
    }
    run(params)
"""
