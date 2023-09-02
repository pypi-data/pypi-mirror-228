from ...lib import Descriptor
import json


def formato_minutos(minutos):
    sec = minutos * 60
    sec = sec % (24 * 3600)
    hour = sec // 3600
    sec %= 3600
    min = sec // 60
    sec %= 60
    return "%02d:%02d:%02d" % (hour, min, sec)


def print_ascii_box(text):
    box_width = len(text) + 4
    horizontal_line = "+" + "-" * box_width + "+"
    empty_line = "| " + " " * len(text) + "   |"

    print(horizontal_line)
    print(empty_line)
    print(f"| {text}  |")
    print(empty_line)
    print(horizontal_line)


def print_readable_info(script_info):
    print_ascii_box("📊 Estadísticas:")
    print(
        f"Total de Caracteres Distintos: {script_info['stats']['totalCaracteres']}")
    print(f"Total de Escenas: {script_info['stats']['totalScenes']}")
    print(
        f"Total de Líneas de Diálogo: {script_info['stats']['totalLineasDialogo']}")
    print(
        f"Total de Palabras en Diálogo: {script_info['stats']['totalDePalabras']}")
    print(
        f"Minutos estimados de Diálogo: {formato_minutos(script_info['stats']['estimacionTiempo'])}\n")

    print_ascii_box("🏠 Escenas:")
    for scene in script_info['scenes']:
        print(
            f"{scene['pos']}, {formato_minutos(scene['time'])}, {scene['name']}")

    print_ascii_box("👨‍🦰 Caracteres: ")
    for character in script_info['caracteres']:
        print(character)


def print_json_info(script_info):
    json_info = json.dumps(script_info, indent=4)
    print(json_info)


def run(params):
    dsc = Descriptor.Descriptor(f"{params['pname']}.cst").get_script_info()
    if "json" in params:
        print_json_info(dsc)
    else:
        print_readable_info(dsc)
