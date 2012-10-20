import os
import errno
import logging

from linkins import script

log = logging.getLogger(__name__)

def make(
        srcdir,
        linkdir,
        scriptname=None,
        runscript=False,
        replace=False,
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
        scriptsrc = None
        if scriptname is not None and scriptname in files:
            scriptsrc = os.path.join(path, scriptname)
            files.remove(scriptname)
        for file_ in files:
            srcpath = os.path.join(path, file_)
            pathtail = os.path.relpath(srcpath, srcdir)
            linkpath = os.path.join(linkdir, pathtail)
            pathexist = os.path.dirname(linkpath)
            if not os.path.exists(pathexist):
                os.makedirs(pathexist)
            if os.path.exists(linkpath):
                if not replace:
                    log.error(
                        '{linkpath} already exists. Not linking.'.format(
                            linkpath=linkpath,
                        )
                    )
                    continue
                log.debug(
                    '{linkpath} already exists. Replacing.'.format(
                        linkpath=linkpath,
                    )
                )
                try:
                    os.unlink(linkpath)
                except OSError, e:
                    # It's OK if the link disappeared
                    if e.errno != errno.ENOENT:
                        raise
            os.symlink(srcpath, linkpath)
        # Don't run scriptsrc if it's None or empty
        if scriptsrc and runscript:
            scriptdir = os.path.dirname(scriptsrc)
            scripttail = os.path.relpath(scriptdir, srcdir)
            scriptdst = os.path.join(linkdir, scripttail)
            if not os.path.exists(scriptdst):
                os.makedirs(scriptdst)
            script.runscript(scriptsrc, srcdir, linkdir, scripttail)
