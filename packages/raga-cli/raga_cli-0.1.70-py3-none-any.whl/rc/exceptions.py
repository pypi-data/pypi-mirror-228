
class RcException(Exception):
    """Base class for all rc exceptions."""

    def __init__(self, msg, *args):
        assert msg
        self.msg = f"rc: {msg}"
        super().__init__(msg, *args)


class InvalidArgumentError(ValueError, RcException):
    """Thrown if arguments are invalid."""

    def __init__(self, msg, *args):
        self.msg = msg
        super().__init__(msg, *args)


class DirNotFound(RcException):
    pass

class GitExistError(RcException):
    pass

class RepoNameAlreadyExist(RcException):
    pass

class RepoNameNotFound(RcException):
    pass

class DataDirNotFound(RcException):
    pass

class GitBranchNotMatchRepoName(RcException):
    pass

class RepoLocked(RcException):
    pass

class RepoPutError(RcException):
    pass

class RepoLocalVersionNotStable(RcException):
    pass

class GitUntrackError(RcException):
    pass

class RepoCommitVersionNotFound(RcException):
    pass

class RootDirCheckForDatasetError(RcException):
    pass
