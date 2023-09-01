from ...utils import Job
from . import jtask

description = "Genera una plantilla yaml del proyecto."
configMap = {
    "type": "object",
    "properties": {
        "pname": {
            "type": "string",
            "description": "Nombre del proyecto"
        },
        "useDefault": {
            "type": "string",
            "description": "Nombre de la plantilla por defecto que se empleará"
        }
    },
    "required": ["pname"]
}


class MJob(Job.Job):
    def __init__(self):
        super().__init__(description,
                         configMap)

    def task(self):
        if not "useDefault" in self.params:
            self.params['useDefault'] = 'default'

        jtask.run(self.params)


def get():
    return MJob()
