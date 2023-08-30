import logging
import subprocess

from rc.exceptions import RcException

logger = logging.getLogger(__name__)

class SubProcessError(RcException):
    def __init__(self, msg):
        super().__init__(msg)

def run_command_on_subprocess(command, cwd=None, exception=True):
    logger.debug(command)
    kwargs = {
        "capture_output": True,
        "shell": True,
        "text":True,
        "cwd": cwd,
        "check":True
    } if cwd else {
        "capture_output": True,
        "shell": True,
        "text":True,
        "check":True
    }
    try:
        result = subprocess.run(command, **kwargs)
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()
        logger.debug("STD OUT: {}".format(stdout))
        logger.debug("STD ERR: {}".format(stderr))
        return stdout if stdout else stderr
    except subprocess.CalledProcessError as e:
        stdout = e.stdout
        stderr = e.stderr
        logger.debug("STD OUT: {}".format(stdout))
        logger.debug("STD ERR: {}".format(stderr))
        if exception:
            raise SubProcessError(f"command '{command}' failed with return code {e.returncode}")
        return stdout if stdout else stderr