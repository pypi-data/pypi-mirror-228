from typing import (
    TYPE_CHECKING
)
import logging

from rc.exceptions import (
    RcException,
    DirNotFound,
    GitExistError,
    RepoNameNotFound
)

if TYPE_CHECKING:
    from rc.repo import Repo
from rc.config import Config
from rc.entities.repos import RcRepo, RcRepoCommit
from rc.git import Git
from rc.dvc import DVC
from halo import Halo

logger = logging.getLogger(__name__)

def clone(
        repo: "Repo",
        repo_name, #name is equivalent of git branch name
        config: "Config",
        rc_repo: "RcRepo",
        rc_repo_commit: "RcRepoCommit",
        git: "Git",
        dvc: "DVC",
        sp: "Halo"
        ):
    from rc.dirs import is_dir_exit
    from rc import (
        REPO_DIR_EXIST,
        GIT_EXIST,
        REPO_NOT_FOUND,
    )

    if is_dir_exit(repo_name): raise DirNotFound(REPO_DIR_EXIST)
    
    path = git.is_git_initialized()
    if path: logger.debug(f"{GIT_EXIST} : PATH: {path}"); raise GitExistError(GIT_EXIST)

    if not rc_repo.remote: raise RepoNameNotFound(REPO_NOT_FOUND)

    if not git.does_git_remote_branch_exist(repo_name): raise RepoNameNotFound(REPO_NOT_FOUND)

    git.git_clone_and_check_out_repo_clone(repo_name, rc_repo_commit.commit_id, rc_repo.tag, rc_repo_commit.branch)
    dvc.dvc_pull(repo_name)
    sp.succeed(f"Successfully cloned '{repo_name}'")



