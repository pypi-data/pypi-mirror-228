from ...utils import Job
from . import jtask

description = "Carga al proyecto un timeline con extension yaml"
configMap = {
    "type": "object",
    "properties": {
        "pname": {
            "type": "string",
            "description": "Nombre del proyecto."
        },
        "timeline": {
            "type": "string",
            "description": "Timeline .yaml a cargar."
        }
    },
    "required": ["pname", "timeline"]
}


class MJob(Job.Job):
    def __init__(self):
        super().__init__(description,
                         configMap)

    def task(self):
        jtask.run(self.params)


def get():
    return MJob()
