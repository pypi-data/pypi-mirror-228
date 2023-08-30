"""Helpers for other modules."""
import logging
import os
import re
from typing import Dict, List
from rc.utils.run_cli_cmd import *
import socket

import colorama

logger = logging.getLogger(__name__)


def colorize(message, color=None, style=None):
    """Returns a message in a specified color."""
    if not color:
        return message

    styles = {"dim": colorama.Style.DIM, "bold": colorama.Style.BRIGHT}

    colors = {
        "green": colorama.Fore.GREEN,
        "yellow": colorama.Fore.YELLOW,
        "blue": colorama.Fore.BLUE,
        "red": colorama.Fore.RED,
        "magenta": colorama.Fore.MAGENTA,
        "cyan": colorama.Fore.CYAN,
    }

    return "{style}{color}{message}{reset}".format(
        style=styles.get(style, ""),
        color=colors.get(color, ""),
        message=message,
        reset=colorama.Style.RESET_ALL,
    )


def boxify(message, border_color=None):
    """Put a message inside a box.

    Args:
        message (unicode): message to decorate.
        border_color (unicode): name of the color to outline the box with.
    """
    lines = message.split("\n")
    max_width = max(_visual_width(line) for line in lines)

    padding_horizontal = 5
    padding_vertical = 1

    box_size_horizontal = max_width + (padding_horizontal * 2)

    chars = {"corner": "+", "horizontal": "-", "vertical": "|", "empty": " "}

    margin = "{corner}{line}{corner}\n".format(
        corner=chars["corner"], line=chars["horizontal"] * box_size_horizontal
    )

    padding_lines = [
        "{border}{space}{border}\n".format(
            border=colorize(chars["vertical"], color=border_color),
            space=chars["empty"] * box_size_horizontal,
        )
        * padding_vertical
    ]

    content_lines = [
        "{border}{space}{content}{space}{border}\n".format(
            border=colorize(chars["vertical"], color=border_color),
            space=chars["empty"] * padding_horizontal,
            content=_visual_center(line, max_width),
        )
        for line in lines
    ]

    return "{margin}{padding}{content}{padding}{margin}".format(
        margin=colorize(margin, color=border_color),
        padding="".join(padding_lines),
        content="".join(content_lines),
    )


def _visual_width(line):
    """Get the the number of columns required to display a string"""

    return len(re.sub(colorama.ansitowin32.AnsiToWin32.ANSI_CSI_RE, "", line))


def _visual_center(line, width):
    """Center align string according to it's visual width"""

    spaces = max(width - _visual_width(line), 0)
    left_padding = int(spaces / 2)
    right_padding = spaces - left_padding

    return (left_padding * " ") + line + (right_padding * " ")


def relpath(path, start=os.curdir):
    path = os.path.abspath(os.fspath(path))
    start = os.path.abspath(os.fspath(start))

    # Windows path on different drive than curdir doesn't have relpath
    if os.name == "nt" and not os.path.commonprefix([start, path]):
        return path

    return os.path.relpath(path, start)


def as_posix(path: str) -> str:
    import ntpath
    import posixpath

    return path.replace(ntpath.sep, posixpath.sep)


def env2bool(var, undefined=False):
    """
    undefined: return value if env var is unset
    """
    var = os.getenv(var, None)
    if var is None:
        return undefined
    return bool(re.search("1|y|yes|true", var, flags=re.I))


def resolve_output(inp, out, force=False):
    from urllib.parse import urlparse

    name = os.path.basename(os.path.normpath(urlparse(inp).path))
    if not out:
        ret = name
    elif os.path.isdir(out):
        ret = os.path.join(out, name)
    else:
        ret = out

    if os.path.exists(ret) and not force:
        hint = "\nTo override it, re-run with '--force'."
        raise Exception(ret, hint=hint)

    return ret


def format_link(link):
    return "<{blue}{link}{nc}>".format(  # noqa: UP032
        blue=colorama.Fore.CYAN, link=link, nc=colorama.Fore.RESET
    )


def error_link(name):
    return format_link(f"https://raga.ai/{name}")


def error_handler(func):
    def wrapper(*args, **kwargs):
        onerror = kwargs.get("onerror", None)
        result = {}

        try:
            vals = func(*args, **kwargs)
            if vals:
                result["data"] = vals
        except Exception as e:  # noqa: BLE001, pylint: disable=broad-except
            if onerror is not None:
                onerror(result, e, **kwargs)
        return result

    return wrapper


def onerror_collect(result: Dict, exception: Exception, *args, **kwargs):
    logger.debug("", exc_info=True)
    result["error"] = exception


def errored_revisions(rev_data: Dict) -> List:
    from dvc.utils.collections import nested_contains

    result = []
    for revision, data in rev_data.items():
        if nested_contains(data, "error"):
            result.append(revision)
    return result

def is_internet_available(host="www.google.com", port=80, timeout=5):
    """
    Check if there is an active internet connection by trying to establish a socket connection.
    
    Args:
        host (str): The host to connect to (default is "www.google.com").
        port (int): The port to use for the connection (default is 80 for HTTP).
        timeout (int): The timeout for the connection attempt in seconds (default is 5 seconds).
        
    Returns:
        bool: True if the internet connection is available, False otherwise.
    """
    try:
        socket.create_connection((host, port), timeout=timeout)
        return True
    except OSError:
        pass
    return False
