import logging
from abc import ABC, abstractmethod

from rc.exceptions import RcException


logger = logging.getLogger(__name__)


class CmdBase(ABC):
    def __init__(self, args):
        from rc.repo import Repo
        from rc.config import Config
        from rc.git import Git
        from rc.dvc import DVC
        config = Config(profile=args.profile)
        self.repo: "Repo" = Repo()
        self.config: "Config" =  config
        self.git: "Git" =  Git(config)
        self.dvc: "DVC" =  DVC(config)
        self.args = args
    def do_run(self):
        return self.run()
            
    @abstractmethod
    def run(self):
        pass


