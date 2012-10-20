import os
import errno

import mock
import pytest
import tempdirs

from linkins import link

@tempdirs.makedirs(2)
def test_make_simple(srcdir, linkdir):
    srcfile = os.path.join(srcdir, 'foo')
    linkfile = os.path.join(linkdir, 'foo')
    with open(srcfile, 'w') as fp:
        fp.write('source content')
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
    )
    assert os.listdir(linkdir) == ['foo']
    assert os.path.isfile(srcfile)
    assert os.path.islink(linkfile)
    with open(linkfile) as fp:
        assert fp.read() == 'source content'

@tempdirs.makedirs(2)
def test_make_nested_dirs(srcdir, linkdir):
    nesteddir = os.path.join(srcdir, 'foo', 'bar')
    os.makedirs(nesteddir)
    srcfile = os.path.join(srcdir, 'foo', 'bar', 'fee')
    linkfile = os.path.join(linkdir, 'foo', 'bar', 'fee')
    with open(srcfile, 'w') as fp:
        fp.write('source content')
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
    )
    assert os.listdir(linkdir) == ['foo']
    foodir = os.path.join(linkdir, 'foo')
    assert os.listdir(foodir) == ['bar']
    bardir = os.path.join(foodir, 'bar')
    assert os.listdir(bardir) == ['fee']
    assert os.path.isfile(srcfile)
    assert os.path.islink(linkfile)
    with open(linkfile) as fp:
        assert fp.read() == 'source content'

@tempdirs.makedirs(2)
def test_make_nested_dirs_empty(srcdir, linkdir):
    nesteddir = os.path.join(srcdir, 'foo', 'bar')
    os.makedirs(nesteddir)
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
    )
    assert os.listdir(linkdir) == []

@tempdirs.makedirs(2)
def test_make_many_dirs(srcdir, linkdir):
    nesteddir = os.path.join(srcdir, 'foo')
    os.makedirs(nesteddir)
    nesteddir = os.path.join(srcdir, 'fee')
    os.makedirs(nesteddir)
    barsrc = os.path.join(srcdir, 'foo', 'bar')
    barlink = os.path.join(linkdir, 'foo', 'bar')
    fosrc = os.path.join(srcdir, 'fee', 'fo')
    folink = os.path.join(linkdir, 'fee', 'fo')
    with open(barsrc, 'w') as fp:
        fp.write('bar source content')
    with open(fosrc, 'w') as fp:
        fp.write('fo source content')
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
    )
    assert sorted(os.listdir(linkdir)) == sorted(['foo', 'fee'])
    foodir = os.path.join(linkdir, 'foo')
    assert os.listdir(foodir) == ['bar']
    feedir = os.path.join(linkdir, 'fee')
    assert os.listdir(feedir) == ['fo']
    assert os.path.isfile(barsrc)
    assert os.path.islink(barlink)
    with open(barlink) as fp:
        assert fp.read() == 'bar source content'
    assert os.path.isfile(fosrc)
    assert os.path.islink(folink)
    with open(folink) as fp:
        assert fp.read() == 'fo source content'

@tempdirs.makedirs(2)
def test_make_many_files(srcdir, linkdir):
    foosrc = os.path.join(srcdir, 'foo')
    barsrc = os.path.join(srcdir, 'bar')
    foolink = os.path.join(linkdir, 'foo')
    barlink = os.path.join(linkdir, 'bar')
    with open(foosrc, 'w') as fp:
        fp.write('foo source content')
    with open(barsrc, 'w') as fp:
        fp.write('bar source content')
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
    )
    assert sorted(os.listdir(linkdir)) == sorted(['foo', 'bar'])
    assert os.path.isfile(foosrc)
    assert os.path.isfile(barsrc)
    assert os.path.islink(foolink)
    assert os.path.islink(barlink)
    with open(foolink) as fp:
        assert fp.read() == 'foo source content'
    with open(barlink) as fp:
        assert fp.read() == 'bar source content'

@tempdirs.makedirs()
def test_make_bad_linkdir(srcdir):
    res = pytest.raises(
        ValueError,
        link.make,
        srcdir=srcdir,
        linkdir='',
        )
    assert res.type == ValueError
    assert res.value.message == 'Link directory "" does not exist'

@tempdirs.makedirs()
def test_make_bad_srcdir(linkdir):
    res = pytest.raises(
        ValueError,
        link.make,
        srcdir='',
        linkdir=linkdir,
        )
    assert res.type == ValueError
    assert res.value.message == 'Target directory "" does not exist'

