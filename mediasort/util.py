import magic
import filetype
from enum import Enum

class Safety(Enum):
    SAFE = 1
    UNSAFE = 2
    IDENTICAL = 3


def get_mimetype(path):
    """ Get the mimetype of the given file pointer.
        @param  path    Path to a file to get the MIME for.
        @return     A string representing the mimetype or `None` if no MIME
                    coul be discerned. """
    guess = filetype.guess(path)

    if guess:
        return guess.mime

    # If we were unable to guess the MIME, attempt to use filemagic.
    with magic.Magic() as m:
        return m.id_filename(path)

def is_video(mime):
    """ Returns `True` if the specified file pointer represents a video.
        `False` otherwise. """
    return mime.startswith("video/")


def is_photo(mime):
    """ Returns `True` if the specified file pointer represents a photo.
        `False` otherwise. """
    return mime.startswith("image/")
