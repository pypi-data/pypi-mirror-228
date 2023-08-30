import sys
import time
from typing import (
    TYPE_CHECKING
)
import threading
import logging
from halo import Halo

from rc.exceptions import (
    RcException,
    DirNotFound,
    GitExistError,
    RepoNameNotFound,
    DataDirNotFound,
    GitBranchNotMatchRepoName,
    RepoLocked,
    RepoPutError,
    RepoLocalVersionNotStable,
    GitUntrackError,
    RootDirCheckForDatasetError,
)

if TYPE_CHECKING:
    from rc.repo import Repo
from rc.config import Config
from rc.entities.repos import RcRepo, RcRepoCommit, RepoLock
from rc.git import Git
from rc.dvc import DVC
from rc.cli.utils import retry, upload_model_file_list_json
from rc.error_messages import *
from rc.dirs import *

logger = logging.getLogger(__name__)
stop_event = threading.Event()
REPO_COMMIT_IDS = []
POOL_TIME = 2
ES_POOL_TIME = 5

def put(
        repo: "Repo",
        repo_name, #name is equivalent of git branch name
        message,
        config: "Config",
        rc_repo: "RcRepo",
        rc_repo_commit: "RcRepoCommit",
        rc_repo_lock: "RepoLock",
        git: "Git",
        dvc: "DVC",
        sp: "Halo"
        ):
    
    
    if not rc_repo.remote: raise RepoNameNotFound(f"{REPO_NOT_FOUND_PUT} '{repo_name}'.")

    data_dirs = get_all_data_folder()
    if rc_repo.tag == "dataset" and not data_dirs: raise DataDirNotFound(DATA_DIR_NOT_FOUND_PUT)

    current_branch = git.get_current_branch()
    if rc_repo.tag == "dataset" and not (repo_name == current_branch): raise GitBranchNotMatchRepoName(f"{GIT_BRANCH_NOT_MATCH_REPO_NAME}.\nrepo: '{repo_name}' \nbranch: '{current_branch}'\nuse: git checkout {repo_name}")

    if rc_repo_lock.locked: raise RepoLocked(f"{REPO_LOCKED}")

    if rc_repo.tag == "dataset":
        if rc_repo.tag == "dataset" and check_root_folder(): raise RootDirCheckForDatasetError(FILE_IN_ROOT_DIR_DATASET)
        data_dirs = back_slash_trim(get_non_empty_folders(data_dirs))
        
        if not data_dirs: raise DataDirNotFound(DATA_DIR_NOT_FOUND_PUT)
        make_dir_alive(valid_dot_dvc_with_folder(data_dirs))
        current_version = rc_repo_commit.get_current_version(data_dirs)
        
        if not rc_repo_commit.is_current_version_stable():
             raise RepoLocalVersionNotStable(LOCAL_VERSION_NOT_STABLE)

        if not check_untrack_file(git, dvc):
            sp.info("There are no changes since last update.")
            return 1
            
        #Start Dataset Thread
        dataset_thread(
                        dvc,
                        rc_repo_commit,
                        rc_repo_lock,
                        data_dirs,
                        message,
                        current_version,
                        sp
                       )
       
    if rc_repo.tag == "model":
        extension_validation()
        if git.check_git_untrack_files() or git.check_git_uncommit_files() or git.check_git_deleted_files():
            raise GitUntrackError(GIT_UNTRACK_FILE)
        if git.check_branch_upstream():
            raise GitUntrackError(f"RC is not able to track git push. Please configure upstream for branch {git.get_current_branch()}.\nUse 'git push --set-upstream origin {git.get_current_branch()}'")
        if git.check_push_left():
            raise GitUntrackError(GIT_UNTRACK_FILE)
        current_version = rc_repo_commit.get_current_version()
        commit_hash = git.get_recent_commit_hash()
        checked_dirs = check_empty_dirs(os.getcwd())
        if checked_dirs:
            sp.warn(f"Empty directory found - '{','.join(checked_dirs)}'")
            sp.start("Processing...")
        if rc_repo_commit.get_commit_version(commit_hash) and not dvc.dvc_status():
            sp.info("There are no changes since last update.")
            return 1
        model_thread(
                    dvc,
                    git,
                    config,
                    rc_repo_commit,
                    rc_repo_lock,
                    message,
                    current_version,
                    sp
                    )

    sp.succeed("Successfully uploaded!")


