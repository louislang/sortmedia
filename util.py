import magic
from enum import Enum

class Safety(Enum):
    SAFE = 1
    UNSAFE = 2
    IDENTICAL = 3

def get_mimetype(fp):
    """ Get the mimetype of the given file pointer. 
    
        @param  fp  The file pointer to process. 
        
        @return     A string representing the mimetype. """
    mimetype = None
    with magic.Magic(flags=magic.MAGIC_MIME_TYPE) as m:
        mimetype = m.id_buffer(fp.read(512))
        fp.seek(0)

    return mimetype

def is_video(mime):
    """ Returns `True` if the specified file pointer represents a video.
        `False` otherwise. """
    return mime.startswith("video/")

def is_photo(mime):
    """ Returns `True` if the specified file pointer represents a photo.
        `False` otherwise. """
    return mime.startswith("image/")