@tempdirs.makedirs(2)
def test_make_dir_exists(srcdir, linkdir):
    srcfile = os.path.join(srcdir, 'foo')
    linkfile = os.path.join(linkdir, 'foo')
    olddir = os.path.join(linkdir, 'fee')
    os.makedirs(olddir)
    with open(srcfile, 'w') as fp:
        fp.write('source content')
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
    )
    assert sorted(os.listdir(linkdir)) == sorted(['foo', 'fee'])
    assert os.listdir(olddir) == []
    assert os.path.isfile(srcfile)
    assert os.path.islink(linkfile)
    with open(linkfile) as fp:
        assert fp.read() == 'source content'

@tempdirs.makedirs(2)
def test_make_file_exists(srcdir, linkdir):
    srcfile = os.path.join(srcdir, 'foo')
    linkfile = os.path.join(linkdir, 'foo')
    oldfile = os.path.join(linkdir, 'fee')
    with open(oldfile, 'w') as fp:
        fp.write('old content')
    with open(srcfile, 'w') as fp:
        fp.write('source content')
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
    )
    assert sorted(os.listdir(linkdir)) == sorted(['foo', 'fee'])
    assert os.path.isfile(oldfile)
    with open(oldfile) as fp:
        assert fp.read() == 'old content'
    assert os.path.isfile(srcfile)
    assert os.path.islink(linkfile)
    with open(linkfile) as fp:
        assert fp.read() == 'source content'

@tempdirs.makedirs(2)
def test_make_nested_dir_exists(srcdir, linkdir):
    nesteddir = os.path.join(srcdir, 'foo')
    os.makedirs(nesteddir)
    srcfile = os.path.join(srcdir, 'foo', 'fee')
    linkfile = os.path.join(linkdir, 'foo', 'fee')
    olddir = os.path.join(linkdir, 'foo', 'fo')
    os.makedirs(olddir)
    with open(srcfile, 'w') as fp:
        fp.write('source content')
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
    )
    assert os.listdir(linkdir) == ['foo']
    foodir = os.path.join(linkdir, 'foo')
    assert sorted(os.listdir(foodir)) == sorted(['fo', 'fee'])
    assert os.listdir(olddir) == []
    assert os.path.isfile(srcfile)
    assert os.path.islink(linkfile)
    with open(linkfile) as fp:
        assert fp.read() == 'source content'

@tempdirs.makedirs(2)
def test_make_nested_file_exists(srcdir, linkdir):
    nesteddir = os.path.join(srcdir, 'foo')
    os.makedirs(nesteddir)
    srcfile = os.path.join(srcdir, 'foo', 'fee')
    linkfile = os.path.join(linkdir, 'foo', 'fee')
    olddir = os.path.join(linkdir, 'foo')
    os.makedirs(olddir)
    oldfile = os.path.join(linkdir, 'foo', 'fo')
    with open(oldfile, 'w') as fp:
        fp.write('old content')
    with open(srcfile, 'w') as fp:
        fp.write('source content')
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
    )
    assert os.listdir(linkdir) == ['foo']
    foodir = os.path.join(linkdir, 'foo')
    assert sorted(os.listdir(foodir)) == sorted(['fo', 'fee'])
    assert os.path.isfile(oldfile)
    with open(oldfile) as fp:
        assert fp.read() == 'old content'
    assert os.path.isfile(srcfile)
    assert os.path.islink(linkfile)
    with open(linkfile) as fp:
        assert fp.read() == 'source content'

@tempdirs.makedirs(2)
@mock.patch('linkins.link.log')
def test_make_linkdir_has_file(srcdir, linkdir, fakelog):
    srcfile = os.path.join(srcdir, 'foo')
    linkfile = os.path.join(linkdir, 'foo')
    with open(srcfile, 'w') as fp:
        fp.write('source content')
    with open(linkfile, 'w') as fp:
        fp.write('existing content')
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
    )
    error = mock.call.error(
        '{linkfile} already exists. Not linking.'.format(
            linkfile=linkfile,
        ),
    )
    assert fakelog.mock_calls == [error]

@tempdirs.makedirs(2)
@mock.patch('linkins.link.log')
def test_make_linkdir_has_link(srcdir, linkdir, fakelog):
    srcfile = os.path.join(srcdir, 'foo')
    linkfile = os.path.join(linkdir, 'foo')
    with open(srcfile, 'w') as fp:
        fp.write('source content')
    os.symlink(srcfile, linkfile)
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
    )
    error = mock.call.error(
        '{linkfile} already exists. Not linking.'.format(
            linkfile=linkfile,
        ),
    )
    assert fakelog.mock_calls == [error]

