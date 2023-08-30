import logging
import os
import json
import time
import pathlib
from datetime import datetime
from rc.config import Config
from rc.entities.repos import RcRepoCommit

logger = logging.getLogger(__name__)


def fix_subparsers(subparsers):
    """Workaround for bug in Python 3. See more info at:
    https://bugs.python.org/issue16308

    Args:
        subparsers: subparsers to fix.
    """
    subparsers.required = True
    subparsers.dest = "cmd"


def append_doc_link(help_message, path):
    from rc.utils import format_link

    if not path:
        return help_message
    doc_base = "https://exe.com/"
    return f"{help_message}\nDocumentation: {format_link(doc_base + path)}"


def hide_subparsers_from_help(subparsers):
    # metavar needs to be explicitly set in order to hide subcommands
    # from the 'positional arguments' choices list
    # see: https://bugs.python.org/issue22848
    # Need to set `add_help=False`, but avoid setting `help`
    # (not even to `argparse.SUPPPRESS`).
    # NOTE: The argument is the parent subparser, not the subcommand parser.
    cmds = [cmd for cmd, parser in subparsers.choices.items() if parser.add_help]
    subparsers.metavar = "{{{}}}".format(",".join(cmds))
                   
    
def path_to_dict(path, is_full_path=False):
    if not os.path.exists(path):
        return None

    name = os.path.basename(path)
    if name == ".rc" or name == ".git" or name == ".DS_Store" or name == ".dvc" or name == ".gitignore" or name == ".dvcignore" or name == "model.dvc":
        return None

    d = {'name': name}
    if is_full_path:
        current_path = os.getcwd()
        full_path = os.path.join(current_path, path)
        d['full_path'] = full_path

    if os.path.isdir(path):
        d['type'] = "directory"
        children = []
        for filename in os.listdir(path):
            child_path = os.path.join(path, filename)
            child_dict = path_to_dict(child_path, is_full_path)
            if child_dict is not None:
                children.append(child_dict)
        if children:  # Only add children if there are any non-empty directories or files
            d['children'] = children
        else:
            return None
    else:
        d['type'] = "file"
        d['last_updated'] = datetime.fromtimestamp(os.path.getmtime(path)).strftime('%Y-%m-%d %H:%M:%S')

    return d


def upload_model_file_list_json(commit_id, config_manager: Config, rc_repo_commit:RcRepoCommit, cwd = None):
    if cwd:
        owd = os.getcwd()
        os.chdir(f"{owd}/{cwd}") 
    logger.debug("MODEL FILE UPLOADING")
    model_file_list = json.loads(json.dumps(path_to_dict('.')))
    CLOUD_STORAGE = config_manager.get_config_value('cloud_storage')
    CLOUD_STORAGE_BUCKET = config_manager.get_config_value('bucket_name')
    CLOUD_STORAGE_DIR = config_manager.get_config_value('cloud_storage_dir')

    SECRET = config_manager.get_config_value('minio_secret_key') if CLOUD_STORAGE == 'minio' else config_manager.get_config_value('s3_storage_secret_key')
    ACCESS = config_manager.get_config_value('minio_access_key') if CLOUD_STORAGE == 'minio' else config_manager.get_config_value('s3_storage_access_key')

    MINIO_URL = config_manager.get_config_value('minio_url')
    repo = rc_repo_commit.repo.repo_name
    dest = f"{CLOUD_STORAGE_DIR}/{repo}/model_files/{commit_id}.json"
    json_file = f'{commit_id}.json'
    with open(json_file, 'w', encoding='utf-8') as cred:    
        json.dump(model_file_list, cred, ensure_ascii=False, indent=4)  

    import botocore.session   

    session = botocore.session.Session()
    session.set_credentials(ACCESS, SECRET)
    
    if CLOUD_STORAGE == 'minio':
        s3 = session.create_client('s3', endpoint_url=MINIO_URL)
    else:
        s3 = session.create_client('s3')

    with open(json_file, 'rb') as file:
        s3.put_object(Bucket=CLOUD_STORAGE_BUCKET, Key=dest, Body=file) 
    
    pathlib.Path(json_file).unlink(missing_ok=True)
    if cwd:
        os.chdir(owd) 
    logger.debug("MODEL FILE UPLOADED")
    return 1

    
def retry(ExceptionToCheck, tries=4, delay=3, backoff=2):
    """
    Retry calling the decorated function using an exponential backoff.

    Args:
        ExceptionToCheck (Exception): the exception to check. When an exception of this type is raised, the function will be retried.
        tries (int): number of times to try before giving up.
        delay (int): initial delay between retries in seconds.
        backoff (int): backoff multiplier (e.g. value of 2 will double the delay each retry).

    Example Usage:
    ```
    @retry(Exception, tries=4, delay=3, backoff=2)
    def test_retry():
        # code to retry
    ```
    """
    logger.debug("RETRYING")
    def deco_retry(f):
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck as e:
                    print(f"Got exception '{e}', retrying in {mdelay} seconds...")
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)
        return f_retry
    return deco_retry


