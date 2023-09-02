# cassette/main.py

import click
from cassette.commands import run, list_jobs
from cassette.utils import EnvConfig

EnvConfig.EnvConfig.load_dotenv()


@click.group()
def cli():
    """
    🎬 Cassette 📼 - Aplicación para renderizar escenas desde archivos Fountain con configuraciones YAML.
    """
    pass


# Registrar todos los comandos
run.register_commands(cli)
list_jobs.register_commands(cli)


def main():
    cli()


if __name__ == '__main__':
    main()
