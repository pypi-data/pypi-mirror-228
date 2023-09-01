from ...utils import Job
from . import jtask

description = "Renderiza el audio por separado de los personajes."
configMap = {
    "type": "object",
    "properties": {
        "pname": {
            "type": "string",
            "description": "Nombre del fichero del proyecto sin extension."
        },
        "storepath": {
            "type": "string",
            "description": "Ruta donde se almacenará la salida."
        }
    },
    "required": ["pname", "storepath"]
}


class MJob(Job.Job):
    def __init__(self):
        super().__init__(description,
                         configMap)

    def task(self):
        jtask.run(self.params)


def get():
    return MJob()
