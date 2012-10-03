import os
import logging

from linkins import util

log = logging.getLogger(__name__)

def make(
        srcdir,
        linkdir,
):
    if not os.path.exists(srcdir):
        raise ValueError(
            'Target directory "{srcdir}" does not exist'.format(
                srcdir=srcdir,
            )
        )
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
            try:
                os.symlink(srcpath, linkpath)
            except OSError, e:
                if e.errno == 17 and e.strerror == 'File exists':
                    log.debug(
                        '{linkpath} already exists'.format(
                            linkpath=linkpath,
                        )
                    )
                else:
                    raise
