import click
import json
import logging
from ..utils.ModuleRunner import ModuleRunner

# Configura el sistema de registro de registros
logger = logging.getLogger(__name__)


@click.command()
@click.option('--job', '-j', required=True, help='Nombre del job.')
@click.option('-p', '--param', multiple=True, help='Parámetros en formato "parametro=valor". Puedes especificar múltiples parámetros.')
def run(job, param):
    """
    Ejecuta el comando 'run' con un nombre de job y parámetros opcionales.
    """
    logger.info(f'Nombre del job: {job}')

    # Validar el formato "key=value" para todos los parámetros
    params_dict = {}
    for p in param:
        parts = p.split('=')
        if len(parts) != 2:
            logger.error(
                f'Error: El parámetro "{p}" no sigue el formato "key=value".')
            return
        key, value = parts
        params_dict[key] = value

    # Si todos los parámetros son válidos, exportar a JSON
    if params_dict:
        json_params = json.dumps(params_dict, indent=4)
        logger.debug(f'Parámetros en formato JSON:\n{json_params}')

    ModuleRunner(job).run(params_dict)


def register_commands(cli):
    cli.add_command(run)


@click.group()
def cli():
    """
    Mi aplicación de línea de comandos.
    """
    pass


# Registra el comando 'run' en la aplicación principal.
register_commands(cli)

if __name__ == '__main__':
    cli()
