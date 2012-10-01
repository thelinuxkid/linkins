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

def test_splitondir_simple():
    on = '/foo/bar'
    path = '/foo/bar/fee/fo'
    res = util.splitondir(on, path)
    assert res == 'fee/fo'

def test_splitondir_on_root():
    on = '/'
    path = '/foo/bar'
    res = util.splitondir(on, path)
    assert res == 'foo/bar'

def test_splitondir_on_trailing_slash():
    on = '/foo/bar/'
    path = '/foo/bar/fee'
    res = util.splitondir(on, path)
    assert res == 'fee'

def test_splitondir_on_rel():
    on = 'bar/fee/foo/far'
    path = '/foo/bar/fee'
    res = util.splitondir(on, path)
    assert res == None

def test_splitondir_on_empty():
    on = ''
    path = '/foo/bar'
    res = util.splitondir(on, path)
    assert res == None

def test_splitondir_on_longer():
    on = '/foo/bar/fee'
    path = '/foo/bar'
    res = util.splitondir(on, path)
    assert res == ''

def test_splitondir_on_same():
    on = '/foo/bar'
    path = '/foo/bar'
    res = util.splitondir(on, path)
    assert res == ''

def test_splitondir_path_rel():
    on = '/foo/bar'
    path = 'foo/bar/fee'
    res = util.splitondir(on, path)
    assert res == None

def test_splitondir_path_empty():
    on = '/foo/bar'
    path = ''
    res = util.splitondir(on, path)
    assert res == None

def test_splitondir_path_root():
    on = '/foo/bar'
    path = '/'
    res = util.splitondir(on, path)
    assert res == ''

def test_splitondir_path_trailing_slash():
    on = '/foo/bar'
    path = '/foo/bar/'
    res = util.splitondir(on, path)
    assert res == ''

def test_splitondir_both_rel():
    on = 'foo/bar'
    path = 'foo/bar/fee'
    res = util.splitondir(on, path)
    assert res == 'fee'

def test_splitondir_both_empty():
    on = ''
    path = ''
    res = util.splitondir(on, path)
    assert res == ''
