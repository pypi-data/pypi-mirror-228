import pyttsx3
import logging
import os
import random
from pedalboard import Pedalboard, Reverb, Distortion, Delay, Gain
from pedalboard.io import AudioFile

# Configura el sistema de registro (logging)
logger = logging.getLogger(__name__)

TMP_OUTWAV = "/tmp"

EXAMPLE_VOICE_CONFIG = {
    "voice": {
        "tts": {
            "voiceid": 14,
            "rate": 200,
            "volume": 1
        },
        "filter": [
            {
                "reverb": {
                    "room_size": 0.5,
                    "damping": 0.5,
                    "wet_level": 0.33,
                    "dry_level": 0.4,
                    "width": 1.0,
                    "freeze_mode": 0.0
                }
            },
            {
                "distortion": {
                    "drive_db": 25
                }
            },
            {
                "delay": {
                    "delay_seconds": 0.5,
                    "feedback": 0.0,
                    "mix": 0.5
                }
            },
            {
                "gain": {
                    "gain_db": 1.0
                }
            }
        ]
    }
}


class CharacterAudio:
    def __init__(self, config=None):
        self.engine = pyttsx3.init()
        self._character_config = config
        self.current_say = None  # Almacena la última salida generada
        self.filters = []

        self._configureTTS(self._character_config)
        self._configureFilters(self._character_config)

    def _configureTTS(self, config):
        if config and "voice" in config:
            voice_config = config["voice"]
            if "tts" in voice_config:
                tts_config = voice_config["tts"]
                for key, value in tts_config.items():
                    if key == "voiceid":
                        voice_id = self.engine.getProperty('voices')[value].id
                        self.engine.setProperty('voice', voice_id)
                        logger.debug(
                            f"Configurando propiedad 'voice' a '{voice_id}'")
                    else:
                        self.engine.setProperty(key, value)
                        logger.debug(
                            f"Configurando propiedad '{key}' a '{value}'")

    def _configureFilters(self, config):
        if config and "voice" in config:
            for filter_item in config.get('voice').get("filter", []):
                for filter_name, filter_params in filter_item.items():
                    if filter_name == "reverb":
                        reverb = Reverb(
                            room_size=filter_params.get("room_size", 0.5),
                            damping=filter_params.get("damping", 0.5),
                            wet_level=filter_params.get("wet_level", 0.33),
                            dry_level=filter_params.get("dry_level", 0.4),
                            width=filter_params.get("width", 1.0),
                            freeze_mode=filter_params.get("freeze_mode", 0.0)
                        )
                        self.filters.append(reverb)
                    elif filter_name == "distortion":
                        distortion = Distortion(
                            drive_db=filter_params.get("drive_db", 25)
                        )
                        self.filters.append(distortion)
                    elif filter_name == "delay":
                        delay = Delay(
                            delay_seconds=filter_params.get(
                                "delay_seconds", 0.5),
                            feedback=filter_params.get("feedback", 0.0),
                            mix=filter_params.get("mix", 0.5)
                        )
                        self.filters.append(delay)
                    elif filter_name == "gain":
                        gain = Gain(
                            gain_db=filter_params.get("gain_db", 1.0)
                        )
                        self.filters.append(gain)

    def ttsay(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def ttsay_and_save(self, text, out):
        try:
            self.engine.save_to_file(text, out)
            self.engine.runAndWait()
            logger.debug(f"Salida guardada en '{out}'")
        except Exception as e:
            logger.error(f"Error al guardar la salida en '{out}': {str(e)}")

    def addFilters(self, inputwav, out):
        board = Pedalboard(self.filters)
        with AudioFile(inputwav) as f:
            with AudioFile(out, 'w', f.samplerate, f.num_channels) as o:
                while f.tell() < f.frames:
                    chunk = f.read(f.samplerate)
                    effected = board(chunk, f.samplerate, reset=False)
                    o.write(effected)

    def say(self, text, out="/tmp/tmpcharacter.wav"):
        self.current_say = out

        if self.filters:
            logger.debug(f"Aplicando filtros")
            # Extraer el nombre del archivo del parámetro 'out'
            out_filename = os.path.basename(out).split('.')[0]
            # Generar un valor aleatorio de tres dígitos
            random_number = random.randint(100, 999)
            # Construir el nombre del archivo temporal
            temp_filename = f"{out_filename}-{random_number}.tmp.wav"
            # Unir el directorio base con el nombre del archivo temporal
            full_path = os.path.join(TMP_OUTWAV, temp_filename)
            self.ttsay_and_save(text, full_path)
            self.addFilters(full_path, out)
            os.remove(full_path)
        else:
            logger.debug(f"Sin filtros")
            self.ttsay_and_save(text, out)

        logger.debug(f"Salida de say guardada en '{out}'")
