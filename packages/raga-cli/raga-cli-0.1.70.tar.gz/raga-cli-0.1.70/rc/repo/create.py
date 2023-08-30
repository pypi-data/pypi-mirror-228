from typing import (
    TYPE_CHECKING
)
import logging

from rc.exceptions import (
    RcException,
    DirNotFound,
    GitExistError,
    RepoNameAlreadyExist
)

if TYPE_CHECKING:
    from rc.repo import Repo
from rc.config import Config
from rc.entities.repos import RcRepo, RcRepoCommit
from rc.git import Git
from rc.dvc import DVC
from halo import Halo

logger = logging.getLogger(__name__)

def create(
        repo: "Repo",
        repo_name, #name is equivalent of git branch name
        tag,
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
        REPO_ALREADY_EXIST,
    )
    if is_dir_exit(repo_name): raise DirNotFound(REPO_DIR_EXIST)
        
    path = git.is_git_initialized()
    if path: logger.debug(f"{GIT_EXIST} : PATH: {path}"); raise GitExistError(GIT_EXIST)

    if rc_repo.remote: raise RepoNameAlreadyExist(REPO_ALREADY_EXIST)

    if git.does_git_remote_branch_exist(repo_name): raise RepoNameAlreadyExist(REPO_ALREADY_EXIST)

    git.git_clone_and_check_out_repo_creation(repo_name, tag)
    dvc.dvc_init_set_up_config(repo_name, tag)
    rc_repo.create_repository(git)
    git.git_commit_push(repo_name)
    if tag == "model":
        rc_repo_commit.create_repo_commit(commit_id=git.get_recent_commit_hash(repo_name))
    rc_repo.create_repo_lock()
    sp.succeed(f"Successfully created '{repo_name}'")



