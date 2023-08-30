import logging
import sys
from typing import Optional



logger = logging.getLogger(__name__)

class RcParserError(Exception):
    """Base class for CLI parser errors."""
    def __init__(self):
        super().__init__("parser error")


def parse_args(argv=None):
    """Parses CLI arguments.

    Args:
        argv: optional list of arguments to parse. sys.argv is used by default.

    Raises:
        RcParserError: raised for argument parsing errors.
    """

    from .parser import get_main_parser
    parser = get_main_parser()
    args = parser.parse_args(argv)
    args.parser = parser
    return args


def _log_unknown_exceptions() -> None:
    from rc.info import get_rc_info
    from rc.ui import ui
    from rc.utils import colorize

    logger.exception("unexpected error")
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("Version info for developers:\n%s", get_rc_info())

    q = colorize("Having any troubles?", "yellow")
    link = colorize("https://info.raga.ai", "blue")
    footer = f"\n{q} Hit us up at {link}, we are always happy to help!"
    ui.error_write(footer)

def print_error(msg):
    from rc.ui import ui
    from rc.utils import colorize
    q = colorize(f"ERROR", "red")
    footer = f"{q}: {msg}"
    ui.error_write(footer)


def _log_exceptions(exc: Exception) -> Optional[int]:
    """Try to log some known exceptions, that are not DVCExceptions."""
    from rc.utils import error_link, format_link
    
    if isinstance(exc, OSError):
        import errno

        if exc.errno == errno.EMFILE:
            logger.exception(
                (
                    "too many open files, please visit "
                    "%s to see how to handle this problem"
                ),
                error_link("many-files"),
                extra={"tb_only": True},
            )
        else:
            _log_unknown_exceptions()
        return None

    _log_unknown_exceptions()
    return None


# def valid_requirement():
#     for tool in ['git']:
#         try:
#             subprocess.run([tool, '--version'], capture_output=True, text=True, check=True)
#         except OSError:
#             raise RctlError(f'rc: error: {tool} not found! Please install {tool}')


def main(argv=None):
    """Main entry point for rc CLI.

    Args:
        argv: optional list of arguments to parse. sys.argv is used by default.

    Returns:
        int: command's return code.
    """
    from rc._debug import debugtools
    from rc.config import ConfigError
    from rc.exceptions import RcException
    from rc.commands.repo import RepoError
    from rc.logger import set_loggers_level
    from rc.utils import is_internet_available

    # NOTE: stderr/stdout may be closed if we are running from rc.daemon.
    # On Linux we directly call cli.main after double forking and closing
    # the copied parent's standard file descriptors. If we make any logging
    # calls in this state it will cause an exception due to writing to a closed
    # file descriptor.
    if sys.stderr.closed:  # pylint: disable=using-constant-test
        logging.disable()
    elif sys.stdout.closed:  # pylint: disable=using-constant-test
        logging.disable(logging.INFO)

    args = None

    outer_log_level = logger.level
    try:
        args = parse_args(argv)
        level = None
        if args.quiet:
            level = logging.CRITICAL
        elif args.verbose == 1:
            level = logging.DEBUG
        elif args.verbose > 1:
            level = logging.TRACE  # type: ignore[attr-defined]

        if level is not None:
            set_loggers_level(level)

        if level and level <= logging.DEBUG:
            from platform import platform, python_implementation, python_version

            from rc import PKG, __version__

            pyv = f"{python_implementation()} {python_version()}"
            pkg = f" ({PKG})" if PKG else ""
            logger.debug("v%s%s, %s on %s", __version__, pkg, pyv, platform())
            logger.debug("command: %s", " ".join(argv or sys.argv))

        logger.trace(args)  # type: ignore[attr-defined]
        if not sys.stdout.closed and not args.quiet:
            from rc.ui import ui
            ui.enable()
        if not is_internet_available():
            raise RcException("No Internet.")
        with debugtools(args):
            cmd = args.func(args)
            ret = cmd.do_run()
    except ConfigError as exc:
        logger.exception("configuration error")
        ret = 251
    except KeyboardInterrupt:
        logger.exception("interrupted by the user")
        ret = 252
    except BrokenPipeError:
        import os

        # Python flushes standard streams on exit; redirect remaining output
        # to devnull to avoid another BrokenPipeError at shutdown
        # See: https://docs.python.org/3/library/signal.html#note-on-sigpipe
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
        ret = 141  # 128 + 13 (SIGPIPE)
    except RepoError as exc:
        logger.error(exc)
        ret = 200
    except RcException:
        ret = 255
        logger.exception("")
    except RcParserError:
        ret = 254
    except Exception as exc:  # noqa: BLE001, pylint: disable=broad-except
        # pylint: disable=no-member
        ret = _log_exceptions(exc) or 255
        
    try:
        # print(ret)
        # from rc import analytics

        # # if analytics.is_enabled():
        # analytics.collect_and_send_report(args, ret)

        return ret
    finally:
        logger.setLevel(outer_log_level)
    
