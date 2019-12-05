import os
import logging

from pathlib import Path
from mediasort.photo import Photo
from mediasort.video import Video
from mediasort.util import is_video, is_photo, get_mimetype

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class MediaSort:
    """ Handles processing the specified source path. """

    def __init__(self, dry=False, copy=False, noprocess=[], excludes=[]):
        """ Initialize a new media sorter.
        
            @param  dry         Print out files that would be processed without
                                actually processing anything.
            @param  copy        Copy instead of move files.
            @param  noprocess   List of directories to skip processing, but
                                still move.
            @param  excludes    List of directories to not process. """
        logger.info(f"Dry Run: {'Yes' if dry else 'No'}")
        logger.info(f"Mode: {'Copy' if copy else 'Move'}")
        self.copy = copy
        self.dry_run = dry
        self.noprocess = noprocess
        self.excludes = excludes

    def process_files(self, src, dst):
        """ Kick off processing.
        
            @param  src     The source directory to process.
            @param  dst     The destination to move files to. """
        if not os.path.isdir(src):
            logger.error(f"The specified source director `{src}` doest not " +
                         "exist.")
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

                    detail = ' -- DUPLICATE' if not took_action else ''
                    logger.info(f"{path}{detail}")

        logger.info(f"Processed {total_photos+total_videos} files")
        logger.info(f"\tTotal videos...: {total_videos}")
        logger.info(f"\tTotal photos...: {total_photos}")
        logger.info(f"\tDuplicates.....: {total_duplicates}")
