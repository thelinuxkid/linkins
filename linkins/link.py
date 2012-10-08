import os
import logging

from linkins import script

log = logging.getLogger(__name__)

def make(
        srcdir,
        linkdir,
        scriptname=None,
        runscript=False,
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
            try:
                os.symlink(srcpath, linkpath)
            except OSError, e:
                if e.errno == 17 and e.strerror == 'File exists':
                    log.error(
                        '{linkpath} already exists. Not linking.'.format(
                            linkpath=linkpath,
                        )
                    )
                else:
                    raise
        # Don't run scriptsrc if it's None or empty
        if scriptsrc and runscript:
            scripttail = os.path.relpath(scriptsrc, srcdir)
            scriptdst = os.path.join(linkdir, scripttail)
            linkscriptdir = os.path.dirname(scriptdst)
            if not os.path.exists(linkscriptdir):
                os.makedirs(linkscriptdir)
            srcscriptdir = os.path.dirname(scriptsrc)
            script.runscript(scriptsrc, srcscriptdir, linkscriptdir)
