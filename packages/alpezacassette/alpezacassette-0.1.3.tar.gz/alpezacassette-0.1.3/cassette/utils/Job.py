import jsonschema
import logging
import sys


class Job:
    def __init__(self, description="", configMap={}):
        """
        Constructor de la clase Job.

        :param description: Descripción del trabajo.
        :param configMap: Diccionario que representa un JSON Schema.
        """
        self.description = description
        self.configMap = configMap
        self.params = {}

    def __str__(self):
        return f"Job(description='{self.description}', configMap={self.configMap})"

    def _validate_config(self, params):
        """
        Valida el diccionario params con un JSON Schema.
        """
        try:
            jsonschema.validate(instance=params, schema=self.configMap)
            return True
        except jsonschema.exceptions.ValidationError as e:
            logging.error("Error de validación del JSON Schema: %s", e)
            # Obtener la lista de campos faltantes
            campos_faltantes = [err.split("'")[1] for err in e.validator_value]
            logging.error(campos_faltantes)
            return False

    def task(self):
        logging.warning(
            f"Este job no realiza ninguna task. Implemente la función `task()`")

    def getParam(self, param):
        return self.params[param]

    def run(self, params):
        if self.configMap:
            if not self._validate_config(params):
                logging.error("Error al ejecutar el job")
                sys.exit(1)
            else:
                self.params = params
        logging.debug(f"Lanzando job con los parametros {str(params)}")
        self.task()
