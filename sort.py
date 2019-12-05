from mediasort.photo import Photo
from mediasort.video import Video
from mediasort.util import is_video, is_photo, get_mimetype
from mediasort.sort import MediaSort

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument('-c',
                    '--copy',
                    action='store_true',
                    help='Copy instead of move files.',
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
                    help='The media source directory to process.')
parser.add_argument('dst',
                    nargs='+',
                    help='The destination directory to move or copy files.')
args = parser.parse_args()

src = args.src[0]
dst = args.dst[0]

ms = MediaSort(dry=args.dry, copy=args.copy)
ms.process_files(src, dst)
