import os

from contextlib import contextmanager

@contextmanager
def remove_path(path):
    try:
        yield path
    finally:
        try:
            os.remove(path)
        except OSError, e:
            # It's OK if the path is already gone
            if not (
                    e.errno == 2
                    and
                    e.strerror == 'No such file or directory'
            ):
                raise

# Avoid name clash with os.path.abspath
def abs_path(path):
    path = os.path.expanduser(path)
    path = os.path.abspath(path)
    return path

def splitall(path):
    # TODO test to see if this works across platforms. If the behavior
    # of os.path.split is consistent then it should.
    def _splitall(path):
        (head,tail) = os.path.split(path)
        # We need to make sure that the tail is not empty
        # because there was a leading slash.
        (head_,tail_) = os.path.split(head)
        # We've reached the root of the path
        if tail == '' and tail_ == '':
            if head != '':
                yield head
        else:
            for h in _splitall(head):
                yield h
        # This conditional statement prevents yielding the empty string
        # when os.path.split has returned ('/', ''). For this function it
        # means we have reached the end of an absolute path. The case in
        # which we should return the empty string, i.e., when the user
        # provided path is '/', is covered by the calling function.
        if not (head_ != '' and tail_ == '' and head != '' and tail == ''):
            yield tail

    # Special case where we always return the exact same result as
    # os.path.split
    if len(path) <= 1:
        (head,tail) = os.path.split(path)
        yield head
        yield tail
    else:
        for s in _splitall(path):
            yield s
