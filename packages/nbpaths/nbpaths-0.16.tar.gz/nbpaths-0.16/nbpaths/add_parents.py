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

    # avoid adding duplicate paths to sys.path
    new_paths = [parent for parent in parents if str(parent) not in sys.path]

    # only add parents up to and including that which contains the stopfile
    if stopfile_path:
        new_paths = new_paths[: new_paths.index(stopfile_path) + 1]

    paths_to_add = [str(path) for path in new_paths]

    # reverse the path order so that parents closer to current file are checked first
    # insert in second position as the first entry in sys.path is the current directory

    paths_to_add.reverse()
    for path in paths_to_add:
        sys.path.insert(1, path)

    return
