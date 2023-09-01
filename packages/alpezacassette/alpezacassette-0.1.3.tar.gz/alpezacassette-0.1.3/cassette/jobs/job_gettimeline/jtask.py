from . import TimelineTemplate
from ...lib import Descriptor


def run(params):
    db_file_path = params['pname']
    output_file_path = f"{params['pname']}.yaml"

    descriptor = Descriptor.Descriptor(db_file_path)
    characters = descriptor.get_characters()
    scenes = descriptor.get_scenes()

    # Renderiza la plantilla con los datos
    rendered_yaml = TimelineTemplate.TimelineTemplate(
        params['useDefault']).render(characters=characters, scenes=scenes)

    # Guarda el resultado en un archivo YAML

    with open(output_file_path, "w") as output_file:
        output_file.write(rendered_yaml)

    print(f"Archivo YAML generado y guardado en {output_file_path}")
