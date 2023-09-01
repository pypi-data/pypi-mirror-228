import sys
import os
relative_path = os.getcwd()
sys.path.append(relative_path)
if True:
    from mysql import *
