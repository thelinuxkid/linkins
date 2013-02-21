import re
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

def _exclude_regex(
        path,
        exclude,
        include,
):
    for exclude_regex in exclude:
        if not exclude_regex.match(path):
            continue
        for include_regex in include:
            if include_regex.match(path):
                return False
        return True
    return False

def _exclude(
        srcdir,
        path,
        files,
        exclude,
        include,
):
    pathtail = os.path.relpath(path, srcdir)
    if _exclude_regex(
            pathtail,
            exclude,
            include,
    ):
        log.debug(
            'Excluding directory {pathtail}'.format(
                pathtail=pathtail,
            )
        )
        return
    result = []
    for file_ in files:
        filetail = os.path.join(pathtail, file_)
        # Avoid paths like ./foo
        filetail = os.path.normpath(filetail)
        if _exclude_regex(
                filetail,
                exclude,
                include,
        ):
            log.debug(
                'Excluding file {filetail}'.format(
                    filetail=filetail,
                )
            )
            continue
        result.append(file_)
    return result

def make(
        srcdir,
        linkdir,
        scriptname=None,
        runscript=False,
        replace=False,
        clean=False,
        multiprocess=False,
        exclude=None,
        include=None,
):
    if exclude is None:
        exclude = []
    if include is None:
        include = []
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
    exclude_regex = [re.compile(file_) for file_ in exclude]
    include_regex = [re.compile(file_) for file_ in include]
    for (path, dirs, files) in os.walk(srcdir):
        files = _exclude(
            srcdir,
            path,
            files,
            exclude_regex,
            include_regex,
        )
        if not files:
            continue
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
                srcdir,
                linkdir,
                multiprocess,
            )
