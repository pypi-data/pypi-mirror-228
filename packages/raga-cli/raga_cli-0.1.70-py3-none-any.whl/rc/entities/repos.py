import time
from rc.config import Config
from rc.api_client import APIClient, APIClientError
import logging
import os, pwd
import json
from halo import Halo


from rc.git import Git
from rc.dvc import DVC
# if TYPE_CHECKING:

logger = logging.getLogger(__name__)

class RcRepo:
    def __init__(self, config:Config, repo_name, tag=None):
        self.config = config
        response = self.get_repository(repo_name)
        self.remote = response.get("repo_name", False)
        self.repo_name = response.get("repo_name", repo_name)
        self.git_repo = response.get("git_repo", None)
        self.minio_repo = response.get("minio_repo", None)
        self.remote_storage_url = response.get("remote_storage_url", None)
        self.tag = response.get("tag", tag)
        self.created_at = response.get("created_at", None)
        self.created_by = response.get("created_by", None)
        self.updated_at = response.get("updated_at", None)

        self.CREATED_BY = pwd.getpwuid(os.getuid()).pw_name
        self.CLOUD_STORAGE_BUCKET = self.config.get_config_value("bucket_name")
        self.CLOUD_STORAGE_DIR = self.config.get_config_value("cloud_storage_dir")
        self.CLOUD_STORAGE_LOCATION = f"s3://{self.CLOUD_STORAGE_BUCKET}/{self.CLOUD_STORAGE_DIR}"


    def get_repository(self, repo_name):
        return self.make_request(end_point=f"repos-name?repoName={repo_name}", method="get", payload=None)
                
                
    def create_repository(self, git:Git):
        payload = json.dumps({
                    "repo_name":self.repo_name,
                    "tag":self.tag,
                    "created_by":self.CREATED_BY,
                    "git_repo":git.get_git_repo_url(self.repo_name).replace('\n', ''),
                    "remote_storage_url":f"{self.CLOUD_STORAGE_BUCKET}/{self.CLOUD_STORAGE_LOCATION}",
                })
        logger.debug(f"CREATE REPO PAYLOAD: {payload}")
        
        return self.make_request(end_point="repos", method="post", payload=payload)
    
                
    def create_repo_lock(self):
        payload = json.dumps({"repo_name":self.repo_name, "user_name":self.CREATED_BY, "locked":False})
        
        return self.make_request(end_point="repolock", method="post", payload=payload)
         
    def get_repo_commit(self):
        return self.make_request(end_point=f"repocommit/repo/{self.repo_name}", method="get", payload=None)
    
    def make_request(self, end_point, method, payload=None):
        with APIClient(self.config.get_core_config_value("rc_base_url")) as client:
            response_method = getattr(client, method.lower())
            response = response_method(end_point, data=payload)
            if response:
                data = response.json()
                data = data.get('data', None)
                if data:
                    logger.debug(f"RESPONSE DATA : {data}")
                    return data
                else:
                    return {}
            else:
                raise APIClientError(f"something went wrong")
            
class RepoLock:
    def __init__(self, config:Config, repo_name):
        self.config = config
        self.repo_name = repo_name
        response = self.get_repo_lock()
        self.locked = response.get("locked", False) 
        self.created_at = response.get("created_at", None) 
        self.user_name = response.get("user_name", None) 


    def get_repo_lock(self):
        return self.make_request(end_point=f"repolock?key={self.repo_name}", method="get", payload=None)
    

    def update_repo_lock(self, lock_value:bool=False):
        self.make_request(end_point=f"repolock/{self.repo_name}", method="put", payload=json.dumps({"locked":lock_value}))


    def set_repo_lock(self, stop_event, pool_time):
        logger.debug("START HTTP THREAD")
        while not stop_event.is_set():
            logger.debug("REPO LOCKING")
            self.make_request(end_point=f"repolock/{self.repo_name}", method="put", payload=json.dumps({"locked":True}))
            time.sleep(pool_time)


    def make_request(self, end_point, method, payload=None):
        with APIClient(self.config.get_core_config_value("rc_base_url")) as client:
            response_method = getattr(client, method.lower())
            response = response_method(end_point, data=payload)
            if response:
                data = response.json()
                data = data.get('data', None)
                if data:
                    logger.debug(f"RESPONSE DATA : {data}")
                    return data
                else:
                    return {}
            else:
                raise APIClientError(f"something went wrong")


