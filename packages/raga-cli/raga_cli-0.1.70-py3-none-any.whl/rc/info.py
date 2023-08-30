import platform

from rc import PKG, __version__

package = "" if PKG is None else f" ({PKG})"


def get_rc_info():
    rc_version = f"RC version: {__version__}{package}"
    info = [
        rc_version,
        "-" * len(rc_version),
        f"Platform: Python {platform.python_version()} on {platform.platform()}",
    ]
    return "\n".join(info)

