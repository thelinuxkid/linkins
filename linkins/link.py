import os
import errno
import logging

from linkins import script

log = logging.getLogger(__name__)

def _unlink(linkpath):
    try:
        os.unlink(linkpath)
    except OSError, e:
        # It's OK if the link disappeared
        if e.errno != errno.ENOENT:
            raise

def _clean_empty_dirs(path, linkdir):
    if os.listdir(path) != [] or path == linkdir:
        return
    os.rmdir(path)
    parent = os.path.dirname(path)
    _clean_empty_dirs(parent, linkdir)

def _clean(
        files,
        path,
        srcdir,
        linkdir,
):
    pathtail = os.path.relpath(path, srcdir)
    linkpath = os.path.join(linkdir, pathtail)
    # Avoid a possible . at the end of path, e.g., "/foo/."
    linkpath = os.path.normpath(linkpath)
    for file_ in files:
        linkfile = os.path.join(linkpath, file_)
        if os.path.lexists(linkfile):
            log.debug(
                '{linkfile} exists. Removing.'.format(
                    linkfile=linkfile,
                )
            )
            _unlink(linkfile)
    if os.path.exists(linkpath):
        _clean_empty_dirs(linkpath, linkdir)

def _link(
        files,
        path,
        srcdir,
        linkdir,
        replace,
):
    for file_ in files:
        srcpath = os.path.join(path, file_)
        pathtail = os.path.relpath(srcpath, srcdir)
        linkpath = os.path.join(linkdir, pathtail)
        pathexist = os.path.dirname(linkpath)
        if not os.path.exists(pathexist):
            os.makedirs(pathexist)
        if os.path.lexists(linkpath):
            if not replace:
                log.warn(
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
            _unlink(linkpath)
        os.symlink(srcpath, linkpath)

def _script(
        scriptsrc,
        path,
        srcdir,
        linkdir,
        multiprocess,
):
      scriptdir = os.path.dirname(scriptsrc)
      scripttail = os.path.relpath(scriptdir, srcdir)
      scriptdst = os.path.join(linkdir, scripttail)
      name = os.path.basename(scriptsrc)
      name = os.path.join(scripttail, name)
      if not os.path.exists(scriptdst):
          os.makedirs(scriptdst)
      log.debug(
          'Running script {name}'.format(
              name=name,
          )
      )
      script.runscript(
          scriptsrc,
          srcdir,
          linkdir,
          scripttail,
          name=name,
          multiprocess=multiprocess,
      )

def _exclude(path, files, exclude):
    for file_ in exclude:
        out = os.path.relpath(file_, path)
        if out in files:
            log.debug(
                'Excluding {file_}'.format(
                    file_=file_,
                )
            )
            files.remove(out)
    return files

def make(
        srcdir,
        linkdir,
        scriptname=None,
        runscript=False,
        replace=False,
        clean=False,
        multiprocess=False,
        exclude=None,
):
    if exclude is None:
        exclude = []
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
        pathtail = os.path.relpath(path, srcdir)
        if pathtail in exclude:
            log.debug(
                'Excluding {pathtail}'.format(
                    pathtail=pathtail,
                )
            )
            continue
        files = _exclude(pathtail, files, exclude)
        scriptsrc = None
        if scriptname is not None and scriptname in files:
            scriptsrc = os.path.join(path, scriptname)
            files.remove(scriptname)
        if clean:
            _clean(
                files,
                path,
                srcdir,
                linkdir,
            )
            continue
        _link(
            files,
            path,
            srcdir,
            linkdir,
            replace,
        )
        # Don't run scriptsrc if it's None or empty
        if scriptsrc and runscript:
            _script(
                scriptsrc,
                path,
                srcdir,
                linkdir,
                multiprocess,
            )
