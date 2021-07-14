import logging

logging.basicConfig(level="DEBUG")
logger = logging.getLogger("my_log")
debug_handler = logging.FileHandler(filename="debug.log", mode="a+")
debug_handler.setLevel(logging.DEBUG)
warning_handler = logging.FileHandler(filename="warning.log", mode="a+")
warning_handler.setLevel(logging.WARNING)
critical_handler = logging.FileHandler(filename="critical.log", mode="a+")
critical_handler.setLevel(logging.CRITICAL)
logger.addHandler(debug_handler)
logger.addHandler(warning_handler)
logger.addHandler(critical_handler)
