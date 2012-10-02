import os

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

def test_make_bad_target():
    res = pytest.raises(
        ValueError,
        link.make,
        srcdir='',
        linkdir='',
        )
    assert res.type == ValueError
    assert res.value.message == 'Link directory "" does not exist'

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
