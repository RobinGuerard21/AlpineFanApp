import logging
import sys
import datetime
import os

current_date = datetime.date.today().strftime("%Y-%m-%d")

# Configure logging to write to a file
log_file = f"{current_date}.log"
if not os.path.exists("logs"):
    os.mkdir("logs")
logging.basicConfig(filename=os.path.join("logs", log_file), level=logging.INFO,
                    format='%(asctime)s - %(levelname)-8s - %(message)s')

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.INFO)
logging.getLogger().addHandler(stream_handler)

class StreamToLogger:
    def __init__(self, logger, level=logging.INFO):
        self.logger = logger
        self.level = level

    def write(self, message):
        self.logger.log(self.level, message)

    def flush(self):
        pass

# Create a logger
logger = logging.getLogger('console')

# Redirect stdout and stderr to the logger
sys.stdout = StreamToLogger(logger, logging.INFO)
sys.stderr = StreamToLogger(logger, logging.ERROR)

def close_log_file():
    logging.shutdown()

# Register the close_log_file function to be called on program exit or reload
sys.exitfunc = close_log_file