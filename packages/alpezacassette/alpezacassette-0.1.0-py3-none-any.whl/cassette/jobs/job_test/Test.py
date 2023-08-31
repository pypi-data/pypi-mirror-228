from ...utils import Job
from . import jtask

description = "Ejemplo de job test para plantilla de desrrollo."
configMap = {
    "type": "object",
    "properties": {
        "nombreArchivo": {
            "type": "string",
            "description": "El nombre del archivo."
        },
        "ruta": {
            "type": "string",
            "description": "La ruta del archivo."
        }
    },
    "required": ["nombreArchivo", "ruta"]
}


class MJob(Job.Job):
    def __init__(self):
        super().__init__(description,
                         configMap)

    def task(self):
        jtask.run(self.params)


def get():
    return MJob()
