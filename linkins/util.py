import os

# Avoid name clash with os.path.abspath
def abs_path(path):
    path = os.path.expanduser(path)
    path = os.path.abspath(path)
    return path
