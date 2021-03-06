import argparse
import logging

from linkins import link, util

log = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            'Link a directory structure, execute user-defined '
            'scripts and safely backup existing files'
        )
    )
    parser.add_argument(
        'srcdir',
        metavar='TARGET_DIR',
        type=str,
        nargs='+',
        help='path(s) to the directory structure to be linked',
    )
    parser.add_argument(
        'linkdir',
        metavar='LINK_DIR',
        type=str,
        help='path to the directory where the links are to be created',
    )
    parser.add_argument(
        '-s',
        '--script',
        default='linkins-script',
        type=str,
        help=(
            'name of the script that can be executed at each level '
            'of the target directory hierarchy. Scripts are never '
            'linked (default: %(default)s)'
        ),
    )
    parser.add_argument(
        '-r',
        '--run',
        action='store_true',
        default=False,
        help=(
            'run the script (defined by --script) at each level of the '
            'target directory hierarchy it is found (default: '
            '%(default)s)'
        ),
    )
    parser.add_argument(
        '-f',
        '--force',
        action='store_true',
        default=False,
        help='replace existing links (default: %(default)s)',
    )
    parser.add_argument(
        '-c',
        '--clean',
        action='store_true',
        default=False,
        help=(
            'remove existing links (and their empty parent '
            'directories). Supersedes --force and --run '
            '(default: %(default)s)'
        ),
    )
    parser.add_argument(
        '-m',
        '--multiprocess',
        action='store_true',
        default=False,
        help='run scripts as subprocesses (default: %(default)s)',
    )
    parser.add_argument(
        '-e',
        '--exclude',
        metavar='PATTERN',
        type=str,
        nargs='+',
        help='exclude files matching PATTERN from all operations'
    )
    parser.add_argument(
        '-i',
        '--include',
        metavar='PATTERN',
        type=str,
        nargs='+',
        help='do not exclude files matching PATTERN from all operations'
    )
    loggroup = parser.add_mutually_exclusive_group()
    loggroup.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        default=False,
        help='output DEBUG logging statements (default: %(default)s)',
    )
    loggroup.add_argument(
        '-q',
        '--quiet',
        action='store_true',
        default=False,
        help=(
            'only output ERROR and FATAL logging statements '
            '(default: %(default)s)'
        )
    )
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    level = logging.INFO
    # Only one of verbose and quiet will be set
    if args.verbose:
        level = logging.DEBUG
    if args.quiet:
        level = logging.ERROR
    logging.basicConfig(
        level=level,
        format='%(name)s: %(levelname)s: %(message)s',
    )

    srcdirs = args.srcdir
    linkdir = util.abs_path(args.linkdir)
    for srcdir in srcdirs:
        srcdir = util.abs_path(srcdir)
        log.debug(
            'Processing links from "{srcdir}" to "{linkdir}"...'.format(
                srcdir=srcdir,
                linkdir=linkdir,
            )
        )
        link.make(
            srcdir=srcdir,
            linkdir=linkdir,
            scriptname=args.script,
            runscript=args.run,
            force=args.force,
            clean=args.clean,
            multiprocess=args.multiprocess,
            exclude=args.exclude,
            include=args.include,
        )
