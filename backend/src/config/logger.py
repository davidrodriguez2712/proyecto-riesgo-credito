import logging.config
import yaml
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
CONFIG_PATH = BASE_DIR / "src" / "config" / "logger.yaml"
def setup_logging(path = CONFIG_PATH):
    with open(path, 'r') as file:
        config_log = yaml.safe_load(file)
        logging.config.dictConfig(config_log)

setup_logging()

logger = logging.getLogger('mlops')
logger.debug('Cargado correctamente la configuración del logging')


if __name__ == '__main__':
    print(BASE_DIR)
    print(CONFIG_PATH)
