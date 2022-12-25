import logging


logging.basicConfig(
    format="[%(asctime)s] [%(levelname)s] [%(name)s] : %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
)

LOGGER = logging.getLogger("HellBot")