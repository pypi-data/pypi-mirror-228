import argparse
import logging

from rc.cli.command import CmdBase
from rc.exceptions import RcException

logger = logging.getLogger(__name__)

class PutError(RcException):
    def __init__(self, msg):
        super().__init__(msg)


class CmdPut(CmdBase):
    def validate_args(self) -> None:
        from rc.exceptions import InvalidArgumentError

        args = self.args
        if not getattr(args, "message", None):
            raise InvalidArgumentError("the following argument is required: -m/--message and make can not be empty.")      

    def run(self):  
        from rc.exceptions import RcException, InvalidArgumentError
        from rc.entities.repos import RcRepo, RcRepoCommit, RepoLock
        from rc.git import Git
        from rc.dirs import get_dir_name
        from rc.dvc import DVC
        from halo import Halo
        try:
            self.validate_args()
        except InvalidArgumentError:
            logger.exception("")
            return 1 
        repo_name = get_dir_name()
        try:   
            with Halo(text=f"Processing...", spinner='dots') as sp:  
                git = Git(self.config)
                dvc = DVC(self.config)
                repo = RcRepo(self.config, repo_name)
                self.repo.put(
                        repo_name,
                        self.args.message,
                        self.config,
                        repo,
                        RcRepoCommit(self.config, repo,dvc, git),
                        RepoLock(self.config, repo_name),
                        git,
                        dvc,
                        sp
                        )                                
        except RcException:
            logger.exception("")
            return 1 
        return 0


def add_parser(subparsers, parent_parser):
    REPO_HELP = "Upload tracked files or directories to remote storage and create a checkpoint."

    put_parser = subparsers.add_parser(
        "put",
        parents=[parent_parser],
        description=REPO_HELP,
        help=REPO_HELP,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    put_parser.add_argument(
        "-m", 
        "--message", 
        metavar="<text>", 
        help="Commit message",
    )
     
    
    put_parser.set_defaults(func=CmdPut)
