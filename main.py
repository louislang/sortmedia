from util import *
from photo import Photo
from pathlib import Path

for f in Path("test/").rglob("*"):
    path = f.as_posix()
    obj = None

    f = open(path, 'rb')
    obj = None
    
    mime = get_mimetype(f) 

    if is_video(mime):
        #obj = Video(f, path, mime)
        print("Video not supported!")
    elif is_photo(mime):
        obj = Photo(f, path, mime)

    if obj:
        obj.copy('foo/')
