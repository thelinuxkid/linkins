import os
import errno

import mock
import pytest
import tempdirs

from linkins import link


@tempdirs.makedirs(2)
def test_make_simple(**kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
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
def test_make_nested_dirs(**kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
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
def test_make_nested_dirs_empty(**kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
    nesteddir = os.path.join(srcdir, 'foo', 'bar')
    os.makedirs(nesteddir)
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
    )
    assert os.listdir(linkdir) == []


@tempdirs.makedirs(2)
def test_make_many_dirs(**kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
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
def test_make_many_files(**kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
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
def test_make_bad_linkdir(**kwargs):
    (srcdir,) = kwargs['tempdirs_dirs']
    res = pytest.raises(
        ValueError,
        link.make,
        srcdir=srcdir,
        linkdir='',
    )
    assert res.type == ValueError
    assert res.value.message == 'Link directory "" does not exist'


@tempdirs.makedirs()
def test_make_bad_srcdir(**kwargs):
    (linkdir,) = kwargs['tempdirs_dirs']
    res = pytest.raises(
        ValueError,
        link.make,
        srcdir='',
        linkdir=linkdir,
    )
    assert res.type == ValueError
    assert res.value.message == 'Target directory "" does not exist'


@tempdirs.makedirs(2)
def test_make_dir_exists(**kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
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
def test_make_file_exists(**kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
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
def test_make_nested_dir_exists(**kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
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
def test_make_nested_file_exists(**kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
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
def test_make_linkdir_has_file(fakelog, **kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
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
    error = mock.call.warn(
        '{linkfile} already exists. Not linking.'.format(
            linkfile=linkfile,
        ),
    )
    assert fakelog.mock_calls == [error]


@tempdirs.makedirs(2)
@mock.patch('linkins.link.log')
def test_make_linkdir_has_link(fakelog, **kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
    srcfile = os.path.join(srcdir, 'foo')
    linkfile = os.path.join(linkdir, 'foo')
    with open(srcfile, 'w') as fp:
        fp.write('source content')
    os.symlink(srcfile, linkfile)
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
    )
    error = mock.call.warn(
        '{linkfile} already exists. Not linking.'.format(
            linkfile=linkfile,
        ),
    )
    assert fakelog.mock_calls == [error]


@tempdirs.makedirs(2)
@mock.patch('linkins.link.log')
def test_make_linkdir_force_file(fakelog, **kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
    srcfile = os.path.join(srcdir, 'foo')
    linkfile = os.path.join(linkdir, 'foo')
    with open(srcfile, 'w') as fp:
        fp.write('source content')
    with open(linkfile, 'w') as fp:
        fp.write('existing content')
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
        force=True,
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
def test_make_linkdir_force_same_link(fakelog, **kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
    srcfile = os.path.join(srcdir, 'foo')
    linkfile = os.path.join(linkdir, 'foo')
    with open(srcfile, 'w') as fp:
        fp.write('source content')
    os.symlink(srcfile, linkfile)
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
        force=True,
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
def test_make_linkdir_force_different_link(
        fakelog,
        **kwargs
):
    (srcdir, linkdir, diffdir) = kwargs['tempdirs_dirs']
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
        force=True,
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
        fakeunlink,
        fakelog,
        **kwargs
):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
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
        force=True,
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
        fakeunlink,
        fakelog,
        **kwargs
):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
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
        force=True,
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
def test_make_script_simple(fakerun, **kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
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
        name='./foo-script',
        multiprocess=False,
    )
    assert fakerun.mock_calls == [run]
    assert os.listdir(linkdir) == []


@tempdirs.makedirs(2)
@mock.patch('linkins.script.runscript')
def test_make_script_many_files(fakerun, **kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
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
        name='./foo-script',
        multiprocess=False,
    )
    assert fakerun.mock_calls == [run]
    assert os.listdir(linkdir) == ['foo']
    assert os.path.isfile(srcfile)
    assert os.path.islink(linkfile)
    with open(linkfile) as fp:
        assert fp.read() == 'source content'


@tempdirs.makedirs(2)
@mock.patch('linkins.script.runscript')
def test_make_script_nested_dir(fakerun, **kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
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
        name='foo/bar-script',
        multiprocess=False,
    )
    assert fakerun.mock_calls == [run]
    assert os.listdir(linkdir) == ['foo']


@tempdirs.makedirs(2)
@mock.patch('linkins.script.runscript')
def test_make_script_many_scripts(fakerun, **kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
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
        name='./bar-script',
        multiprocess=False,
    )
    runnested = mock.call(
        scriptnested,
        srcdir,
        linkdir,
        'foo',
        name='foo/bar-script',
        multiprocess=False,
    )
    calls = [
        run,
        runnested,
    ]
    assert fakerun.mock_calls == calls
    assert os.listdir(linkdir) == ['foo']


@tempdirs.makedirs(2)
@mock.patch('linkins.script.runscript')
def test_make_script_no_run(fakerun, **kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
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
def test_make_script_no_run_nested(fakerun, **kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
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


@tempdirs.makedirs(2)
@mock.patch('linkins.script.runscript')
def test_make_script_multiprocess(fakerun, **kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
    scriptfile = os.path.join(srcdir, 'foo-script')
    with open(scriptfile, 'w') as fp:
        fp.write('script content')
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
        scriptname='foo-script',
        runscript=True,
        multiprocess=True,
    )
    run = mock.call(
        scriptfile,
        srcdir,
        linkdir,
        '.',
        name='./foo-script',
        multiprocess=True,
    )
    assert fakerun.mock_calls == [run]
    assert os.listdir(linkdir) == []


@tempdirs.makedirs(2)
@mock.patch('linkins.link.log')
def test_make_linkdir_clean_file(fakelog, **kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
    srcfile = os.path.join(srcdir, 'foo')
    linkfile = os.path.join(linkdir, 'foo')
    with open(srcfile, 'w') as fp:
        fp.write('source content')
    with open(linkfile, 'w') as fp:
        fp.write('existing content')
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
        clean=True,
    )
    debug = mock.call.debug(
        '{linkfile} exists. Removing.'.format(
            linkfile=linkfile,
        ),
    )
    assert fakelog.mock_calls == [debug]
    assert os.listdir(linkdir) == []
    assert os.path.isfile(srcfile)
    assert not os.path.exists(linkfile)


@tempdirs.makedirs(2)
@mock.patch('linkins.link.log')
def test_make_linkdir_clean_link(fakelog, **kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
    srcfile = os.path.join(srcdir, 'foo')
    linkfile = os.path.join(linkdir, 'foo')
    with open(srcfile, 'w') as fp:
        fp.write('source content')
    os.symlink(srcfile, linkfile)
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
        clean=True,
    )
    debug = mock.call.debug(
        '{linkfile} exists. Removing.'.format(
            linkfile=linkfile,
        ),
    )
    assert fakelog.mock_calls == [debug]
    assert os.listdir(linkdir) == []
    assert os.path.isfile(srcfile)
    assert not os.path.exists(linkfile)


@tempdirs.makedirs(2)
@mock.patch('linkins.link.log')
def test_make_linkdir_clean_nested_dirs(fakelog, **kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
    srcnesteddir = os.path.join(srcdir, 'foo', 'bar', 'fee', 'fo')
    os.makedirs(srcnesteddir)
    linknesteddir = os.path.join(linkdir, 'foo', 'bar', 'fee', 'fo')
    os.makedirs(linknesteddir)
    srcfile = os.path.join(srcdir, 'foo', 'bar', 'fee', 'fo', 'fi')
    linkfile = os.path.join(linkdir, 'foo', 'bar', 'fee', 'fo', 'fi')
    with open(srcfile, 'w') as fp:
        fp.write('source content')
    os.symlink(srcfile, linkfile)
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
        clean=True,
    )
    debug = mock.call.debug(
        '{linkfile} exists. Removing.'.format(
            linkfile=linkfile,
        ),
    )
    assert fakelog.mock_calls == [debug]
    assert os.listdir(linkdir) == []
    assert os.path.isfile(srcfile)
    assert not os.path.exists(linkfile)


@tempdirs.makedirs(2)
@mock.patch('linkins.link.log')
def test_make_linkdir_clean_dir_exists(fakelog, **kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
    srcfile = os.path.join(srcdir, 'foo')
    linkfile = os.path.join(linkdir, 'foo')
    olddir = os.path.join(linkdir, 'fee')
    os.makedirs(olddir)
    with open(srcfile, 'w') as fp:
        fp.write('source content')
    os.symlink(srcfile, linkfile)
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
        clean=True,
    )
    debug = mock.call.debug(
        '{linkfile} exists. Removing.'.format(
            linkfile=linkfile,
        ),
    )
    assert fakelog.mock_calls == [debug]
    assert os.listdir(linkdir) == ['fee']
    assert os.listdir(olddir) == []
    assert os.path.isfile(srcfile)
    assert not os.path.exists(linkfile)


@tempdirs.makedirs(2)
@mock.patch('linkins.link.log')
def test_make_linkdir_clean_file_exists(fakelog, **kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
    srcfile = os.path.join(srcdir, 'foo')
    linkfile = os.path.join(linkdir, 'foo')
    oldfile = os.path.join(linkdir, 'fee')
    with open(oldfile, 'w') as fp:
        fp.write('old content')
    with open(srcfile, 'w') as fp:
        fp.write('source content')
    os.symlink(srcfile, linkfile)
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
        clean=True,
    )
    debug = mock.call.debug(
        '{linkfile} exists. Removing.'.format(
            linkfile=linkfile,
        ),
    )
    assert fakelog.mock_calls == [debug]
    assert os.listdir(linkdir) == ['fee']
    assert os.path.isfile(oldfile)
    with open(oldfile) as fp:
        assert fp.read() == 'old content'
    assert os.path.isfile(srcfile)
    assert not os.path.exists(linkfile)


@tempdirs.makedirs(2)
@mock.patch('linkins.link.log')
def test_make_linkdir_clean_nested_dir_exists(fakelog, **kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
    nesteddir = os.path.join(srcdir, 'foo')
    os.makedirs(nesteddir)
    srcfile = os.path.join(srcdir, 'foo', 'fee')
    linkfile = os.path.join(linkdir, 'foo', 'fee')
    olddir = os.path.join(linkdir, 'foo', 'fo')
    os.makedirs(olddir)
    with open(srcfile, 'w') as fp:
        fp.write('source content')
    os.symlink(srcfile, linkfile)
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
        clean=True,
    )
    debug = mock.call.debug(
        '{linkfile} exists. Removing.'.format(
            linkfile=linkfile,
        ),
    )
    assert fakelog.mock_calls == [debug]
    assert os.listdir(linkdir) == ['foo']
    foodir = os.path.join(linkdir, 'foo')
    assert os.listdir(foodir) == ['fo']
    assert os.listdir(olddir) == []
    assert os.path.isfile(srcfile)
    assert not os.path.exists(linkfile)


@tempdirs.makedirs(2)
@mock.patch('linkins.link.log')
def test_make_linkdir_clean_nested_file_exists(fakelog, **kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
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
    os.symlink(srcfile, linkfile)
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
        clean=True,
    )
    debug = mock.call.debug(
        '{linkfile} exists. Removing.'.format(
            linkfile=linkfile,
        ),
    )
    assert fakelog.mock_calls == [debug]
    assert os.listdir(linkdir) == ['foo']
    foodir = os.path.join(linkdir, 'foo')
    assert os.listdir(foodir) == ['fo']
    assert os.path.isfile(oldfile)
    with open(oldfile) as fp:
        assert fp.read() == 'old content'
    assert os.path.isfile(srcfile)
    assert not os.path.exists(linkfile)


@tempdirs.makedirs(2)
@mock.patch('linkins.link.log')
def test_make_linkdir_exclude_dir(fakelog, **kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
    srcpath = os.path.join(srcdir, 'foo')
    os.makedirs(srcpath)
    srcfile = os.path.join(srcdir, 'foo', 'bar')
    linkfile = os.path.join(linkdir, 'foo', 'bar')
    with open(srcfile, 'w') as fp:
        fp.write('source content')
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
        exclude=['foo'],
    )
    debug = mock.call.debug(
        'Excluding directory foo'
    )
    assert fakelog.mock_calls == [debug]
    assert os.listdir(linkdir) == []
    assert os.path.isfile(srcfile)
    assert not os.path.exists(linkfile)


@tempdirs.makedirs(2)
@mock.patch('linkins.link.log')
def test_make_linkdir_exclude_file(fakelog, **kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
    srcfile = os.path.join(srcdir, 'foo')
    linkfile = os.path.join(linkdir, 'foo')
    with open(srcfile, 'w') as fp:
        fp.write('source content')
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
        exclude=['foo'],
    )
    debug = mock.call.debug(
        'Excluding file foo'
    )
    assert fakelog.mock_calls == [debug]
    assert os.listdir(linkdir) == []
    assert os.path.isfile(srcfile)
    assert not os.path.exists(linkfile)


@tempdirs.makedirs(2)
@mock.patch('linkins.link.log')
def test_make_linkdir_exclude_nested_dir(fakelog, **kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
    srcnesteddir = os.path.join(srcdir, 'foo', 'bar')
    os.makedirs(srcnesteddir)
    srcfile = os.path.join(srcdir, 'foo', 'bar', 'fee')
    linkfile = os.path.join(linkdir, 'foo', 'bar', 'fee')
    with open(srcfile, 'w') as fp:
        fp.write('source content')
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
        exclude=['foo/bar'],
    )
    debug = mock.call.debug(
        'Excluding directory foo/bar'
    )
    assert fakelog.mock_calls == [debug]
    assert os.listdir(linkdir) == []
    assert os.path.isfile(srcfile)
    assert not os.path.exists(linkfile)


@tempdirs.makedirs(2)
@mock.patch('linkins.link.log')
def test_make_linkdir_exclude_nested_file(fakelog, **kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
    srcnesteddir = os.path.join(srcdir, 'foo', 'bar')
    os.makedirs(srcnesteddir)
    srcfile = os.path.join(srcdir, 'foo', 'bar', 'fee')
    linkfile = os.path.join(linkdir, 'foo', 'bar', 'fee')
    with open(srcfile, 'w') as fp:
        fp.write('source content')
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
        exclude=['foo/bar/fee'],
    )
    debug = mock.call.debug(
        'Excluding file foo/bar/fee'
    )
    assert fakelog.mock_calls == [debug]
    assert os.listdir(linkdir) == []
    assert os.path.isfile(srcfile)
    assert not os.path.exists(linkfile)


@tempdirs.makedirs(2)
@mock.patch('linkins.link.log')
def test_make_linkdir_exclude_many_files(fakelog, **kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
    srcnesteddir = os.path.join(srcdir, 'foo', 'bar')
    os.makedirs(srcnesteddir)
    linknesteddir = os.path.join(linkdir, 'foo')
    os.makedirs(linknesteddir)
    linkfee = os.path.join(linkdir, 'foo', 'bar', 'fee')
    srcfee = os.path.join(srcdir, 'foo', 'bar', 'fee')
    with open(srcfee, 'w') as fp:
        fp.write('fee source content')
    srcfi = os.path.join(srcdir, 'foo', 'fi')
    linkfi = os.path.join(linkdir, 'foo', 'fi')
    with open(srcfi, 'w') as fp:
        fp.write('fi source content')
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
        exclude=['foo/bar'],
    )
    debug = mock.call.debug(
        'Excluding directory foo/bar'
    )
    assert fakelog.mock_calls == [debug]
    assert os.listdir(linkdir) == ['foo']
    foodir = os.path.join(linkdir, 'foo')
    assert os.listdir(foodir) == ['fi']
    assert os.path.isfile(srcfi)
    assert os.path.islink(linkfi)
    assert os.path.isfile(srcfee)
    assert not os.path.exists(linkfee)


@tempdirs.makedirs(2)
@mock.patch('linkins.link.log')
def test_make_linkdir_exclude_multiple(fakelog, **kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
    linkbar = os.path.join(linkdir, 'bar')
    srcbar = os.path.join(srcdir, 'bar')
    with open(srcbar, 'w') as fp:
        fp.write('fee source content')
    srcfoo = os.path.join(srcdir, 'foo')
    linkfoo = os.path.join(linkdir, 'foo')
    with open(srcfoo, 'w') as fp:
        fp.write('fi source content')
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
        exclude=['foo', 'bar'],
    )
    debugfoo = mock.call.debug(
        'Excluding file foo'
    )
    debugbar = mock.call.debug(
        'Excluding file bar'
    )
    assert fakelog.mock_calls == [debugbar, debugfoo]
    assert os.listdir(linkdir) == []
    assert os.path.isfile(srcbar)
    assert os.path.isfile(srcfoo)
    assert not os.path.exists(linkbar)
    assert not os.path.exists(linkfoo)


@tempdirs.makedirs(2)
@mock.patch('linkins.link.log')
def test_make_linkdir_exclude_empty(fakelog, **kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
    srcfile = os.path.join(srcdir, 'foo')
    linkfile = os.path.join(linkdir, 'foo')
    with open(srcfile, 'w') as fp:
        fp.write('source content')
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
        exclude=[],
    )
    assert fakelog.mock_calls == []
    assert os.listdir(linkdir) == ['foo']
    assert os.path.isfile(srcfile)
    assert os.path.islink(linkfile)


@tempdirs.makedirs(2)
@mock.patch('linkins.link.log')
def test_make_linkdir_exclude_other(fakelog, **kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
    srcfile = os.path.join(srcdir, 'foo')
    linkfile = os.path.join(linkdir, 'foo')
    with open(srcfile, 'w') as fp:
        fp.write('source content')
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
        exclude=['fee'],
    )
    assert fakelog.mock_calls == []
    assert os.listdir(linkdir) == ['foo']
    assert os.path.isfile(srcfile)
    assert os.path.islink(linkfile)


@tempdirs.makedirs(2)
@mock.patch('linkins.link.log')
def test_make_linkdir_exclude_clean(fakelog, **kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
    srcfile = os.path.join(srcdir, 'foo')
    linkfile = os.path.join(linkdir, 'foo')
    with open(srcfile, 'w') as fp:
        fp.write('source content')
    os.symlink(srcfile, linkfile)
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
        exclude=['foo'],
        clean=True,
    )
    debug = mock.call.debug(
        'Excluding file foo',
    )
    assert fakelog.mock_calls == [debug]
    assert os.listdir(linkdir) == ['foo']
    assert os.path.isfile(srcfile)
    assert os.path.islink(linkfile)


@tempdirs.makedirs(2)
@mock.patch('linkins.link.log')
@mock.patch('linkins.script.runscript')
def test_make_linkdir_exclude_script(fakerun, fakelog, **kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
    scriptfile = os.path.join(srcdir, 'foo-script')
    with open(scriptfile, 'w') as fp:
        fp.write('script content')
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
        scriptname='foo-script',
        runscript=True,
        exclude=['foo-script'],
    )
    assert fakerun.mock_calls == []
    debug = mock.call.debug(
        'Excluding file foo-script'
    )
    assert fakelog.mock_calls == [debug]
    assert os.listdir(linkdir) == []


@tempdirs.makedirs(2)
@mock.patch('linkins.link.log')
def test_make_linkdir_exclude_dir_regex(fakelog, **kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
    srcpath = os.path.join(srcdir, 'foo')
    os.makedirs(srcpath)
    srcfile = os.path.join(srcdir, 'foo', 'bar')
    linkfile = os.path.join(linkdir, 'foo', 'bar')
    with open(srcfile, 'w') as fp:
        fp.write('source content')
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
        exclude=['f.*'],
    )
    debug = mock.call.debug(
        'Excluding directory foo'
    )
    assert fakelog.mock_calls == [debug]
    assert os.listdir(linkdir) == []
    assert os.path.isfile(srcfile)
    assert not os.path.exists(linkfile)


@tempdirs.makedirs(2)
@mock.patch('linkins.link.log')
def test_make_linkdir_exclude_file_regex(fakelog, **kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
    srcfile = os.path.join(srcdir, 'foo')
    linkfile = os.path.join(linkdir, 'foo')
    with open(srcfile, 'w') as fp:
        fp.write('source content')
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
        exclude=['f.*'],
    )
    debug = mock.call.debug(
        'Excluding file foo'
    )
    assert fakelog.mock_calls == [debug]
    assert os.listdir(linkdir) == []
    assert os.path.isfile(srcfile)
    assert not os.path.exists(linkfile)


@tempdirs.makedirs(2)
@mock.patch('linkins.link.log')
def test_make_linkdir_exclude_file_regex_other(fakelog, **kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
    srcfile = os.path.join(srcdir, 'foo')
    linkfile = os.path.join(linkdir, 'foo')
    with open(srcfile, 'w') as fp:
        fp.write('source content')
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
        exclude=['fe.*'],
    )
    assert fakelog.mock_calls == []
    assert os.listdir(linkdir) == ['foo']
    assert os.path.isfile(srcfile)
    assert os.path.islink(linkfile)


@tempdirs.makedirs(2)
@mock.patch('linkins.link.log')
def test_make_linkdir_exclude_file_regex_complex(fakelog, **kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
    srcfile = os.path.join(srcdir, 'foo_bar_me')
    linkfile = os.path.join(linkdir, 'foo_bar_me')
    with open(srcfile, 'w') as fp:
        fp.write('source content')
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
        exclude=['^foo.*me$'],
    )
    debug = mock.call.debug(
        'Excluding file foo_bar_me'
    )
    assert fakelog.mock_calls == [debug]
    assert os.listdir(linkdir) == []
    assert os.path.isfile(srcfile)
    assert not os.path.exists(linkfile)


@tempdirs.makedirs(2)
@mock.patch('linkins.link.log')
def test_make_linkdir_exclude_file_regex_nested(fakelog, **kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
    srcnesteddir = os.path.join(srcdir, 'foo', 'bar')
    os.makedirs(srcnesteddir)
    srcfile = os.path.join(srcdir, 'foo', 'bar', 'fee')
    linkfile = os.path.join(linkdir, 'foo', 'bar', 'fee')
    with open(srcfile, 'w') as fp:
        fp.write('source content')
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
        exclude=['foo.*b.*/fee'],
    )
    debug = mock.call.debug(
        'Excluding file foo/bar/fee'
    )
    assert fakelog.mock_calls == [debug]
    assert os.listdir(linkdir) == []
    assert os.path.isfile(srcfile)
    assert not os.path.exists(linkfile)


@tempdirs.makedirs(2)
@mock.patch('linkins.link.log')
def test_make_linkdir_exclude_file_regex_many_files(fakelog, **kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
    srcfoo = os.path.join(srcdir, 'foo')
    linkfoo = os.path.join(linkdir, 'foo')
    srcbar = os.path.join(srcdir, 'bar')
    linkbar = os.path.join(linkdir, 'bar')
    with open(srcfoo, 'w') as fp:
        fp.write('foo source content')
    with open(srcbar, 'w') as fp:
        fp.write('bar source content')
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
        exclude=['^f.*$'],
    )
    debug = mock.call.debug(
        'Excluding file foo'
    )
    assert fakelog.mock_calls == [debug]
    assert os.listdir(linkdir) == ['bar']
    assert os.path.isfile(srcbar)
    assert os.path.islink(linkbar)
    assert os.path.isfile(srcfoo)
    assert not os.path.exists(linkfoo)


@tempdirs.makedirs(2)
@mock.patch('linkins.link.log')
def test_make_linkdir_exclude_file_regex_multiple(fakelog, **kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
    srcfoo = os.path.join(srcdir, 'foo')
    linkfoo = os.path.join(linkdir, 'foo')
    srcbar = os.path.join(srcdir, 'bar')
    linkbar = os.path.join(linkdir, 'bar')
    with open(srcfoo, 'w') as fp:
        fp.write('foo source content')
    with open(srcbar, 'w') as fp:
        fp.write('bar source content')
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
        exclude=['^f.*$', 'b.*'],
    )
    bardebug = mock.call.debug(
        'Excluding file bar'
    )
    foodebug = mock.call.debug(
        'Excluding file foo'
    )
    assert fakelog.mock_calls == [bardebug, foodebug]
    assert os.listdir(linkdir) == []
    assert os.path.isfile(srcbar)
    assert not os.path.exists(linkbar)
    assert os.path.isfile(srcfoo)
    assert not os.path.exists(linkfoo)


@tempdirs.makedirs(2)
@mock.patch('linkins.link.log')
def test_make_linkdir_include_dir(fakelog, **kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
    srcpath = os.path.join(srcdir, 'foo')
    os.makedirs(srcpath)
    srcfile = os.path.join(srcdir, 'foo', 'bar')
    linkfile = os.path.join(linkdir, 'foo', 'bar')
    with open(srcfile, 'w') as fp:
        fp.write('source content')
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
        include=['foo'],
    )
    assert fakelog.mock_calls == []
    assert os.listdir(linkdir) == ['foo']
    foodir = os.path.join(linkdir, 'foo')
    assert os.listdir(foodir) == ['bar']
    assert os.path.isfile(srcfile)
    assert os.path.islink(linkfile)


@tempdirs.makedirs(2)
@mock.patch('linkins.link.log')
def test_make_linkdir_include_file(fakelog, **kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
    srcfile = os.path.join(srcdir, 'foo')
    linkfile = os.path.join(linkdir, 'foo')
    with open(srcfile, 'w') as fp:
        fp.write('source content')
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
        include=['foo'],
    )
    assert fakelog.mock_calls == []
    assert os.listdir(linkdir) == ['foo']
    assert os.path.isfile(srcfile)
    assert os.path.islink(linkfile)


@tempdirs.makedirs(2)
@mock.patch('linkins.link.log')
def test_make_linkdir_include_dir_regex(fakelog, **kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
    srcpath = os.path.join(srcdir, 'foo')
    os.makedirs(srcpath)
    srcfile = os.path.join(srcdir, 'foo', 'bar')
    linkfile = os.path.join(linkdir, 'foo', 'bar')
    with open(srcfile, 'w') as fp:
        fp.write('source content')
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
        include=['f.*'],
    )
    assert fakelog.mock_calls == []
    assert os.listdir(linkdir) == ['foo']
    foodir = os.path.join(linkdir, 'foo')
    assert os.listdir(foodir) == ['bar']
    assert os.path.isfile(srcfile)
    assert os.path.islink(linkfile)


@tempdirs.makedirs(2)
@mock.patch('linkins.link.log')
def test_make_linkdir_include_file_regex(fakelog, **kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
    srcfile = os.path.join(srcdir, 'foo')
    linkfile = os.path.join(linkdir, 'foo')
    with open(srcfile, 'w') as fp:
        fp.write('source content')
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
        include=['f.*'],
    )
    assert fakelog.mock_calls == []
    assert os.listdir(linkdir) == ['foo']
    assert os.path.isfile(srcfile)
    assert os.path.islink(linkfile)


@tempdirs.makedirs(2)
@mock.patch('linkins.link.log')
def test_make_linkdir_include_empty(fakelog, **kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
    srcfile = os.path.join(srcdir, 'foo')
    linkfile = os.path.join(linkdir, 'foo')
    with open(srcfile, 'w') as fp:
        fp.write('source content')
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
        include=[],
    )
    assert fakelog.mock_calls == []
    assert os.listdir(linkdir) == ['foo']
    assert os.path.isfile(srcfile)
    assert os.path.islink(linkfile)


@tempdirs.makedirs(2)
@mock.patch('linkins.link.log')
def test_make_linkdir_include_other(fakelog, **kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
    srcfile = os.path.join(srcdir, 'foo')
    linkfile = os.path.join(linkdir, 'foo')
    with open(srcfile, 'w') as fp:
        fp.write('source content')
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
        include=['fee'],
    )
    assert fakelog.mock_calls == []
    assert os.listdir(linkdir) == ['foo']
    assert os.path.isfile(srcfile)
    assert os.path.islink(linkfile)


@tempdirs.makedirs(2)
@mock.patch('linkins.link.log')
def test_make_linkdir_include_exclude_dir(fakelog, **kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
    srcpath = os.path.join(srcdir, 'foo')
    os.makedirs(srcpath)
    srcfile = os.path.join(srcdir, 'foo', 'bar')
    linkfile = os.path.join(linkdir, 'foo', 'bar')
    with open(srcfile, 'w') as fp:
        fp.write('source content')
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
        exclude=['foo'],
        include=['foo'],
    )
    assert fakelog.mock_calls == []
    assert os.listdir(linkdir) == ['foo']
    foodir = os.path.join(linkdir, 'foo')
    assert os.listdir(foodir) == ['bar']
    assert os.path.isfile(srcfile)
    assert os.path.islink(linkfile)


@tempdirs.makedirs(2)
@mock.patch('linkins.link.log')
def test_make_linkdir_include_exclude_file(fakelog, **kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
    srcfile = os.path.join(srcdir, 'foo')
    linkfile = os.path.join(linkdir, 'foo')
    with open(srcfile, 'w') as fp:
        fp.write('source content')
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
        exclude=['foo'],
        include=['foo'],
    )
    assert fakelog.mock_calls == []
    assert os.listdir(linkdir) == ['foo']
    assert os.path.isfile(srcfile)
    assert os.path.islink(linkfile)


@tempdirs.makedirs(2)
@mock.patch('linkins.link.log')
def test_make_linkdir_include_multiple_exclude(fakelog, **kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
    linkbar = os.path.join(linkdir, 'bar')
    srcbar = os.path.join(srcdir, 'bar')
    with open(srcbar, 'w') as fp:
        fp.write('fee source content')
    srcfoo = os.path.join(srcdir, 'foo')
    linkfoo = os.path.join(linkdir, 'foo')
    with open(srcfoo, 'w') as fp:
        fp.write('fi source content')
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
        exclude=['foo'],
        include=['foo', 'bar'],
    )
    assert fakelog.mock_calls == []
    assert sorted(os.listdir(linkdir)) == sorted(['foo', 'bar'])
    assert os.path.isfile(srcbar)
    assert os.path.isfile(srcfoo)
    assert os.path.islink(linkbar)
    assert os.path.islink(linkfoo)


@tempdirs.makedirs(2)
@mock.patch('linkins.link.log')
def test_make_linkdir_include_exclude_multiple(fakelog, **kwargs):
    (srcdir, linkdir) = kwargs['tempdirs_dirs']
    linkbar = os.path.join(linkdir, 'bar')
    srcbar = os.path.join(srcdir, 'bar')
    with open(srcbar, 'w') as fp:
        fp.write('bar source content')
    srcfoo = os.path.join(srcdir, 'foo')
    linkfoo = os.path.join(linkdir, 'foo')
    with open(srcfoo, 'w') as fp:
        fp.write('foo source content')
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
        exclude=['foo', 'bar'],
        include=['bar'],
    )
    debug = mock.call.debug(
        'Excluding file foo'
    )
    assert fakelog.mock_calls == [debug]
    assert os.listdir(linkdir) == ['bar']
    assert os.path.isfile(srcbar)
    assert os.path.isfile(srcfoo)
    assert os.path.islink(linkbar)
    assert not os.path.exists(linkfoo)
