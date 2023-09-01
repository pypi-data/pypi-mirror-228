import sqlite3
import json
from . import CharacterAudio
import os
import logging
from concurrent.futures import ThreadPoolExecutor


class CharacterAudioRender:

    def __init__(self, character_id, db_file):
        self.db_file = db_file
        self.character_id = character_id
        self._load()
        self.logger = logging.getLogger(__name__)

    def _load(self):
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        query = '''
        SELECT Character.character_id, name, tts
        FROM Character
        INNER JOIN CharacterDescriptor ON Character.character_id = CharacterDescriptor.character_id
        WHERE Character.character_id = ?;
        '''
        cursor.execute(query, (self.character_id,))
        character_data = cursor.fetchone()
        conn.close()

        if character_data:
            self.name = character_data['name']
            self.tts = json.loads(character_data['tts'])
            self.audio = CharacterAudio.CharacterAudio(config=self.tts)
            return True
        else:
            return False

    def render_dialogue(self, dialogue_id, text, output_path):
        try:
            self.audio.say(text, out=output_path)

            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            update_query = '''
            UPDATE Dialogue
            SET audioPath = ?
            WHERE dialogue_id = ?;
            '''
            cursor.execute(update_query, (output_path, dialogue_id))
            conn.commit()
            conn.close()
            self.logger.debug(
                f"Rendered dialogue {dialogue_id} to {output_path}")
        except Exception as e:
            self.logger.error(
                f"Error rendering dialogue {dialogue_id}: {str(e)}")

    def renderAllDialogs(self, outputDirectory, maxjobs=1, outprefix=""):
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        query = '''
        SELECT dialogue_id, text
        FROM Dialogue
        WHERE character_id = ?;
        '''
        cursor.execute(query, (self.character_id,))
        dialogues = cursor.fetchall()
        conn.close()

        self.logger.info(f"Started rendering {len(dialogues)} dialogues.")

        with ThreadPoolExecutor(maxjobs) as executor:
            futures = []
            for dialogue in dialogues:
                dialogue_id = dialogue['dialogue_id']
                text = dialogue['text']
                output_path = os.path.join(
                    outputDirectory, f"{outprefix}{self.character_id}_{dialogue_id}.wav")
                futures.append(executor.submit(
                    self.render_dialogue, dialogue_id, text, output_path))

            for future in futures:
                future.result()

        self.logger.info("Finished rendering all dialogues.")


"""
if __name__ == "__main__":
    # Example usage:
    character_id = 1
    db_file = "/Users/alvaroperis/Dropbox/cinemawritter/fontana/miguion.cst"
    output_dir = "/Users/alvaroperis/Dropbox/cinemawritter/fontana/salidas"

    # Configura el nivel de log a DEBUG
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    renderer = CharacterAudioRender(character_id, db_file)
    renderer.renderAllDialogs(output_dir)
"""
