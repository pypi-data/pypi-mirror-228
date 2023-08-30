import os
import logging
import re


from rc.config import Config
from rc.exceptions import RcException

from rc.utils import run_command_on_subprocess

logger = logging.getLogger(__name__)

class DVCError(RcException):
    def __init__(self, msg):
        super().__init__(msg)
class DVC:
    def __init__(self, config:Config):
        self.CLOUD_STORAGE_DIR = config.get_config_value("cloud_storage_dir")
        self.CLOUD_STORAGE_BUCKET = config.get_config_value("bucket_name")
        self.CLOUD_STORAGE = config.get_config_value("cloud_storage")
        self.CLOUD_STORAGE_LOCATION = f"s3://{self.CLOUD_STORAGE_BUCKET}/{self.CLOUD_STORAGE_DIR}"
        self.MINIO_URL = config.get_config_value("minio_url")
        self.SECRET = config.get_config_value('minio_secret_key') if self.CLOUD_STORAGE == 'minio' else config.get_config_value('s3_storage_secret_key')
        self.ACCESS = config.get_config_value('minio_access_key') if self.CLOUD_STORAGE == 'minio' else config.get_config_value('s3_storage_access_key')

    def dvc_init_set_up_config(
            self,
            repo_name,
            tag
        ):
        try:
            run_command_on_subprocess("dvc init -f", repo_name)    
            run_command_on_subprocess(f"dvc remote add -d {self.CLOUD_STORAGE_BUCKET} {self.CLOUD_STORAGE_LOCATION}/{repo_name} -f", repo_name)   
            if self.CLOUD_STORAGE == 'minio':        
                run_command_on_subprocess(f"dvc remote modify {self.CLOUD_STORAGE_BUCKET} endpointurl {self.MINIO_URL}", repo_name)           
            run_command_on_subprocess(f"dvc remote modify {self.CLOUD_STORAGE_BUCKET} secret_access_key {self.SECRET}", repo_name)         
            run_command_on_subprocess(f"dvc remote modify {self.CLOUD_STORAGE_BUCKET} access_key_id {self.ACCESS}", repo_name)        
            run_command_on_subprocess("dvc config core.autostage true", repo_name)
            return True
        except Exception as exc:
            raise DVCError(exc)
        
    def dvc_pull(
            self,
            repo_name
        ):
        try:
            run_command_on_subprocess('dvc pull -f', repo_name)
            return True
        except Exception as exc:
            raise DVCError(exc)
    
    def dvc_status(self):
        try:
            res_str = run_command_on_subprocess(f"dvc status")    
            if re.search(r'(modified:)', res_str):
                return True  
            if re.search(r'(Data and pipelines are up to date)', res_str):
                return False
            if re.search(r'(There are no data or pipelines tracked in this project yet)', res_str):
                return False  
            return False
        except Exception as exc:
            raise DVCError(exc)
        

    def dvc_add(self, paths):
        from datetime import timedelta
        from timeit import default_timer as timer
        start = timer()
        from rc.dirs import is_dot_dvc_file_exist

        try:
            for path in paths:
                if is_dot_dvc_file_exist(path):
                    run_command_on_subprocess(f"dvc commit {path} -f")
                else:
                    run_command_on_subprocess(f"dvc add {path}")
                run_command_on_subprocess("git add {0}.dvc".format(path))
            logger.debug('DVC ADD TIME {0}'.format(timedelta(seconds=timer()-start)))
            return True
        except Exception as exc:
            raise DVCError(exc)


    def dvc_push(self, paths):
        from datetime import timedelta
        from timeit import default_timer as timer
        start = timer()
        from rc.dirs import is_dot_dvc_file_exist

        try:
            run_command_on_subprocess("dvc push {0}".format(' '.join(paths)))
            logger.debug('DVC PUSH TIME {0}'.format(timedelta(seconds=timer()-start)))
            return True
        except Exception as exc:
            raise DVCError(exc)


    def check_dvc_add_left(self):
        logger.debug("Check DVC ADD left")
        try:
            result = run_command_on_subprocess('dvc status') 
            if re.search(r'(modified:)', result):
                logger.debug("DVC ADD left")
                return True  
            logger.debug("Clean DVC ADD")
            return False
        except Exception as exc:
            raise DVCError(exc)
        

    def check_dvc_file_deleted(self):   
        logger.debug("Check DVC DELETED file")     
        try:
            result = run_command_on_subprocess('dvc status') 
            if re.search(r'(deleted:)', result):
                logger.debug("DVC DELETED file")
                return True  
            logger.debug("Clean DVC ADD")
        except Exception as exc:
            raise DVCError(exc)