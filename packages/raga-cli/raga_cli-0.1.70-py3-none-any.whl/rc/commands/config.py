import argparse
import logging
from rc.cli.command import CmdBase

logger = logging.getLogger(__name__)

class CmdGet(CmdBase):   
        
    def run(self):
       
        return 0


def add_parser(subparsers, parent_parser):
    REPO_HELP = "Get or set config options."

    config_parser = subparsers.add_parser(
        "config",
        parents=[parent_parser],
        description=REPO_HELP,
        help=REPO_HELP,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
   
    config_parser.set_defaults(func=CmdGet)