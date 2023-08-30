import argparse
import logging
from rc.cli.command import CmdBase

logger = logging.getLogger(__name__)

class CmdGet(CmdBase):   
        
    def run(self):
        from rc.exceptions import RcException
        from rc.entities.repos import RcRepo, RcRepoCommit, RepoLock
        from rc.dirs import get_dir_name
        from halo import Halo
  
        repo_name = get_dir_name()
        try:   
            with Halo(text=f"Processing...", spinner='dots') as sp:  
                repo = RcRepo(self.config, repo_name)
                self.repo.get(
                        repo_name,
                        self.args.repo_version,
                        self.config,
                        repo,
                        RcRepoCommit(self.config, repo ,self.dvc, self.git),
                        RepoLock(self.config, repo_name),
                        self.git,
                        self.dvc,
                        sp
                        )                                
        except RcException:
            logger.exception("")
            return 1 
        return 0


def add_parser(subparsers, parent_parser):
    REPO_HELP = "Download files or directories tracked by RC"

    get_parser = subparsers.add_parser(
        "get",
        parents=[parent_parser],
        description=REPO_HELP,
        help=REPO_HELP,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    get_parser.add_argument(
        "-repo-version", 
        "--repo-version", 
        default=None,
        metavar="<int>",
        type=int,
        help="Download files or directories of particular repo version",
    )
    get_parser.set_defaults(func=CmdGet)