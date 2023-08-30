import sys
import time
from typing import (
    TYPE_CHECKING
)
import threading
import logging
from halo import Halo

from rc.exceptions import (
    RootDirCheckForDatasetError,
    RepoCommitVersionNotFound
)

if TYPE_CHECKING:
    from rc.repo import Repo
from rc.config import Config
from rc.entities.repos import RcRepo, RcRepoCommit, RepoLock
from rc.git import Git
from rc.dvc import DVC
from rc.error_messages import *
from rc.dirs import *
  
logger = logging.getLogger(__name__)
stop_event = threading.Event()
REPO_COMMIT_IDS = []
POOL_TIME = 2
ES_POOL_TIME = 5

def get(
        repo: "Repo",
        repo_name, #name is equivalent of git branch name
        commit_version:None,
        config: "Config",
        rc_repo: "RcRepo",
        rc_repo_commit: "RcRepoCommit",
        rc_repo_lock: "RepoLock",
        git: "Git",
        dvc: "DVC",
        sp: "Halo"
        ):
    from rc.prompt import confirm

    if rc_repo.tag == "dataset" and check_root_folder(): raise RootDirCheckForDatasetError(FILE_IN_ROOT_DIR_DATASET)

    if commit_version:
        repo_commit = rc_repo_commit.get_repo_commit_by_version(commit_version)
        if not repo_commit:
             raise RepoCommitVersionNotFound(f"Version {commit_version} not found on server.")
        if not repo_commit['commit_id']:
            logger.debug("Commit Id not found on server. Please check the API response.")
            raise RepoCommitVersionNotFound(f"something went wrong.")
        sp.stop()
        if confirm("Are you sure you want to get it?"):
            common_validation(git, dvc, sp)
            sp.start()
            rc_repo_commit.download_commit_by_version(repo_commit, sp)        
    else:     
        common_validation(git, dvc, sp)
        sp.start()
        rc_repo_commit.download_commit(sp)
    sp.succeed("Successfully downloaded!")

def common_validation(git: Git, dvc:DVC, sp:Halo):
     if git.check_git_untrack_files() or git.check_git_uncommit_files() or git.check_git_deleted_files() or git.check_push_left() or dvc.dvc_status():
            sp.stop()
            input("Press Enter to continue (Untracked files will be deleted) or Ctrl + C to cancel...\n")