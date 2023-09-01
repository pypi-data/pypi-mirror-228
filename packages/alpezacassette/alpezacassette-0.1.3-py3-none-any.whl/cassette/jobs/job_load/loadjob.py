import sqlite3
from ...lib import Fountain


def runloader(fountain_file, pname):

    # Conectar o crear la base de datos
    conn = sqlite3.connect(f"{pname}.cst")
    cursor = conn.cursor()

    # Crear una instancia de Fountain y parsear el guion
    with open(fountain_file, 'r', encoding='utf-8') as fountain_file:
        fountain_text = fountain_file.read()

    fountain = Fountain.Fountain(fountain_text)

    current_scene_number = None  # Para rastrear el número de escena actual

    # Insertar la información del guion en la base de datos
    for scene in fountain.elements:
        if scene.element_type == 'Scene Heading':
            # Insertar información de la escena
            current_scene_number = scene.scene_number
            cursor.execute('''
                INSERT INTO Scene (script_id, scene_number, location, description)
                VALUES (?, ?, ?, ?)
            ''', (1, current_scene_number, scene.element_text, ''))

        elif scene.element_type == 'Character':
            # Obtener el ID del personaje por nombre
            cursor.execute(
                'SELECT character_id FROM Character WHERE name = ?', (scene.element_text,))
            character_row = cursor.fetchone()

            if character_row is not None:
                character_id = character_row[0]
            else:
                # El personaje no se encontró, así que lo insertamos en la base de datos
                cursor.execute('''
                    INSERT INTO Character (script_id, name)
                    VALUES (?, ?)
                ''', (1, scene.element_text))

                # Recuperar el ID del personaje recién insertado
                cursor.execute('SELECT last_insert_rowid()')
                character_id = cursor.fetchone()[0]

        elif scene.element_type == 'Dialogue':
            # Obtener el ID de la última escena insertada
            cursor.execute('SELECT MAX(scene_id) FROM Scene')
            scene_id = cursor.fetchone()[0]

            # Insertar el diálogo
            cursor.execute('''
                INSERT INTO Dialogue (scene_id, character_id, text)
                VALUES (?, ?, ?)
            ''', (scene_id, character_id, scene.element_text))

        elif scene.element_type == 'Element':
            # Obtener el ID de la última escena insertada
            cursor.execute('SELECT MAX(scene_id) FROM Scene')
            scene_id = cursor.fetchone()[0]

            # Insertar elemento en la tabla Element
            cursor.execute('''
                INSERT INTO Element (scene_id, element_type, text)
                VALUES (?, ?, ?)
            ''', (scene_id, scene.element_type, scene.element_text))

    # Guardar los cambios y cerrar la conexión
    conn.commit()
    conn.close()
