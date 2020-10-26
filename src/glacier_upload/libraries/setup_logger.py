import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%b-%d-%Y %H:%M:%S')
logging.getLogger("botocore").setLevel(logging.WARNING)
logger = logging.getLogger("glacier_logger")
