import argparse

from mediasort.photo import Photo
from mediasort.video import Video
from mediasort.util import is_video, is_photo, get_mimetype
from mediasort.sort import MediaSort

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
                    nargs='+',
                    help='List of directories to move but not recurse into ' +
                         'for processing')
parser.add_argument('-e',
                    '--excludes',
                    nargs='+',
                    help='List of directories to skip completely')

args = parser.parse_args()

src = args.src[0]
dst = args.dst[0]

ms = MediaSort(dry=args.dry, 
               copy=args.copy,
               noprocess=args.noprocess,
               excludes=args.excludes)
ms.process_files(src, dst)
