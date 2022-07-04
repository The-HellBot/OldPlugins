# Configs imports from here

import os

if os.path.exists("config.py"):
    from config import Development as Config  # noqa
else:
    from .config import Config  # noqa


# hellbot
