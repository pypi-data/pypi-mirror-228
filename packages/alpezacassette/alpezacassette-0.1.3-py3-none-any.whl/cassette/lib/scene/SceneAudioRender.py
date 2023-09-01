import sqlite3
import json
from pydub import AudioSegment


class SceneAudioRender:

    def __init__(self, scene_id, db_file):
        self.db_file = db_file
        self.scene_id = scene_id
        self._load()

    def _load(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT dialogue_id, audioPath FROM Dialogue WHERE scene_id = ? ORDER BY dialogue_id ASC", (self.scene_id,))
        self.dialogue_records = cursor.fetchall()
        conn.close()

    def isDialogueRendered(self):
        """
        Valida que el campo `audioPath` esté informado en todos los registros de la tabla `Dialogue`
        para el `scene_id` especificado.
        """
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM Dialogue WHERE scene_id = ? AND audioPath IS NULL", (self.scene_id,))
        count = cursor.fetchone()[0]
        conn.close()

        if count == 0:
            return True  # Todos los registros tienen audioPath informado
        else:
            return False  # Al menos un registro no tiene audioPath informado

    def renderScene(self, outputDirectory, outprefix=""):
        concatenated_audio = AudioSegment.silent(
            duration=0)  # Inicializar un audio vacío

        for dialogue_id, audioPath in self.dialogue_records:
            audio = AudioSegment.from_file(audioPath, format="wav")
            concatenated_audio += audio

        output_path = f"{outputDirectory}/{outprefix}{self.scene_id}.wav"
        concatenated_audio.export(output_path, format="wav")

        # Actualizar la tabla Scene con la ruta de salida
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Scene SET audioPath = ? WHERE scene_id = ?", (output_path, self.scene_id))
        conn.commit()
        conn.close()
