import os
import logging
import re

from rc.config import Config
from rc.exceptions import RcException

from rc.utils import run_command_on_subprocess

logger = logging.getLogger(__name__)

class GitError(RcException):
    def __init__(self, msg):
        super().__init__(msg)

class Git:
    def __init__(self, config:Config):
        self.GH_TOKEN = config.get_config_value("gh_token")
        self.GIT_ORG = config.get_config_value("git_org")
        self.GIT_COMMON_REPO = config.get_config_value("repo_name")
        self.INITIAL_COMMIT = config.get_config_value("git_initial_commit")
        self.GIT_IGNORED_EXES = config.get_config_value("gitignored_extensions")

    def is_git_initialized(self, directory_path=os.getcwd()):
        while directory_path != "/":
            git_directory = os.path.join(directory_path, ".git")
            if os.path.exists(git_directory) and os.path.isdir(git_directory):
                return directory_path
            directory_path = os.path.dirname(directory_path)
        return None


    def does_git_remote_branch_exist(
            self,
            branch_name
            ):
        
        remote_url = f"https://{self.GH_TOKEN}@github.com/{self.GIT_ORG}/{self.GIT_COMMON_REPO}.git"
        res_str = run_command_on_subprocess(f"git ls-remote --heads {remote_url} {branch_name}")
        return bool(res_str.strip())


    def fetch_all_git_branch(
            self,
            cwd=None
            ):
        try:
            command = "git branch -r"
            if cwd:
                result = run_command_on_subprocess(command=command, cwd=cwd)
            else:
                result = run_command_on_subprocess(command=command)
            
            branches = result.strip().splitlines()
            
            for branch in branches:
                if "->" not in branch:
                    self.checkout_branch(branch.strip(), cwd)
        except Exception as exc:
            raise GitError(exc)


    def checkout_branch(
            self, 
            branch, 
            cwd=None
            ):
        try:
            command = f"git checkout --track {branch}"
            if cwd:
                run_command_on_subprocess(command=command, cwd=cwd, exception=False)
            else:
                run_command_on_subprocess(command=command, exception=False)
        except Exception as exc:
            raise GitError(exc)

    def get_git_repo_url(swlf, repo):
        return run_command_on_subprocess(command="git config --get remote.origin.url", cwd=repo)


    def git_clone_and_check_out_repo_creation(
            self,
            repo_name,
            tag
            ): 
        try:
            run_command_on_subprocess(f"mkdir {repo_name}") 
            run_command_on_subprocess(f"git clone https://{self.GH_TOKEN}@github.com/{self.GIT_ORG}/{self.GIT_COMMON_REPO}.git .", repo_name)
            run_command_on_subprocess(f"git checkout -b {repo_name}", repo_name)
            self.fetch_all_git_branch(repo_name)
            run_command_on_subprocess(f"git checkout {repo_name}", repo_name)
            if tag == "model": 
                GIT_IGNORED_EXES = self.GIT_IGNORED_EXES.split(",")
                for extension in GIT_IGNORED_EXES:
                    run_command_on_subprocess(f"echo *{extension} >> .gitignore", repo_name)
                run_command_on_subprocess(f"mkdir model", repo_name) 
                run_command_on_subprocess(f"echo /model >> .gitignore", repo_name) 
                run_command_on_subprocess("touch README.md", repo_name)      
                run_command_on_subprocess("git add README.md", repo_name)
                run_command_on_subprocess("git add .gitignore", repo_name)
            return True
        except Exception as exc:
            raise GitError(exc)
        
    def git_clone_and_check_out_repo_clone(
            self,
            repo_name,
            commit_id,
            tag,
            branch
            ): 
        from rc.dirs import is_dir_exit
        try:
            run_command_on_subprocess(f"mkdir {repo_name}") 
            run_command_on_subprocess(f"git clone https://{self.GH_TOKEN}@github.com/{self.GIT_ORG}/{self.GIT_COMMON_REPO}.git .", repo_name)
            self.fetch_all_git_branch(repo_name)
            run_command_on_subprocess(f"git checkout {repo_name}", repo_name)
            if tag == "model":
                if not is_dir_exit("model",repo_name):
                    run_command_on_subprocess(f"mkdir model", repo_name)
                run_command_on_subprocess(f"git checkout {branch}", repo_name)
            run_command_on_subprocess('git reset --hard', repo_name)
            if commit_id:
                run_command_on_subprocess(f'git reset --hard {commit_id}', repo_name)
            run_command_on_subprocess('git clean -fd', repo_name)
            return True
        except Exception as exc:
            raise GitError(exc)
        
    def git_commit_push(
            self,
            repo_name
            ):
        try:
            run_command_on_subprocess(f"git commit -m '{self.INITIAL_COMMIT}' -a", repo_name)    
            run_command_on_subprocess(f"git branch -M {repo_name}", repo_name)    
            run_command_on_subprocess(f"git push --set-upstream origin {repo_name}", repo_name)
        except Exception as exc:
            raise GitError(exc)

    def get_recent_commit_hash(self, cwd = None):
        try:
            if cwd:
                result = run_command_on_subprocess('git rev-parse HEAD', cwd=cwd)
            else:
                result = run_command_on_subprocess('git rev-parse HEAD')
            logger.debug(f"COMMIT HASH: {result.strip()}")
            return result.strip()
        except Exception as exc:
                raise GitError(exc)
    
    def get_current_branch(self, cwd = None):
        try:
            if cwd:
                result = run_command_on_subprocess('git rev-parse HEAD', cwd=cwd)
            else:
                result = run_command_on_subprocess('git rev-parse --abbrev-ref HEAD')
            logger.debug(f"COMMIT HASH: {result.strip()}")
            return result.strip()
        except Exception as exc:
                raise GitError(exc)
    
    def check_git_untrack_files(self):
        try:
            logger.debug("Check GIT UNTRACK file")
            result = run_command_on_subprocess('git status')    
            
            if re.search(r'(Untracked files:)', result):
                return True    
            logger.debug("Clean UNTRACK file")
            return False
        except Exception as exc:
                raise GitError(exc)
    
    def check_git_uncommit_files(self):
        try:
            logger.debug("Check GIT UNCOMMIT file")
            result = run_command_on_subprocess('git status')
            if re.search(r'(Changes to be committed:)', result):
                return True  
            logger.debug("Clean UNCOMMIT file")
            return False
        except Exception as exc:
                raise GitError(exc)
    
    def check_git_deleted_files(self):
        try:
            logger.debug("Check GIT DELETED file")
            result = run_command_on_subprocess('git status')    
            if re.search(r'(Changes not staged for commit:)', result):
                return True  
            logger.debug("Clean DELETED file")
            return False
        except Exception as exc:
                raise GitError(exc)
        
    def check_push_left(self):
        try:
            logger.debug("Check PUSH left")
            result = run_command_on_subprocess('git status')    
            if re.search(r'(use "git push" to publish your local commits)', result):
                return True  
            logger.debug("Clean PUSH")
            return False
        except Exception as exc:
                raise GitError(exc)
        
    def check_branch_upstream(self):
        try:
            logger.debug("Check PUSH left")
            result = run_command_on_subprocess(f'git rev-parse --abbrev-ref {self.get_current_branch()}@{{upstream}}', None, False)    
            if re.search(r'(no upstream configured for branch)', result):
                return True  
            logger.debug("Clean PUSH")
            return False
        except Exception as exc:
                raise GitError(exc)