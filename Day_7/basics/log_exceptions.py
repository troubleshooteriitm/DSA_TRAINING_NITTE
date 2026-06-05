

import logging

logging.basicConfig(
    level=logging.DEBUG
)

try:
    result = 10 / 0
except ZeroDivisionError as e:
    logging.error("An error occurred: %s", e)

print("I am gonna be the King of Pirates!!!")