import os
import contextlib

# Unix, Windows and old Macintosh end-of-line
newlines = ['\n', '\r\n', '\r']


# Avoid name clash with os.path.abspath
def abs_path(path):
    path = os.path.expanduser(path)
    path = os.path.abspath(path)
    return path


def unbuffered_stream(proc, stream='stdout'):
    stream = getattr(proc, stream)
    with contextlib.closing(stream):
        while True:
            out = []
            last = stream.read(1)
            # Don't loop forever
            if last == '' and proc.poll() is not None:
                break
            while last not in newlines:
                out.append(last)
                last = stream.read(1)
            out = ''.join(out)
            yield out
