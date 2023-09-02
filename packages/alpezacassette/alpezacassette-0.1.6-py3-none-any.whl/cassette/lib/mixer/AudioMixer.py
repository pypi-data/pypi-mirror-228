from pydub import AudioSegment
# import yaml


class VoiceLayer:
    def __init__(self):
        self.sound_layer = AudioSegment.empty()
        self.timeline = []

    def load_timeline(self, timeline_yaml):
        # with open(timeline_yaml, 'r') as file:
        #    self.timeline = yaml.safe_load(file)['timeline']
        self.timeline = timeline_yaml

    def mix_audio(self):
        for i, item in enumerate(self.timeline):
            if item['type'] == 'sound':

                audio = AudioSegment.from_file(item['track'])

                if 'duration' in item:
                    duration = int(item['duration']) * \
                        1000  # Duración en milisegundos
                    audio = audio[:duration]

                if 'volume' in item:
                    if item['volume'] == 'fadein':
                        audio = audio.fade_in(3000)  # 3 segundos
                    elif item['volume'] == 'fadeout':
                        audio = audio.fade_out(3000)  # 3 segundos
                    elif item['volume'] == 'inout':
                        audio = audio.fade_in(3000).fade_out(
                            3000)  # 3 segundos

                if i > 0 and self.timeline[i - 1]['type'] == 'scene':
                    # Aplicar transición cruzada con la escena anterior
                    crossfade_duration = 1200  # 1.2 seg
                    crossfade = audio[:crossfade_duration].overlay(
                        self.sound_layer[-crossfade_duration:], loop=True)
                    self.sound_layer = self.sound_layer[:-crossfade_duration] + \
                        crossfade + audio[crossfade_duration:]
                else:
                    self.sound_layer += audio

            elif item['type'] == 'scene':

                scene_audio = AudioSegment.from_file(item['scene_id'])
                if 'background' in item:

                    background_audio = AudioSegment.from_file(
                        item['background'])

                    # Ajustar el volumen del fondo
                    background_audio = background_audio - 20

                    scene_audio = scene_audio.overlay(
                        background_audio, loop=True)

                if i > 0 and self.timeline[i - 1]['type'] == 'sound':
                    # Aplicar transición cruzada con el sonido anterior
                    crossfade_duration = 1500  # 3 segundos
                    crossfade = scene_audio[:crossfade_duration].overlay(
                        self.sound_layer[-crossfade_duration:], loop=True)
                    self.sound_layer = self.sound_layer[:-crossfade_duration] + \
                        crossfade + scene_audio[crossfade_duration:]
                else:
                    self.sound_layer += scene_audio

    def export_mixed_audio(self, output_path):
        normalized_audio = self.sound_layer
        normalized_audio.export(output_path, format="mp3")


"""
if __name__ == "__main__":
    mixer = VoiceLayer()
    mixer.load_timeline("timeline.yaml")
    mixer.mix_audio()
    mixer.export_mixed_audio("output.mp3")
"""
