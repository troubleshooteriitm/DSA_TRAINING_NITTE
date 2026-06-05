import logging

logging.basicConfig(
    level=logging.DEBUG,
    filename="app.log",
    filemode="a",# The 'w' mode means that the log file will be overwritten each time the program runs. If you want to append to the log file instead, you can use 'a' mode.
    format="%(name)s - %(levelname)s -  %(asctime)s -  %(filename)s - %(lineno)d - %(funcName)s  - %(message)s"
)

logging.debug("This is a debug message")
logging.info("This is an info message")
logging.warning("This is a warning message")
