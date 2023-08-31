import importlib
import logging
import traceback

# Configuración básica del logger
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class ModuleRunner:
    def __init__(self, job_name):
        self.job_name = job_name
        self.module_name = f"cassette.jobs.job_{job_name.lower()}.{job_name.capitalize()}"
        self.module = None

        try:
            self.module = importlib.import_module(self.module_name)
        except Exception as e:
            traceback.print_exc()
            logger.error(
                f"Error al cargar el módulo {self.module_name}: {str(e)}")

    def run(self, params):
        if self.module is None:
            logger.error(
                f"El módulo {self.module_name} no se pudo cargar. Consulta los registros de errores para más detalles.")
            return None

        if hasattr(self.module, 'get'):
            try:
                return self.module.get().run(params)
            except Exception as e:
                traceback.print_exc()
                logger.error(
                    f"Error al ejecutar el módulo {self.module_name}: {str(e)}")
                return None
        else:
            logger.error(
                f"La función 'get' no está definida en el módulo {self.module_name}.")
            return None

    def describe(self):
        if self.module is None:
            logger.error(
                f"El módulo {self.module_name} no se pudo cargar. Consulta los registros de errores para más detalles.")
            return None

        if hasattr(self.module, 'get'):
            try:
                return self.module.get().description
            except Exception as e:
                logger.error(
                    f"Error al ejecutar la función 'get().description' en el módulo {self.module_name}: {str(e)}")
                return None
        else:
            logger.error(
                f"La función 'get' no está definida en el módulo {self.module_name}.")
            return None
