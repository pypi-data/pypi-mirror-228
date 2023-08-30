import argparse
import logging

from rc.cli.command import CmdBase
from rc.exceptions import RcException, InvalidArgumentError
from rc.entities.repos import RcRepo, RcRepoCommit
from halo import Halo

logger = logging.getLogger(__name__)

class RepoError(RcException):
    def __init__(self, msg):
        super().__init__(msg)
 

"""
----------------------------
***Repo Name Validation***
----------------------------
Bucket names should not contain upper-case letters
Bucket names should not contain underscores (_)
Bucket names should not end with a dash
Bucket names should be between 3 and 63 characters long
Bucket names cannot contain dashes next to periods (e.g., my-.bucket.com and my.-bucket are invalid)
Bucket names cannot contain periods - Due to our S3 client utilizing SSL/HTTPS, Amazon documentation indicates that a bucket name cannot contain a period, otherwise you will not be able to upload files from our S3 browser in the dashboard.
"""   

class CmdRepoCreate(CmdBase):
    def __init__(self, args): 
        super().__init__(args)

    def validate_args(self) -> None:
        args = self.args
        name = args.name.lower()
        # Check dash
        if '_' in name:
            raise InvalidArgumentError(f"Repository name contains invalid '_' characters.")

        # Check length requirements
        if len(name) < 3 or len(name) > 32:
            raise InvalidArgumentError("Repository names should be between 3 and 32 characters long")
        self.args.name = name
    

    def run(self): 
        try:
            self.validate_args()  
        except InvalidArgumentError:
            logger.exception("")
            return 1 
            
        try:       
            with Halo(text=f"Creating '{self.args.name}'...", spinner='dots') as sp:
                    repo = RcRepo(self.config, self.args.name, self.args.tag)
                    self.repo.create(
                        self.args.name,
                        self.args.tag,
                        self.config,
                        repo,
                        RcRepoCommit(self.config, repo, self.dvc, self.git),
                        self.git,
                        self.dvc,
                        sp
                        )                         
        except RcException:
            logger.exception("")
            return 1
        return 0

class CmdRepoClone(CmdBase):
    def run(self):
        try:       
            with Halo(text=f"Cloning into '{self.args.name}'...", spinner='dots') as sp:
                    repo = RcRepo(self.config, self.args.name)
                    self.repo.clone(
                        self.args.name,
                        self.config,
                        repo,
                        RcRepoCommit(self.config, repo, self.dvc, self.git),
                        self.git,
                        self.dvc,
                        sp
                        )                                         
        except RcException:
            logger.exception("")
            return 1
        return 0
    
class CmdRepoVersion(CmdBase):
    def run(self):
        with Halo(text=f"Processing...", spinner='dots') as sp:
            from rc.dirs import get_dir_name
            repo_name = get_dir_name()
            repo = RcRepo(self.config, repo_name)
            repo_commit = RcRepoCommit(self.config, repo, self.dvc, self.git)
            if self.args.list:
                data = repo_commit.get_versions()
                
                if repo.tag=="dataset":
                    print(f"{'Version':<10} {'Commit id':<40}{'Dir File':<40}{'Commit message':<20}")
                else:
                    print(f"{'Version':<10} {'Branch':<20}  {'Commit id':<40}{'Dir File':<40}{'Commit message':<20}")

                for commit in data:
                    commit_id = commit["commit_id"] if commit["commit_id"] else "N/A"
                    commit_message = commit["commit_message"] if commit["commit_message"] else "N/A"
                    version = commit["version"] if commit["version"] else "N/A"
                    dir_file = commit["dir_file"] if commit["dir_file"] else "N/A"
                    branch = ""
                    sp.stop()
                    if repo.tag=="model":
                        branch =  commit["branch"] if commit["branch"] else "N/A"
                        print(f"{version:<10} {branch:<20}    {commit_id:<40} {dir_file:<40}   {commit_message:<20}")
                    else:
                        print(f"{version:<10} {commit_id:<40} {dir_file:<40}   {commit_message:<40}")
            else:
                sp.stop()
                print(f"version: {repo_commit.get_version_by_commit_hash(self.git.get_recent_commit_hash())['version']}")
        return 0

class CmdRepoInfo(CmdBase):
    def run(self):
        with Halo(text=f"Processing...", spinner='dots') as sp:
            from rc.dirs import get_dir_name
            repo_name = get_dir_name()
            repo = RcRepo(self.config, repo_name)
            repo_commit = RcRepoCommit(self.config, repo, self.dvc, self.git)
            repo_commit_by_version = repo_commit.get_version_by_commit_hash(self.git.get_recent_commit_hash())
            sp.stop()
            print("Repository Information")
            print(f"Name: {repo_name}\nTag: {repo.tag}\nVersion: {repo_commit.version}\nLocal Version:{repo_commit_by_version['version']}")
        return 0

def add_parser(subparsers, parent_parser):
    REPO_HELP = "Manage repository."

    repo_parser = subparsers.add_parser(
        "repo",
        parents=[parent_parser],
        description=REPO_HELP,
        help=REPO_HELP,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    repo_parser_subparsers = repo_parser.add_subparsers(
        dest="cmd",
        help="Use `rc repo CMD --help` for command-specific help.",
    )
    
    REPO_CREATE_HELP = "Create a new repository."

    repo_create_parser = repo_parser_subparsers.add_parser(
        "create",
        parents=[parent_parser],
        description=REPO_HELP,
        help=REPO_CREATE_HELP,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    repo_create_parser.add_argument(
        "-n", 
        "--name", 
        required=True,
        metavar="<str>",
        help="Name of the repository",
    )

    repo_create_parser.add_argument(
        "-tag", 
        "--tag", 
        required=True,
        choices=['dataset', 'model'],
        help="Tag of the repository",
    )

    repo_create_parser.set_defaults(func=CmdRepoCreate)
    
    REPO_CLONE_HELP = "Clone repository."

    repo_clone_parser = repo_parser_subparsers.add_parser(
        "clone",
        parents=[parent_parser],
        description=REPO_HELP,
        help=REPO_CLONE_HELP,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    repo_clone_parser.add_argument(
        "-n", 
        "--name", 
        required=True,
        metavar="<str>",
        help="Name of the repository",
    )

    repo_clone_parser.set_defaults(func=CmdRepoClone)

    REPO_VERSION_HELP = "Show repository current local version."

    repo_version_parser = repo_parser_subparsers.add_parser(
        "version",
        parents=[parent_parser],
        description=REPO_HELP,
        help=REPO_VERSION_HELP,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    repo_version_parser.add_argument(
        "-list", 
        "--list", 
        action='store_true',
        default=False,
        help="List repository versions.",
    )

    repo_version_parser.set_defaults(func=CmdRepoVersion)

    REPO_INFO_HELP = "Show repository information."

    repo_info_parser = repo_parser_subparsers.add_parser(
        "info",
        parents=[parent_parser],
        description=REPO_HELP,
        help=REPO_INFO_HELP,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    repo_info_parser.set_defaults(func=CmdRepoInfo)