@tempdirs.makedirs(2)
@mock.patch('linkins.link.log')
def test_make_linkdir_replace_file(srcdir, linkdir, fakelog):
    srcfile = os.path.join(srcdir, 'foo')
    linkfile = os.path.join(linkdir, 'foo')
    with open(srcfile, 'w') as fp:
        fp.write('source content')
    with open(linkfile, 'w') as fp:
        fp.write('existing content')
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
        replace=True,
    )
    debug = mock.call.debug(
        '{linkfile} already exists. Replacing.'.format(
            linkfile=linkfile,
        ),
    )
    assert fakelog.mock_calls == [debug]
    assert os.listdir(linkdir) == ['foo']
    assert os.path.isfile(srcfile)
    assert os.path.islink(linkfile)
    with open(linkfile) as fp:
        assert fp.read() == 'source content'

@tempdirs.makedirs(2)
@mock.patch('linkins.link.log')
def test_make_linkdir_replace_same_link(srcdir, linkdir, fakelog):
    srcfile = os.path.join(srcdir, 'foo')
    linkfile = os.path.join(linkdir, 'foo')
    with open(srcfile, 'w') as fp:
        fp.write('source content')
    os.symlink(srcfile, linkfile)
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
        replace=True,
    )
    debug = mock.call.debug(
        '{linkfile} already exists. Replacing.'.format(
            linkfile=linkfile,
        ),
    )
    assert fakelog.mock_calls == [debug]
    assert os.listdir(linkdir) == ['foo']
    assert os.path.isfile(srcfile)
    assert os.path.islink(linkfile)
    with open(linkfile) as fp:
        assert fp.read() == 'source content'

@tempdirs.makedirs(3)
@mock.patch('linkins.link.log')
def test_make_linkdir_replace_different_link(
        srcdir,
        linkdir,
        diffdir,
        fakelog,
):
    srcfile = os.path.join(srcdir, 'foo')
    linkfile = os.path.join(linkdir, 'foo')
    difffile = os.path.join(diffdir, 'foo')
    with open(srcfile, 'w') as fp:
        fp.write('source content')
    with open(difffile, 'w') as fp:
        fp.write('different content')
    os.symlink(difffile, linkfile)
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
        replace=True,
    )
    debug = mock.call.debug(
        '{linkfile} already exists. Replacing.'.format(
            linkfile=linkfile,
        ),
    )
    assert fakelog.mock_calls == [debug]
    assert os.listdir(linkdir) == ['foo']
    assert os.path.isfile(srcfile)
    assert os.path.islink(linkfile)
    with open(linkfile) as fp:
        assert fp.read() == 'source content'

@tempdirs.makedirs(2)
@mock.patch('linkins.link.log')
@mock.patch('os.unlink')
def test_make_linkdir_unlink_oserror(
        srcdir,
        linkdir,
        fakeunlink,
        fakelog,
):
    srcfile = os.path.join(srcdir, 'foo')
    linkfile = os.path.join(linkdir, 'foo')
    with open(srcfile, 'w') as fp:
        fp.write('source content')
    os.symlink(srcfile, linkfile)
    error = OSError()
    error.errno = errno.EXDEV
    fakeunlink.side_effect = error
    res = pytest.raises(
        OSError,
        link.make,
        srcdir=srcdir,
        linkdir=linkdir,
        replace=True,
        )
    debug = mock.call.debug(
        '{linkfile} already exists. Replacing.'.format(
            linkfile=linkfile,
        ),
    )
    assert fakelog.mock_calls == [debug]
    unlink = mock.call(linkfile)
    assert fakeunlink.mock_calls == [unlink]
    assert res.type == OSError
    assert res.value.errno == errno.EXDEV

@tempdirs.makedirs(2)
@mock.patch('linkins.link.log')
@mock.patch('os.unlink')
def test_make_linkdir_unlink_oserror_enoent(
        srcdir,
        linkdir,
        fakeunlink,
        fakelog,
):
    srcfile = os.path.join(srcdir, 'foo')
    linkfile = os.path.join(linkdir, 'foo')
    with open(srcfile, 'w') as fp:
        fp.write('source content')
    with open(linkfile, 'w') as fp:
        fp.write('existing content')
    def side_effect(*args):
        os.remove(linkfile)
        error = OSError()
        error.errno = errno.ENOENT
        raise error
    fakeunlink.side_effect = side_effect
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
        replace=True,
    )
    debug = mock.call.debug(
        '{linkfile} already exists. Replacing.'.format(
            linkfile=linkfile,
        ),
    )
    assert fakelog.mock_calls == [debug]
    unlink = mock.call(linkfile)
    assert fakeunlink.mock_calls == [unlink]
    assert os.listdir(linkdir) == ['foo']
    assert os.path.isfile(srcfile)
    assert os.path.islink(linkfile)
    with open(linkfile) as fp:
        assert fp.read() == 'source content'

