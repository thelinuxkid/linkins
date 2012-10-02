=======
linkins
=======

Description
===========

linkins is a command line tool which allows users to link a directory
structure. It provides the ability to execute user-defined scripts at
each level of the directory hierarchy and a safe way to backup
existing files or directories.

Installation
============

You can use pip or easy_install

- pip install linkins
- easy_install linkins

Usage
=====

The linkins runnable takes two positional arguments: the directory which has the files to link and the destination directory. These show up in the help messages as TARGET_DIR and LINK_DIR, respectively::

    linkins TARGET_DIR LINK_DIR

For more information on usage you can run linkins with the --help argument::

    linkins --help
