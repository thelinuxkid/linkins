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
        help='the path to the directory structure to be linked',
    )
    parser.add_argument(
        'linkdir',
        metavar='LINK_DIR',
        type=str,
        help='the path to the directory where the links are to be created',
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        default=False,
        help='output DEBUG logging statements (default: %(default)s)',
        )
    parser.add_argument(
        '-s',
        '--script',
        default='linkins-script',
        type=str,
        help=(
            'Name of the script that can be executed at each level '
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
            'Run the script (defined by --script) at each level of the '
            'target directory hierarchy it is found (default: '
            '%(default)s)'
            ),
        )
    parser.add_argument(
        '-p',
        '--replace',
        action='store_true',
        default=False,
        help='Replace existing links (default: %(default)s)',
        )
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format='%(asctime)s.%(msecs)03d %(name)s: %(levelname)s: %(message)s',
        datefmt='%Y-%m-%dT%H:%M:%S',
        )

    srcdir = util.abs_path(args.srcdir)
    linkdir = util.abs_path(args.linkdir)
    log.debug(
        'Creating links from "{srcdir}" to "{linkdir}"...'.format(
            srcdir=srcdir,
            linkdir=linkdir,
        )
    )
    link.make(
        srcdir=srcdir,
        linkdir=linkdir,
        scriptname=args.script,
        runscript=args.run,
        replace=args.replace,
        )
