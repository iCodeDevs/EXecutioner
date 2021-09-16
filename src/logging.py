'''
    Setup logging
'''

import logging
from src.settings import Settings

LOGGER = logging.getLogger("executioner")
LOGGER.setLevel(Settings.get("LOG_LEVEL", logging.WARNING))
