import argparse
import logging

from rc import __version__
from rc.commands import (
    get,
    put,
    repo,
)

from . import RcParserError

logger = logging.getLogger(__name__)

COMMANDS = [
    repo,
    put,
    get,
]

def _find_parser(parser, cmd_cls):
    defaults = parser._defaults
    if not cmd_cls or cmd_cls == defaults.get("func"):
        parser.print_help()
        raise RcParserError

    actions = parser._actions
    for action in actions:
        if not isinstance(action.choices, dict):
            # NOTE: we are only interested in subparsers
            continue
        for subparser in action.choices.values():
            _find_parser(subparser, cmd_cls)

class RcParser(argparse.ArgumentParser):
    def error(self, message, cmd_cls=None):
        logger.error(message)
        _find_parser(self, cmd_cls)

    def parse_args(self, args=None, namespace=None):
        args, argv = self.parse_known_args(args, namespace)
        if argv:
            msg = "unrecognized arguments: %s"
            self.error(msg % " ".join(argv), getattr(args, "func", None))
        return args

def get_parent_parser():
    """Create instances of a parser containing common arguments shared among
    all the commands.

    When overwriting `-q` or `-v`, you need to instantiate a new object
    in order to prevent some weird behavior.
    """
    from rc._debug import add_debugging_flags
    from rc.profile import config_profile

    parent_parser = argparse.ArgumentParser(add_help=False)
    log_level_group = parent_parser.add_mutually_exclusive_group()
    log_level_group.add_argument(
        "-q", "--quiet", action="count", default=0, help="Be quiet."
    )
    log_level_group.add_argument(
        "-v", "--verbose", action="count", default=0, help="Be verbose."
    )
    parent_parser.add_argument(
        "--profile", metavar="<str>", default=config_profile(), help="Config profile (default).",
    )
    add_debugging_flags(parent_parser)

    return parent_parser

def get_main_parser():
    parent_parser = get_parent_parser()
    # Main parser
    desc = "Data Version Control using RC"
    parser = RcParser(
        prog="rc",
        description=desc,
        parents=[parent_parser],
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False,
    )

    # NOTE: We are doing this to capitalize help message.
    # Unfortunately, there is no easier and clearer way to do it,
    # as adding this argument in get_parent_parser() either in
    # log_level_group or on parent_parser itself will cause unexpected error.
    parser.add_argument(
        "-h",
        "--help",
        action="help",
        default=argparse.SUPPRESS,
        help="Show this help message and exit.",
    )

    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"rc version {__version__}",
        help="Show program's version.",
    )

    # Sub commands
    subparsers = parser.add_subparsers(
        title="Available Commands",
        metavar="COMMAND",
        dest="cmd",
        help="Use `rc COMMAND --help` for command-specific help.",
    )

    from .utils import fix_subparsers
    fix_subparsers(subparsers)

    for cmd in COMMANDS:
        cmd.add_parser(subparsers, parent_parser)

    return parser