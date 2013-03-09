import os
import logging
import subprocess
import multiprocessing

from linkins.util import unbuffered_stream

log = logging.getLogger(__name__)
log.propagate = False
handler = logging.StreamHandler()
fmt = logging.Formatter(
    fmt='%(script)s: %(source)s: %(message)s',
)
handler.setFormatter(fmt)
log.addHandler(handler)

def _run(cmd, name):
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        # Make all end-of-lines '\n'
        universal_newlines=True,
    )
    extra = dict([
        ('script', name),
        ('source', 'SCRIPT'),
    ])
    for line in unbuffered_stream(proc):
        log.info(
            line,
            extra=extra,
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
