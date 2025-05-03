import os
import json

def resolvePath(path: str) -> str:
    if path.startswith("~"):
        return os.path.expanduser(path)
    
    if path.startswith("."):
        return os.path.join(os.getenv("PWD", ""), path[1:])
    
    return path


def binarySearch(binary:str) -> dict:
    enviroment_path = os.getenv("PATH").split(":")
    binarys_found = {}

    for _path in enviroment_path:
        _root_path = resolvePath(_path)
        _content_dir = os.listdir(_root_path)
        
        for _item in _content_dir:
            if os.path.isdir(_item) == False:
                full_path = os.path.join(_root_path, _item)            
                binarys_found[_item] = full_path

    if binary in binarys_found:
        return binarys_found[binary]
    
    return None


if __name__ == "__main__":
    print(binarySearch("wireguard"))
