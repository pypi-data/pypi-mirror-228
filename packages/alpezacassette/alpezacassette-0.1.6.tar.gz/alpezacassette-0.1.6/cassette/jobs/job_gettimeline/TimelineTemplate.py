import jinja2

templates = {
    "default": """
tags:
  # Tagexamples
  sound1: /Users/alvaroperis/Dropbox/cinemawritter/playmix/hinds.wav
  bg: /Users/alvaroperis/Dropbox/cinemawritter/playmix/intro.wav
characters:
  {% for character in characters %}
  # {{ character.name }}
  - id: {{ character.character_id }}
    voice:
      tts:
        voiceid: 14
      filter:
        - reverb:
            room_size: 0.1
  {% endfor %}
timeline:
  {%- for scene in scenes %}
  # {{ scene.location }}
  - type: scene
    scene_id: {{ scene.scene_id }}
    background: bg
  - type: sound
    track: sound1
    duration: 8
    volume: inout
  {% endfor %}
        """
}


class TimelineTemplate:

    def __init__(self, template_string):

        if template_string in templates:
            # Si template_string es un nombre de plantilla en el diccionario templates
            self.template_string = template_string
            self.template = jinja2.Template(templates[template_string])
        else:
            # Si template_string es un nombre de archivo o una ruta de archivo
            try:
                with open(template_string, 'r') as file:
                    self.template_string = file.read()
                self.template = jinja2.Template(self.template_string)
            except FileNotFoundError:
                raise ValueError(f"File '{template_string}' not found.")

    def render(self, **kwargs):
        return self.template.render(**kwargs)
