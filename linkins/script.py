import os
import logging
import subprocess

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

def runscript(path, *args):
    name = os.path.basename(path)
    cmd = [path] + list(args)
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
