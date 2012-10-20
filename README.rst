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

    pip install pyusps

or easy_install::

    easy_install pyusps

Usage
=====

The linkins command takes two positional arguments: the directory
which has the files to link and the destination directory. These show
up in the help messages as TARGET_DIR and LINK_DIR, respectively::

    linkins TARGET_DIR LINK_DIR

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

Output
------

TODO

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

    # I like to install the virtual environment in its own
    # hidden repo but you don't have to
    virtualenv .virtual
    # I leave the magic to Ruby developers (.virtual/bin/activate)
    # but you don't have to agree with me
    .virtual/bin/python setup.py develop
    # Install the testing dependecies. Pip doesn't seem to handle
    # extras_require yet: https://github.com/pypa/pip/issues/7.
    # So, use easy_install.
    # At this point, linkins will already be in easy-install.pth.
    # So easy_install will not attempt to download it
    .virtual/bin/easy_install linkins[test]

If you like to use ipython you can install it with the dev
requirement::

    .virtual/bin/easy_install linkins[dev]

Testing
-------

To run the unit-tests run the following command from the project's
base directory::

    .virtual/bin/py.test
