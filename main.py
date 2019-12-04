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

    def __init__(self, copy=False):
        """ """
        logger.info(f"Mode: {'Copy' if copy else 'Move'}")
        self.copy = copy 

    def process_files(self, src, dst):
        """ """
        if not os.path.isdir(src):
            logger.error(f"The specified source director `{src}` doest " +
                          "not exist.")
            return

        for f in Path(src).rglob("*"):
            path = f.as_posix()
            logger.info(path)
            mime = get_mimetype(path)
            obj = None

            if is_video(mime):
                obj = Video(path, mime) 
            elif is_photo(mime):
                obj = Photo(path, mime)

            if obj:
                if not self.copy:
                    obj.move(dst)
                else:
                    obj.copy(dst)

parser = argparse.ArgumentParser()
parser.add_argument('-c','--copy', help='Copy instead of move files.', required=False, default=False)
parser.add_argument('src', nargs='+', help='The media source directory to process.')
parser.add_argument('dst', nargs='+', help='The destination directory to move or copy files.')
args = parser.parse_args()

src = args.src[0]
dst = args.dst[0]

ms = MediaSort(copy=args.copy)
ms.process_files(src, dst)
