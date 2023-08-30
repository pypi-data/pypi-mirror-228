import os

from . import env

DEFAULT_PROFILE = "default"

def config_profile():
    return os.getenv(env.RC_CONFIG_PROFILE) or DEFAULT_PROFILE
