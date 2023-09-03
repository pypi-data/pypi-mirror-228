import sys
from pathlib import Path


def add_parents(stopfile=".gitignore"):
    # collect list of all parents up directory tree
    parents = list(Path().absolute().parents)

    # stop the iteration once stopfile has been found
    # (stopfile path will be added as a new_path but parents will not)
    stopfile_path = False
    found = False

    for parent in parents:
        if found:
            break

        for file in parent.iterdir():
            if file.name == stopfile:
                found = True

                stopfile_path = parent

                break

    # only add parents up to and including that which contains the stopfile
    nbpaths = parents[: parents.index(stopfile_path) + 1] if stopfile_path else parents            

    # avoid adding duplicate paths to sys.path
    new_paths = [str(path) for path in nbpaths if str(path) not in sys.path]

    # reverse the path order so that parents closer to current file are checked first
    # insert in second position as the first entry in sys.path is the current directory

    new_paths.reverse()
    for path in new_paths:
        sys.path.insert(1, path)

    return
