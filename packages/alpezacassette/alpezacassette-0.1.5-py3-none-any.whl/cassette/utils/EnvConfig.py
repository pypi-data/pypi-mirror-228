import os
import logging
from dotenv import load_dotenv


class EnvConfig:
    @staticmethod
    def load_dotenv():
        """
        Carga las variables de entorno desde un archivo .env en la misma ubicación que el módulo.
        """
        # Obtén la ruta absoluta del directorio del módulo
        module_dir = os.path.dirname(os.path.abspath(__file__))

        # Calcula la ruta absoluta al archivo .env en la misma ubicación que el módulo
        env_file_path = os.path.join(module_dir, '.env')
        # print(env_file_path)
        # Carga las variables de entorno desde el archivo .env
        load_dotenv(env_file_path)

        # Establece el nivel de registro (log level) en base a CPOC_LOG_LEVEL
        log_level = os.getenv('CPOC_LOG_LEVEL', 'DEBUG')
        logging.basicConfig(level=log_level)

        # Muestra todas las variables de entorno en modo de depuración
        logger = logging.getLogger(__name__)
        for key, value in os.environ.items():
            if key.startswith('CPOC_'):
                logger.debug(f'{key}={value}')

    @staticmethod
    def get_variable(variable_name, default=None):
        """
        Recupera el valor de una variable de entorno.

        :param variable_name: Nombre de la variable de entorno.
        :param default: Valor por defecto a retornar si la variable no está definida.
        :return: El valor de la variable de entorno o el valor por defecto si no está definida.
        """
        if variable_name in os.environ:
            return os.getenv(variable_name, default)
        else:
            logging.warning(
                f"La variable de entorno '{variable_name}' no existe. Se retornará el valor default '{default}'")
            return default
