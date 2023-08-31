from ...utils import Job
from . import jtask

description = "Describe un  proyecto cassette mostrando sus estadisticas."
configMap = {
    "type": "object",
    "properties": {
        "pname": {
            "type": "string",
            "description": "Nombre del proyecto cassette."
        },
        "json": {
            "type": "string",
            "description": "Flag opcional que indica si se ha de mostrar en json"
        }
    },
    "required": ["pname"]
}


class MJob(Job.Job):
    def __init__(self):
        super().__init__(description,
                         configMap)

    def task(self):
        jtask.run(self.params)


def get():
    return MJob()
