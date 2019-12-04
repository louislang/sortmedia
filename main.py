import os
import logging
import argparse

from pathlib import Path
from mediasort.util import *
from mediasort.photo import Photo
from mediasort.video import Video

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class MediaSort:
    """ """

    def __init__(self, dry=False, copy=False):
        """ """
        logger.info(f"Dry Run: {'Yes' if dry else 'No'}")
        logger.info(f"Mode: {'Copy' if copy else 'Move'}")
        self.copy = copy 
        self.dry_run = dry

    def process_files(self, src, dst):
        """ """
        if not os.path.isdir(src):
            logger.error(f"The specified source director `{src}` doest " +
                          "not exist.")
            return

        total_photos = 0
        total_videos = 0
        total_duplicates = 0

        for f in Path(src).rglob("*"):
            path = f.as_posix()
            mime = get_mimetype(path)
            obj = None

            if is_video(mime):
                obj = Video(path, mime) 
                total_videos = total_videos + 1
            elif is_photo(mime):
                obj = Photo(path, mime)
                total_photos = total_photos + 1

            if obj:
                if self.dry_run:
                    logger.info(path)
                else:
                    took_action = False
                    if not self.copy:
                        took_action = obj.move(dst)
                    else:
                        took_action = obj.copy(dst)

                    if not took_action:
                        total_duplicates = total_duplicates + 1
                    logger.info(f"{path}{' -- DUPLICATE' if not took_action else ''}")

        logger.info(f"Processed {total_photos+total_videos} files")
        logger.info(f"\tTotal videos...: {total_videos}")
        logger.info(f"\tTotal photos...: {total_photos}")
        logger.info(f"\tDuplicates.....: {total_duplicates}")

parser = argparse.ArgumentParser()
parser.add_argument('-c','--copy', action='store_true', help='Copy instead of move files.', required=False, default=False)
parser.add_argument('-d', '--dry', action='store_true', help='Dry run - do not actually process files', required=False, default=False)
parser.add_argument('src', nargs='+', help='The media source directory to process.')
parser.add_argument('dst', nargs='+', help='The destination directory to move or copy files.')
args = parser.parse_args()

src = args.src[0]
dst = args.dst[0]

ms = MediaSort(dry=args.dry, copy=args.copy)
ms.process_files(src, dst)
