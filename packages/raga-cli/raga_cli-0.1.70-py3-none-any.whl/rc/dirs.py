import os
import pathlib
import logging
from pathlib import Path


from rc.exceptions import RcException

from . import env

DEFAULT_CONFIG_DIR = ".raga"
logger = logging.getLogger(__name__)

class EmptyDirCheckError(RcException):
    def __init__(self, msg):
        super().__init__(msg)


class DVCFileNotFound(RcException):
    def __init__(self, msg):
        super().__init__(msg)

class DirFileNotFound(RcException):
    def __init__(self, msg):
        super().__init__(msg)

def app_config_dir():
    return os.getenv(env.RC_APP_CONFIG_DIR) or DEFAULT_CONFIG_DIR

def is_dir_exit(dir, cwd=None):
    if cwd:
        owd = os.getcwd()
        os.chdir(f"{owd}/{cwd}")
    current_dir = os.getcwd()
    folder_path = os.path.join(current_dir, dir)
    if cwd:
        os.chdir(owd)
    return os.path.exists(folder_path) and os.path.isdir(folder_path)

def get_dir_name(cwd = None):
    if cwd:
        owd = os.getcwd()
        os.chdir(f"{owd}/{cwd}") 
        repo_name =  os.path.basename(os.getcwd()) 
        os.chdir(owd)  
    else:
        repo_name =  os.path.basename(os.getcwd())
    return repo_name

def get_only_valid_dir(dir):
    if not dir.startswith("."):
        return True
    else:
        return False


def get_all_data_folder():
    directory = os.getcwd()
    dirs = next(os.walk(directory))[1]
    filtered = list(filter(get_only_valid_dir, dirs))
    return filtered

def valid_dot_dvc_with_folder(dirs):
    files = find_dvc_files()
    return match_and_delete_files(dirs, files)

def find_dvc_files():
    files = []
    cwd = os.getcwd()   # get the current working directory
    for file in os.listdir(cwd):   # iterate through the files in the current directory
        if file.endswith(".dvc") and not os.path.isdir(os.path.join(cwd, file)):   # check if the file has a .dvc extension and is not a directory
            files.append(os.path.join(cwd, file))
    return files

def match_and_delete_files(dir_list, file_list):
    dir_names = [os.path.basename(d) for d in dir_list]   # get the names of the directories in the first list
    deleted_files = []
    for file in file_list:   # iterate through the files in the second list
        filename = pathlib.Path(file).stem   # get the filename from the full path
        if filename not in dir_names:   # check if the filename is not in the list of directory names
            logger.debug(f"REMOVE DVC FILE : {filename}")
            os.remove(file)   # delete the file if it does not have a matching directory name
            deleted_files.append(file)
    return deleted_files

def get_non_empty_folders(folders):
    non_empty_folders = []

    for folder_path in folders:
        try:
            # Check if the folder exists
            if not os.path.exists(folder_path):
                logger.debug(f"Folder '{folder_path}' does not exist")
                continue

            # Check if the folder is empty
            is_empty = True
            for root, dirs, files in os.walk(folder_path):
                if files or dirs:
                    for file_name in files:
                        if not file_name.startswith('.'):  # Exclude hidden files
                            is_empty = False
                            break
                    if not is_empty:
                        break

            if not is_empty:
                non_empty_folders.append(folder_path)

        except OSError as e:
            raise EmptyDirCheckError(f"Error occurred while checking folder '{folder_path}': {e}")

    return non_empty_folders


def add_tmp_file(path):
    import random
    import string
    # Generate a random string
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    # Create a temporary file with the random string and .tmp extension
    temp_file_path = os.path.join(path, ".tmp")
    with open(temp_file_path, 'w') as temp_file:
        temp_file.write(random_string)

    return temp_file_path


def make_dir_alive(dirs):
    if len(dirs):
        for dir in dirs:
            add_tmp_file(dir)


def is_dot_dvc_file_exist(dir_path):
    dir_path = Path(f'{dir_path}.dvc')
    if dir_path.is_file():
        return True
    return False


def trim_slash(str):
    if str.endswith("/"):
        str = str.rsplit("/", 1)[0] 
    return str


def back_slash_trim(dirs):
    filtered = list(map(trim_slash, dirs))
    return filtered


def get_dir_file(path):
    dvc_file = Path(f'{path}.dvc')
    if not dvc_file.is_file():
        raise DVCFileNotFound("data version control file not found")
    dvc_read = open(dvc_file, "r")
    md5_dir = ''
    for line in dvc_read.readlines():
        if line.find('- md5') != -1:
            md5_dir = line.split(":")[-1].strip()
    if not md5_dir:
        raise DirFileNotFound(".dir file not found.")
    return md5_dir


def check_empty_dirs(dir):
    empty_dirs = []

    for root, dirs, files in os.walk(dir):
        # Exclude certain directories from traversal
        dirs[:] = [d for d in dirs if d not in (".rc", ".git")]

        if not dirs and not files:
            empty_dirs.append(os.path.basename(root))

    return empty_dirs

def check_root_folder():
    root_folder = '.'
    excluded_files = ['.rc', '.gitignore', '.git', '.dvcignore', ".DS_Store", "README.md"]
    excluded_extensions = ['.dvc', '.DS_Store']

    files = []
    for file in os.listdir(root_folder):
        if file not in excluded_files and not any(file.endswith(ext) for ext in excluded_extensions) and not os.path.isdir(os.path.join(root_folder, file)):
            files.append(file)

    return bool(files)