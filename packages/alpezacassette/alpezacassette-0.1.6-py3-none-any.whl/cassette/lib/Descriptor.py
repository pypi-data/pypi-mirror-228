import sqlite3
palabras_por_minuto = 130


class Descriptor:
    def __init__(self, db_file):
        self.db_file = db_file

    def get_script_info(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        # Obtener información general del guión (script)
        cursor.execute("SELECT COUNT(DISTINCT name) FROM Character")
        total_caracteres = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM Scene")
        total_scenes = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM Dialogue")
        total_lineas_dialogo = cursor.fetchone()[0]

        cursor.execute(
            "SELECT SUM(LENGTH(text) - LENGTH(REPLACE(text, ' ', '')) + 1) FROM Dialogue")
        total_de_palabras = cursor.fetchone()[0]

        conn.close()

        return {
            "stats": {
                "totalCaracteres": total_caracteres,
                "totalScenes": total_scenes,
                "totalLineasDialogo": total_lineas_dialogo,
                "totalDePalabras": total_de_palabras,
                "estimacionTiempo": round(total_de_palabras / palabras_por_minuto, 1)
            },
            "scenes": self.get_scene_info(),
            "caracteres": self.get_character_info(),
        }

    def get_scene_info(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        # Obtener información de las escenas (scenes)
        cursor.execute(
            "SELECT scene_id, location FROM Scene ORDER BY scene_id ASC")
        scenes = cursor.fetchall()

        scene_info = []

        for scene in scenes:
            scene_id = scene[0]
            location = scene[1]

            # Calcular el número de palabras en la escena actual
            cursor.execute(
                "SELECT SUM(LENGTH(text) - LENGTH(REPLACE(text, ' ', '')) + 1) FROM Dialogue WHERE scene_id = ?", (scene_id,))
            palabras_escena = cursor.fetchone()[0]

            # Calcular la duración estimada de la escena actual
            if palabras_escena is None:
                palabras_escena = 0
            minutos_estimados = round(palabras_escena / palabras_por_minuto, 2)

            scene_info.append({
                "pos": scene_id,
                "name": location,
                "words": palabras_escena,
                "time": minutos_estimados
            })

        conn.close()

        return scene_info

    def get_character_info(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        # Obtener información de los caracteres (characters)
        cursor.execute("SELECT name FROM Character")
        characters = cursor.fetchall()

        conn.close()

        return [character[0] for character in characters]

    def get_characters(self):
        conn = sqlite3.connect(self.db_file)
        # Configurar el cursor para retornar resultados como diccionarios
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Character")
        characters = cursor.fetchall()
        conn.close()
        return characters

    def get_scenes(self):
        conn = sqlite3.connect(self.db_file)
        # Configurar el cursor para retornar resultados como diccionarios
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Scene")
        scenes = cursor.fetchall()
        conn.close()
        return scenes


# Uso de la clase Descriptor
if __name__ == "__main__":
    db_file_path = "ejemplo.cst"
    descriptor = Descriptor(db_file_path)
    script_info = descriptor.get_script_info()
    print(script_info)