@tempdirs.makedirs(2)
@mock.patch('linkins.script.runscript')
def test_make_script_simple(srcdir, linkdir, fakerun):
    scriptfile = os.path.join(srcdir, 'foo-script')
    with open(scriptfile, 'w') as fp:
        fp.write('script content')
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
        scriptname='foo-script',
        runscript=True,
    )
    run = mock.call(
        scriptfile,
        srcdir,
        linkdir,
        '.',
        )
    assert fakerun.mock_calls == [run]
    assert os.listdir(linkdir) == []

@tempdirs.makedirs(2)
@mock.patch('linkins.script.runscript')
def test_make_script_many_files(srcdir, linkdir, fakerun):
    srcfile = os.path.join(srcdir, 'foo')
    linkfile = os.path.join(linkdir, 'foo')
    scriptfile = os.path.join(srcdir, 'foo-script')
    with open(srcfile, 'w') as fp:
        fp.write('source content')
    with open(scriptfile, 'w') as fp:
        fp.write('script content')
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
        scriptname='foo-script',
        runscript=True,
    )
    run = mock.call(
        scriptfile,
        srcdir,
        linkdir,
        '.',
        )
    assert fakerun.mock_calls == [run]
    assert os.listdir(linkdir) == ['foo']
    assert os.path.isfile(srcfile)
    assert os.path.islink(linkfile)
    with open(linkfile) as fp:
        assert fp.read() == 'source content'

@tempdirs.makedirs(2)
@mock.patch('linkins.script.runscript')
def test_make_script_nested_dir(srcdir, linkdir, fakerun):
    srcnesteddir = os.path.join(srcdir, 'foo')
    os.makedirs(srcnesteddir)
    scriptfile = os.path.join(srcnesteddir, 'bar-script')
    with open(scriptfile, 'w') as fp:
        fp.write('script content')
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
        scriptname='bar-script',
        runscript=True,
    )
    run = mock.call(
        scriptfile,
        srcdir,
        linkdir,
        'foo',
        )
    assert fakerun.mock_calls == [run]
    assert os.listdir(linkdir) == ['foo']

@tempdirs.makedirs(2)
@mock.patch('linkins.script.runscript')
def test_make_script_many_scripts(srcdir, linkdir, fakerun):
    srcnesteddir = os.path.join(srcdir, 'foo')
    os.makedirs(srcnesteddir)
    scriptfile = os.path.join(srcdir, 'bar-script')
    scriptnested = os.path.join(srcnesteddir, 'bar-script')
    with open(scriptfile, 'w') as fp:
        fp.write('bar script content')
    with open(scriptnested, 'w') as fp:
        fp.write('bar nested script content')
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
        scriptname='bar-script',
        runscript=True,
    )
    run = mock.call(
        scriptfile,
        srcdir,
        linkdir,
        '.',
        )
    runnested = mock.call(
        scriptnested,
        srcdir,
        linkdir,
        'foo',
        )
    calls = [
        run,
        runnested,
        ]
    assert fakerun.mock_calls == calls
    assert os.listdir(linkdir) == ['foo']

@tempdirs.makedirs(2)
@mock.patch('linkins.script.runscript')
def test_make_script_no_run(srcdir, linkdir, fakerun):
    scriptfile = os.path.join(srcdir, 'foo-script')
    with open(scriptfile, 'w') as fp:
        fp.write('script content')
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
        scriptname='foo-script',
    )
    assert fakerun.mock_calls == []
    assert os.listdir(linkdir) == []

@tempdirs.makedirs(2)
@mock.patch('linkins.script.runscript')
def test_make_script_no_run_nested(srcdir, linkdir, fakerun):
    nesteddir = os.path.join(srcdir, 'foo', 'bar')
    os.makedirs(nesteddir)
    scriptfile = os.path.join(nesteddir, 'foo-script')
    with open(scriptfile, 'w') as fp:
        fp.write('script content')
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
        scriptname='foo-script',
    )
    assert fakerun.mock_calls == []
    assert os.listdir(linkdir) == []
