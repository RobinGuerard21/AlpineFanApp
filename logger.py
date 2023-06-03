import logging
import sys
import datetime
import os

current_date = datetime.date.today().strftime("%Y-%m-%d")

# Configure logging to write to a file
log_file = f"{current_date}.log"
if not os.path.exists("logs"):
    os.mkdir("logs")
logging.basicConfig(filename=os.path.join("logs", log_file), filemode="w", level=logging.INFO,
                    format='%(asctime)s  - %(levelname)-8s - %(name)s - %(message)s')
# logger = logging.getLogger('alpine_fan')
# logger.setLevel(logging.INFO)
#
# ch = logging.StreamHandler()
# ch.setLevel(logging.INFO)
#
# logger.addHandler(ch)

#
# stream_handler = logging.StreamHandler(sys.stdout)
# stream_handler.setLevel(logging.INFO)
# logging.getLogger().addHandler(stream_handler)
