import json
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# LAS Auth
LAS_USER = os.getenv("LAS_USER")
LAS_PWD = os.getenv("LAS_PWD")

# External Auth
EXT_USER = os.getenv("EXT_USER")
EXT_PWD = os.getenv("EXT_PWD")

POLLER_CLASS = os.getenv("POLLER_CLASS")
CONFIG = json.loads(os.getenv("CONFIG")) if os.getenv("CONFIG") else None
SECRETS = json.loads(os.getenv("SECRETS")) if os.getenv("SECRETS") else None
