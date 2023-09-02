import path
import sys
directory = path.Path(__file__).abspath()
sys.path.append(directory.parent)

import os

def ensure_dir(path_to_dir:str)->None:
        """
        Ensure existence of the specific directory in the file system
        
        :param path_to_dir:str -- path of the directory whose existence should be ensured
        """    
        if not os.path.exists(path_to_dir):
            os.mkdir(path_to_dir)