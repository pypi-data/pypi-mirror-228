import os

from . import env

DEFAULT_API_VERSION = "v1"

def api_version():
    return os.getenv(env.RC_API_VERSION) or DEFAULT_API_VERSION


