import os 
import shutil
import hashlib
import logging

from util import Safety
from abc import ABC, abstractmethod

logger = logging.getLogger('file')
logging.basicConfig(level=logging.INFO)

class File(ABC):
    """ Represents a file on disk. Provides facilities for hashing the file,
        and pulling EXIF data while minimizing the number of times we read the
        file data. """

    def __init__(self, fp, path, mime, exif=None):
        """ Creates a new file pointer for processing. 
            
            @param  path    The path to the file. """
        if not path or not isinstance(path, str):
            raise ValueError(f"Path must be a non-empty string. Got `{path}`.")

        if not os.path.isfile(path):
            raise RuntimeError(f"{path} does not exist.")

        self.fp = fp 
        self.path = path
        self.hash = self.get_hash()
        self.exif = None 
        self.mime = mime 

        super().__init__()

    def __del__(self):
        """ Close the file pointer on object destruct. """
        self.fp.close()

    def get_hash(self):
        """ Returns the SHA256 file hash. """
        m = hashlib.sha256()
        m.update(self.fp.read())
        h = m.digest()
        self.fp.seek(0)
        return h

    def creation_date(self):
        """ """
        if not self.exif:
            self.exif = self.get_exif()

    def __path_from_date(self, root, name):
        """ Returns the target path that we should write a file to. 
        
            @param  name    The name of the file at the destination. """
        creation_date = self.creation_date()
        return os.path.join(root, 
                creation_date["year"], 
                creation_date["month"], 
                name) 

    def hashes_match(self, path):
        """ Returns `True` if the file at the location matches the file
            represented by this `File` object. Used to ensure that we don't
            unnecessarily copy an identical file. 
            
            @param  path    The path we intend to move this file to. """
        with open(path, "rb") as f:
            m = hashlib.sha256()
            m.update(f.read())
            return self.hash == m.digest()

    def write_check(self, path):
        """ Checks to ensure that the path we are intending to write to is
            empty. If a file exists, checks to see if the hash of that file
            matches the hash of the file represented by this `File` object. 

            @param  path    The target path.

            @returns    Returns an enum value. `UNSAFE` if a file exists at the
                        target path and the hashes do not match. `IDENTICAL` if
                        the files are exact matches, and `SAFE` if no file
                        currently exists at the target location.
               """
        if os.path.exists(path):
            if not self.hashes_match(path):
                return Safety.UNSAFE 
            else:
                return Safety.IDENTICAL
        return Safety.SAFE

    def target_path(self, root):
        """ """
        name, ext = os.path.splitext(os.path.basename(self.path))
        mod = ''
        i = 1
        path = self.__path_from_date(root, f"{name}{mod}{ext}") 
        check = self.write_check(path)

        while check == Safety.UNSAFE:
            mod = '_{i}'
            path = os.path.join(root, f"{name}{mod}{ext}")
            check = self.write_check(path)
            i = i + 1

        if check == Safety.SAFE:
            return path

        return None

    def get_exif(self):
        """ """
        raise NotImplementedError()

    def make_nested_dirs(self, target):
        """ """
        dirs = os.path.dirname(target)

        if not os.path.exists(dirs):
            os.makedirs(dirs)

    def move(self, root):
        """ """
        target = self.target_path(root)

        if target:
            self.make_nested_dirs(target)
            print(f"Moving to {target}")
            shutil.move(self.path, target)

    def copy(self, root):
        """ """
        target = self.target_path(root)

        if target:
            self.make_nested_dirs(target)
            print(f"Copying to {target}")
            shutil.copyfile(self.path, target)
