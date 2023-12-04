# Logging using STD-logging-library
# This is a test file and to be added into mean.py 

import logging
import os

# Set up logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='logfile.log')

def log_info(message):
    logging.info(message)

def log_error(message):
    logging.error(message)

def log_debug(message):
    logging.debug(message)

# Example Usage
log_info("This is an info message")
log_error("This is an error message")
log_debug("This is a debug message")
