import os

def checkPermissions(path:str, permissions:int):
    currentPermissions = os.stat(path).st_mode
    if oct(currentPermissions)[-3:] != oct(permissions)[-3:]:
        os.chmod(path, permissions)
