'''
    Setup logging
'''

import logging
from executioner.settings import Settings

LOGGER = logging.getLogger("executioner")
LOGGER.setLevel(Settings.get("logLevel", logging.WARNING))