class RcRepoCommit:
    def __init__(self, config:Config, repo:RcRepo, dvc:DVC, git:Git):
        self.config = config
        self.dvc = dvc
        self.git = git
        self.repo = repo
        self.repo_name = repo.repo_name
        response = self.get_repo_commit()
        self.commit_message = response.get("commit_message", None) 
        self.created_at = response.get("created_at", None) 
        self.dir_file = response.get("dir_file", None) 
        self.folder = response.get("folder", None)  
        self.updated_at = response.get("updated_at", None) 
        self.version = response.get("version", None) 
        self.commit_id = response.get("commit_id", None) 
        self.branch = response.get("branch", None) 
        self.check_elastic_process = response.get("check_elastic_process", None) 
        self.repo_type = response.get("repo_type", None) 
        self.GIT_INITIAL_COMMIT = self.config.get_config_value("git_initial_commit")

    def get_versions(self):
        return self.make_request(end_point=f"version-list/{self.repo_name}", method="get", payload=None) 


    def create_repo_commit(self,
                           commit_message=None, 
                           commit_id = None,
                           folder = None,
                           version=None,
                           dir_file = None,
                           branch=None
                           ):
        
        msg = commit_message if commit_message else self.GIT_INITIAL_COMMIT
        version = version if version else 0
        branch = branch if branch else self.repo_name
        payload = {
            'version':version,
            'commit_message':msg,
            'repo':self.repo_name
        }

        if branch: payload['branch'] = branch
        if dir_file: payload['dir_file'] = dir_file
        if commit_id: payload['commit_id'] = commit_id
        if folder: payload['folder'] = folder

        payload = json.dumps(payload)
        return self.make_request(end_point="repocommit", method="post", payload=payload) 
    

    def get_repo_commit(self):
        return self.make_request(end_point=f"repocommit/repo/{self.repo_name}", method="get", payload=None)
    
    def get_repo_commit_by_version(self, version):
        payload = json.dumps({"repo":self.repo.repo_name, "version":version})
        return self.make_request(end_point=f"repocommit/data", method="post", payload=payload)
    

    def get_version_by_commit_hash(self, git_commit_hash):
        return self.make_request(end_point=f"repocommit/commitId/{git_commit_hash}", method="get", payload=None)
    

    def get_repo_commit_by_id(self, id):
        return self.make_request(end_point=f"repocommit?key={id}", method="get", payload=None)
    
    def update_repo_commit_by_payload(self, payload):
        return self.make_request(end_point=f"repocommit/update/commitid", method="post", payload=payload)

    def get_commit_version(self, commit_id):
        res = self.make_request(end_point=f"repocommit/commitId/{commit_id}", method="get", payload=None)
        if "version" in res:
            return res["version"]
        return False


    def update_repo_commits(self, ids, message):
        from rc.utils.run_cli_cmd import run_command_on_subprocess

        if len(ids):
            run_command_on_subprocess("git commit -am '{}'".format(message), None, False)
            run_command_on_subprocess("git push", None, False)
            for id in ids:     
                commit_hash = self.git.get_recent_commit_hash()
                request_payload = {
                    "id" : id,
                    "commit_id":commit_hash,
                }   
                self.update_repo_commit_by_payload(json.dumps(request_payload))


    def server_repo_commit_status(self, ids):
        elastic_processes = []
        for id in ids:
            elastic_processes.append(self.get_repo_commit_by_id(id)['check_elastic_process'])
        logger.debug("ELASTIC PROCESS {}".format(elastic_processes))
        return all(elastic_processes)


    def get_current_version(self, paths = None):
        from rc.dirs import is_dot_dvc_file_exist
        if not paths:
            current_version = 0 if not self.version else int(self.version)
            return 1 if not current_version else current_version+1
        
        current_version = 0 if not self.version else int(self.version)
        for path in paths:
            if not is_dot_dvc_file_exist(path):
                return current_version+1
            if self.dvc.dvc_status():
                return current_version+1
        return 1 if not current_version else current_version


    def is_current_version_stable(self):
        commit_version_res = self.get_version_by_commit_hash(self.git.get_recent_commit_hash())
        if not "version" in commit_version_res:
            return True
        
        if not commit_version_res["version"] and not self.version:
            return True

        if commit_version_res["version"] == self.version:
            return True
        else:
            logger.debug("Local repo version is not stable")
            return False
    
    def download_commit(self, sp:Halo):
        from rc.utils.run_cli_cmd import run_command_on_subprocess
        repo_commit = self.get_repo_commit()
        
        run_command_on_subprocess('git reset --hard')
        run_command_on_subprocess('git reset --hard {0}'.format(repo_commit['commit_id']))
        if self.repo.tag == "model":
            run_command_on_subprocess('git checkout {0}'.format(repo_commit['branch']))
        run_command_on_subprocess('git clean -fd')
        sp.text="Downloading..."
        run_command_on_subprocess('dvc pull -f')

    def download_commit_by_version(self, repo_commit, sp:Halo):
        from rc.utils.run_cli_cmd import run_command_on_subprocess
        
        run_command_on_subprocess('git reset --hard')
        run_command_on_subprocess('git reset --hard {0}'.format(repo_commit['commit_id']))
        if self.repo.tag == "model":
            run_command_on_subprocess('git checkout {0}'.format(repo_commit['branch']))
        run_command_on_subprocess('git clean -fd')
        sp.text="Downloading..."
        run_command_on_subprocess('dvc pull -f')

    def make_request(self, end_point, method, payload=None):
        with APIClient(self.config.get_core_config_value("rc_base_url")) as client:
            response_method = getattr(client, method.lower())
            response = response_method(end_point, data=payload)
            if response:
                data = response.json()
                data = data.get('data', None)
                if data:
                    logger.debug(f"RESPONSE DATA : {data}")
                    return data
                else:
                    return {}
            else:
                raise APIClientError(f"something went wrong")