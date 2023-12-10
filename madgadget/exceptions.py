class GithubNotReachableError(Exception):
    pass


class AndroidUnpackError(Exception):
    pass


class ApktoolError(Exception):
    pass


class ApktoolMissingError(AndroidUnpackError, ApktoolError):
    pass


class AndroidPatchError(Exception):
    pass


class ZipalignError(Exception):
    pass


class APKEditorError(Exception):
    pass


class APKEditorMissingError(AndroidUnpackError, APKEditorError):
    pass
