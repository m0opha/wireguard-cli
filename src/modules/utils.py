import os

def resolvePath(path: str) -> str:
    path = os.path.expanduser(path)    
    path = os.path.abspath(path)
    return path