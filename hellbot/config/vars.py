# Configs imports from here

import os

ENV = bool(os.environ.get("ENV", False))

if ENV:
    pass
else:
    if os.path.exists("config.py"):
        pass

# hellbot
