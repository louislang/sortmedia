import os 
import shutil
import hashlib
import logging

from util import Safety
from abc import ABC, abstractmethod

logger = logging.getLogger('file')
logging.basicConfig(level=logging.INFO)

class File(ABC):
    """ """

    def __init__(self, fp, path, mime, exif=None):
        """ Create a new `File` object for the file data located at `path` and
            which is represented by the open file pointer `fp`.
            
            @param  fp      An open file pointer to the path.
            @param  path    The path to the file.
            @param  mime    The string MIME type of the file.
            @param  exif    A dictionary of EXIF value. """
        if not path or not isinstance(path, str):
            raise ValueError(f"Path must be a non-empty string. Got `{path}`.")

        if not os.path.isfile(path):
            raise RuntimeError(f"{path} does not exist or is not a file.")

        self.fp = fp 
        self.path = path
        self.hash = self.get_hash()
        self.exif = None 
        self.mime = mime 

        super().__init__()

    def __del__(self):
        """ Closes the open file pointer on object destruct. """
        self.fp.close()

    def get_hash(self):
        """ Returns the hash of the file pointer. """
        m = hashlib.sha256()
        m.update(self.fp.read())
        h = m.digest()
        self.fp.seek(0)
        return h

    def creation_date(self):
        """ This method should be implemented by the inheriting class. The
            child class should call this function to ensure that the EXIF data
            is populated. """
        if not self.exif:
            self.exif = self.get_exif()

    def __path_from_date(self, root, name):
        """ Returns a path based on the given creation date, in the format of:
            `<root>/<year>/<month>/<name>`.
            
            @param  root    The root of our absolute path.
            @param  name    The filename of our path. 
            
            @returns    An absolute path. """
        creation_date = self.creation_date()
        return os.path.join(root, 
                creation_date["year"], 
                creation_date["month"], 
                name) 

    def hashes_match(self, path):
        """ Returns a boolean indicating if the hash of `path` matches the
            object hash.
            
            @param  path    The path to compare hashes with.
            
            @returns    `True` if the path's hash matches the objects hash,
                        `False` otherwise. """
        with open(path, "rb") as f:
            m = hashlib.sha256()
            m.update(f.read())
            return self.hash == m.digest()

    def write_check(self, path):
        """ Runs some preliminary checks to ensure that we do not accidentally
            overwrite an existing file. If a file exists at `path` we check
            its hash. If the hashes match, we return `IDENTICAL`. If they do
            not match, we return `UNSAFE` - we do not want to write the file
            to this path. If no file exists at `path` we return `SAFE`.
            
            @param  path    The path to check. 
            
            @returns    `Safety` """
        if os.path.exists(path):
            if not self.hashes_match(path):
                return Safety.UNSAFE 
            else:
                return Safety.IDENTICAL
        return Safety.SAFE

    def target_path(self, root):
        """ Creates a "safe" target path by performing some basic checks. If
            a file exists at the target path with a non-identical hash we
            create a new file with a `_N` prefix (where `N` is an integer
            value). 
            
            @param  root    The root path to set the target path in. 
            
            @returns    An absolute path to write a file to. """
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
        """ Returns the EXIF data for the file. This should be implemented
            in the inheriting class. """
        raise NotImplementedError()

    def make_nested_dirs(self, target):
        """ Create nested directories if they do not exist. """
        dirs = os.path.dirname(target)

        if not os.path.exists(dirs):
            os.makedirs(dirs)

    def move(self, root):
        """ Safely move this file to the target path. """
        target = self.target_path(root)

        if target:
            self.make_nested_dirs(target)
            print(f"Moving to {target}")
            shutil.move(self.path, target)

    def copy(self, root):
        """ Safely copy this file to the target path. """
        target = self.target_path(root)

        if target:
            self.make_nested_dirs(target)
            print(f"Copying to {target}")
            shutil.copyfile(self.path, target)
