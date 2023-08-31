import click
import os
from ..utils.EnvConfig import EnvConfig
from ..utils.ModuleRunner import ModuleRunner


@click.command()
def list_jobs():
    """
    Lista las carpetas bajo el directorio CPOC_JOBS_PATH que comienzan con 'job_'.
    """
    # Obtén la variable de entorno CPOC_JOBS_PATH
    jobs_path = EnvConfig.get_variable('CPOC_JOBS_PATH')

    click.echo(f'Listando trabajos en: {jobs_path}')
    job_folders = [folder for folder in os.listdir(
        jobs_path) if folder.startswith('job_')]

    if job_folders:
        # Quita el prefijo 'job_' de los nombres de las carpetas
        job_names = [folder[len('job_'):] for folder in job_folders]
        click.echo('Trabajos disponibles:')
        for job_name in job_names:
            description = ModuleRunner(job_name).describe()
            click.echo(f'- {job_name}: {description}')
    else:
        click.echo('No se encontraron trabajos.')


def register_commands(cli):
    cli.add_command(list_jobs)


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
