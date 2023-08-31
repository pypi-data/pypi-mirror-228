from . import dbjob
from . import loadjob


def run(params):
    # Creamos la base de datos
    dbjob.createDB(params['pname'])
    # Cargamos el fichero fountain
    loadjob.runloader(params['timeline'], params['pname'])
