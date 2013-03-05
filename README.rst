=======
linkins
=======

Description
===========

linkins is a command line tool which allows users to link a directory
structure. It provides the ability to execute user-defined scripts at
each level of the directory hierarchy.

Installation
============

Install using pip::

    pip install linkins

or easy_install::

    easy_install linkins

Usage
=====

The linkins command takes two positional arguments: a list of
directories which have the files to link and the destination
directory. These show up in the help messages as TARGET_DIR and
LINK_DIR, respectively::

    linkins TARGET_DIR [TARGET_DIR ...] LINK_DIR

It also supports a number of optional arguments. To see all the
supported options you can invoke the help menu::

    linkins --help

Running scripts
===============

*Scripts are not run be default. In order to run your scripts you must
pass the -r or --run option.*

Linkins can run custom scripts at each directory. The only requirement
is that the script name be the same everywhere. By default, linkins
looks for scripts named linkins-script. But, the script name can be
changed with the --script option. An example of a TARGET_DIR with
scripts would be::

    TARGET_DIR/
    |-- .bashrc
    |-- .emacs
    |-- linkins-script
    |-- .emacs.d
    |   |-- linkins-script
    |   |-- wc.el
    |-- .xmonad
    |   |-- xmonad.hs

Scripts must be executable. In Linux that means the executable bit
must be set::

    chmod +x SCRIPT_NAME

Scripts are not linked or copied to LINK_DIR. Instead, and for
convenience, linkins passes three positional arguments to the script:
TARGET_DIR, LINK_DIR and a relative path from TARGET_DIR to the
script's parent directory. All paths are absolute except for the last
positional argument just described. This includes the script
itself. For example, the two scripts in the example above would be
called like::

    TARGET_DIR/linkins-script TARGET_DIR LINKS_DIR .
    ...
    TARGET_DIR/.emacs.d/linkins-script TARGET_DIR LINKS_DIR .emacs.d

If the directory which mirrors the script's parent directory in the
LINK_DIR side does not exist linkdirs will create it.

Any files in the same directory as the script are always linked before
the script is run.

Multiprocessing
---------------

You can run each script as a separate process by using the -m
or --multiprocess option. However, you must be aware of the
consequences. For example, if you have two scripts that install
packages from apt-get one of them will likely fail because it will not
be able to obtain the dpkg lock.

Output
------

A script's output is redirected to linkins' log and is logged at level
INFO. A script log line has the following form::

    SCRIPT: STREAM: MSG

where SCRIPT is the relative path from TARGET_DIR to the script,
STREAM is one of STDOUT or STDERR (depending on the stream the script
outputted to) and MSG is the message outputted by the script.

If the -q option is used the script's output will be not be shown.

Command line options
====================

--exclude
---------

The --exclude option takes a list of arguments separated by
whitespace. These arguments can be paths or regular expressions. Any
directories or files in TARGET_DIR which match the arguments will be
excluded from the operation. You can use --exclude in conjunction with
any other operation.

--include
---------

Without the --exclude option, this option doesn't have much use. You
can use it to *not exclude* directories or files. Like --exclude it
takes a list of arguments separated by whitespace which can be either
paths or regular expressions.

--replace
---------

You can use the --replace option to delete and relink links which
already exist in LINK_DIR. Only links which link to files in
TARGET_DIR will be replaced. Any other directories, files or links in
LINK_DIR will be left untouched.

--clean
-------

You can use the --clean option to delete links which already exist in
LINK_DIR. Only links which link to files in TARGET_DIR will be
replaced. Any other directories, files or links in LINK_DIR will be
left untouched. This operation has precedence over replacing links and
running scripts. --clean will also remove empty parent directories.

Developing
==========

External dependencies
---------------------

    - python-dev
    - python-setuptools
    - python-virtualenv

Setup
-----

To start developing run the following commands from the project's base
directory. You can download the source from
https://github.com/thelinuxkid/linkins::

    # I like to install the virtual environment in a hidden repo.
    virtualenv .virtual
    # I leave the magic to Ruby developers (.virtual/bin/activate)
    .virtual/bin/python setup.py develop
    # At this point, linkins will already be in easy-install.pth.
    # So, pip will not attempt to download it
    .virtual/bin/pip install linkins[test]

If you like to use ipython you can install it with the dev
requirement::

    .virtual/bin/pip install linkins[dev]

Testing
-------

To run the unit-tests run the following command from the project's
base directory::

    .virtual/bin/py.test
