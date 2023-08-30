"""
RC
----
Make your data science projects reproducible and shareable.
"""
import rc.logger
from rc.build import PKG  # noqa: F401
from rc.version import __version__, version_tuple  # noqa: F401
from rc.env import *
from rc.error_messages import *
rc.logger.setup()
