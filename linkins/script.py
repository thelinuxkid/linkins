import os
import logging
import subprocess
import multiprocessing

log = logging.getLogger(__name__)
log.propagate = False
handler = logging.StreamHandler()
fmt = logging.Formatter(
    fmt='%(script)s: %(stream)s: %(message)s',
    )
handler.setFormatter(fmt)
log.addHandler(handler)

def _logscript(fp, **kwargs):
    for line in fp:
        line = line.strip()
        log.info(line, extra=kwargs)

def _run(cmd, name):
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    with proc.stderr as fp:
        _logscript(
            fp,
            script=name,
            stream='STDERR',
        )
    with proc.stdout as fp:
        _logscript(
            fp,
            script=name,
            stream='STDOUT',
        )

def runscript(path, *args, **kwargs):
    multi = kwargs.get('multiprocess', False)
    name = os.path.basename(path)
    name = kwargs.get('name', name)
    cmd = [path] + list(args)
    if multi:
        proc = multiprocessing.Process(
            target=_run,
            args=(cmd, name),
        )
        proc.start()
        return
    _run(cmd, name)
