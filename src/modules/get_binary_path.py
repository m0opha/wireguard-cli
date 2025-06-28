import sys
import os
import json

try:
    from .utils import resolvePath
except ImportError:
    from utils import resolvePath

def getBinaryPath(target_binary:str) -> dict:
    enviroment_paths = os.getenv("PATH").split(":")
    
    binary_isin = []

    for path in enviroment_paths:
        absolute_root_path = os.path.join(resolvePath(path)) 

        for item in os.listdir(absolute_root_path):            
            if item == target_binary:
                binary_isin.append(os.path.join(absolute_root_path, item))

    return binary_isin[0]


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print(f"usage: {os.path.basename(__file__)} <seached binary in path>")
        sys.exit(0)

    print(getBinaryPath(sys.argv[1]))