@retry(Exception, tries=4, delay=3, backoff=2)
def dataset_upload(
     dvc: DVC,
     rc_repo_commit:RcRepoCommit,
     paths, 
     message,  
     current_version,
     sp:Halo
     ):
    sp.text = "Uploading..."
    dvc.dvc_add(paths)
    dvc.dvc_push(paths)

    for path in paths:
        md5_dir = get_dir_file(path)            
        commit_id = rc_repo_commit.create_repo_commit(
            commit_message=message,
            version=current_version,
            dir_file=md5_dir,
            folder=path
            )
        REPO_COMMIT_IDS.append(commit_id['id'])

    stop_checking_elastic_process = False
    while not stop_checking_elastic_process:
        stop_checking_elastic_process = rc_repo_commit.server_repo_commit_status(REPO_COMMIT_IDS)
        if not stop_checking_elastic_process:
            time.sleep(ES_POOL_TIME)
    return 1


@retry(Exception, tries=4, delay=3, backoff=2)
def model_upload(dvc:DVC, git:Git, rc_repo_commit:RcRepoCommit, rc_repo_lock: RepoLock,message, current_version, sp:Halo):
    MODEL_DIR = "model"
    sp.text = "Uploading..."
    dvc.dvc_add([MODEL_DIR])
    dvc.dvc_push([MODEL_DIR])
    md5_dir = get_dir_file(MODEL_DIR)    
    branch = git.get_current_branch()      
    commit_id = rc_repo_commit.create_repo_commit(
        commit_message=message,
        version=current_version,
        dir_file=md5_dir,
        folder=MODEL_DIR,
        branch=branch
        )
    REPO_COMMIT_IDS.append(commit_id['id'])
    stop_checking_elastic_process = False
    while not stop_checking_elastic_process:
        stop_checking_elastic_process = rc_repo_commit.server_repo_commit_status(REPO_COMMIT_IDS)
        if not stop_checking_elastic_process:
            time.sleep(ES_POOL_TIME)
    return 1


def dataset_thread(dvc:DVC, rc_repo_commit:RcRepoCommit, rc_repo_lock: RepoLock, data_dirs, message, current_version, sp:Halo):
    # Create a thread for making an HTTP request
        http_thread = threading.Thread(target=rc_repo_lock.set_repo_lock, args=(stop_event,POOL_TIME))
        http_thread.start()

        try:
            if dataset_upload(dvc, rc_repo_commit, data_dirs, message, current_version, sp):
                # Set the stop event
                stop_event.set()
                rc_repo_lock.update_repo_lock(False)
                rc_repo_commit.update_repo_commits(REPO_COMMIT_IDS, message)
                # Wait for both threads to finish
                http_thread.join()
            else:
                # Set the stop event
                stop_event.set()
                rc_repo_lock.update_repo_lock(False)
                # Wait for both threads to finish
                http_thread.join()
        except Exception as exc:
            # Set the stop event
            stop_event.set()
            rc_repo_lock.update_repo_lock(False)
            # Wait for both threads to finish
            http_thread.join()
            raise RepoPutError(exc)
        return 1


def model_thread(dvc:DVC, git:Git, config:Config, rc_repo_commit:RcRepoCommit, rc_repo_lock: RepoLock, message, current_branch, sp:Halo):
    # Create a thread for making an HTTP request
        http_thread = threading.Thread(target=rc_repo_lock.set_repo_lock, args=(stop_event,POOL_TIME))
        http_thread.start()

        try:
            if model_upload(dvc, git, rc_repo_commit, rc_repo_lock, message, current_branch, sp):
                # Set the stop event
                stop_event.set()
                rc_repo_lock.update_repo_lock(False)
                rc_repo_commit.update_repo_commits(REPO_COMMIT_IDS, message)
                upload_model_file_list_json(git.get_recent_commit_hash(), config, rc_repo_commit)
                # Wait for both threads to finish
                http_thread.join()
            else:
                # Set the stop event
                stop_event.set()
                rc_repo_lock.update_repo_lock(False)
                # Wait for both threads to finish
                http_thread.join()
        except Exception as exc:
            # Set the stop event
            stop_event.set()
            rc_repo_lock.update_repo_lock(False)
            # Wait for both threads to finish
            http_thread.join()
            raise RepoPutError(exc)
        return 1

def check_untrack_file(git:Git, dvc:DVC):
     if not git.check_git_untrack_files() and not git.check_git_uncommit_files() and not dvc.check_dvc_file_deleted() and not git.check_git_deleted_files() and not dvc.check_dvc_add_left():
        return False
     else:
         return True
     

def extension_validation(extensions=["requirements.txt", ".pth"]):
    found_extensions = set()
    for extension in extensions:
        extension_found = False
        for subdir, dirs, filenames in os.walk("."):
            for filename in filenames:
                if filename.endswith(extension):
                    found_extensions.add(extension)
                    extension_found = True
                    break
            if extension_found:
                break
        if not extension_found:
            raise RepoPutError(f"{extension} file not found.")
    return True