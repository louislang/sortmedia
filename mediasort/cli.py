import argparse
from mediasort.sort import MediaSort


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c',
                        '--copy',
                        action='store_true',
                        help='Copy instead of move files',
                        required=False,
                        default=False)
    parser.add_argument('-d',
                        '--dry',
                        action='store_true',
                        help='Dry run - do not actually process files',
                        required=False,
                        default=False)
    parser.add_argument('src',
                        nargs='+',
                        help='The media source directory to process')
    parser.add_argument('dst',
                        nargs='+',
                        help='The destination directory to move or copy files')
    parser.add_argument('-n',
                        '--noprocess',
                        help='List of directories to move but not recurse into ' +
                             'for processing',
                        type=str)
    parser.add_argument('-e',
                        '--excludes',
                        help='List of directories to skip completely',
                        type=str)

    args = parser.parse_args()

    src = args.src[0]
    dst = args.dst[0]

    if args.noprocess:
        args.noprocess = [x for x in args.noprocess.split(',')]

    if args.excludes:
        args.excludes = [x for x in args.excludes.split(',')]

    ms = MediaSort(dry=args.dry, 
                   copy=args.copy,
                   noprocess=args.noprocess,
                   excludes=args.excludes)
    ms.process_files(src, dst)
