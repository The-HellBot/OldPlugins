# Configs imports from here

import os

ENV = bool(os.environ.get("ENV", False))

if ENV:
    from hell_config import Config  # pylint: disable=import-configs
else:
    if os.path.exists("config.py"):
        from config import Development as Config  # pylint: disable=import-configs

# hellbot
