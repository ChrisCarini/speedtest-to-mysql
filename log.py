import logging
import sys

from logging.handlers import RotatingFileHandler

##
# Setup Logging
##
logger = logging.getLogger()
formatter = logging.Formatter(fmt='%(asctime)s - [%(levelname)s] - %(message)s')

stream_handler = logging.StreamHandler(stream=sys.stdout)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

file_handler = RotatingFileHandler('speedtest_to_mysql.log', backupCount=5, maxBytes=1000000)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

logger.setLevel(logging.INFO)
