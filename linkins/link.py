import os

from linkins import util

def make(
        srcdir,
        linkdir,
):
    if not os.path.exists(linkdir):
        raise ValueError(
            'Link directory "{linkdir}" does not exist'.format(
                linkdir=linkdir,
            )
        )
    for (path, dirs, files) in os.walk(srcdir):
        for file_ in files:
            srcpath = os.path.join(path, file_)
            pathtail = util.splitondir(srcdir, srcpath)
            linkpath = os.path.join(linkdir, pathtail)
            pathexist = os.path.dirname(linkpath)
            if not os.path.exists(pathexist):
                os.makedirs(pathexist)
            os.symlink(srcpath, linkpath)
