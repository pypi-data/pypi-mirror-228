import sys
from pathlib import Path

parents = Path().absolute().parents


def add_parents_to_path():

    print(' go go go')
    '''
    for parent in parents:

        if str(parent) not in sys.path:

            sys.path.insert(0, str(parent))

        for file in parent.iterdir():

            if file.name.endswith(".gitignore"):

                return
 '''
add_parents_to_path()