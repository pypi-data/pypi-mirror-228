from ...utils import Job
from . import jtask

description = "Crea un proyecto a partir de un fichero .fountain"
configMap = {
    "type": "object",
    "properties": {
        "fountain": {
            "type": "string",
            "description": "Path donde se encuentra el fichero fountain."
        },
        "pname": {
            "type": "string",
            "description": "Nombre del proyecto."
        }
    },
    "required": ["fountain", "pname"]
}


class MJob(Job.Job):
    def __init__(self):
        super().__init__(description,
                         configMap)

    def task(self):
        jtask.run(self.params)


def get():
    return MJob()
