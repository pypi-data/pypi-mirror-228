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

        if template_string not in templates:
            raise ValueError(
                f"Template key '{template_string}' not found in the templates dictionary.")

        self.template_string = template_string
        self.template = jinja2.Template(templates[template_string])

    def render(self, **kwargs):
        return self.template.render(**kwargs)
