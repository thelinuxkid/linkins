from linkins import util

def test_splitall_simple():
    path = '/foo/bar'
    res = util.splitall(path)
    assert list(res) == ['/', 'foo', 'bar']

def test_splitall_rel():
    path = 'foo/bar'
    res = util.splitall(path)
    assert list(res) == ['', 'foo', 'bar']

def test_splitall_one_char():
    path = 'p'
    res = util.splitall(path)
    assert list(res) == ['', 'p']

def test_splitall_empty():
    path = ''
    res = util.splitall(path)
    assert list(res) == ['', '']

def test_splitall_root():
    path = '/'
    res = util.splitall(path)
    assert list(res) == ['/', '']

def test_splitall_trailing_slash():
    path = '/foo/bar/'
    res = util.splitall(path)
    assert list(res) == ['/', 'foo', 'bar', '']

def test_splitall_trailing_slash_rel():
    path = 'bar/'
    res = util.splitall(path)
    assert list(res) == ['', 'bar', '']
