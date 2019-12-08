import os
import sys
import shutil
import piexif
import unittest
import random
import string

from PIL import Image
from unittest.mock import MagicMock

from sortmedia.util import Safety
from sortmedia import util
from sortmedia.photo import Photo
from sortmedia.sort import SortMedia

def randomword(n):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(n))

def faux_exif():
    zeroth_ifd = {
            piexif.ImageIFD.Make: u"Canon",
            piexif.ImageIFD.XResolution: (96, 1),
            piexif.ImageIFD.YResolution: (96, 1),
            piexif.ImageIFD.Software: u"piexif"
    }

    exif_ifd = {
            piexif.ExifIFD.DateTimeOriginal: u"2099:09:29 10:10:10",
            piexif.ExifIFD.LensMake: u"LensMake",
            piexif.ExifIFD.Sharpness: 65535,
            piexif.ExifIFD.LensSpecification: ((1, 1),
                                               (1, 1),
                                               (1, 1),
                                               (1, 1)),
    }

    first_ifd = {
            piexif.ImageIFD.Make: u"Canon",
            piexif.ImageIFD.XResolution: (40, 1),
            piexif.ImageIFD.YResolution: (40, 1),
            piexif.ImageIFD.Software: u"piexif"
    }

    exif_dict = {
            "0th": zeroth_ifd,
            "Exif": exif_ifd,
            "1st": first_ifd,
    }

    return piexif.dump(exif_dict)

def create_file(width, height, color, name='', withExif=True):
    if not name:
        name = randomword(5)

    exif = faux_exif() if withExif else piexif.dump({})

    filename = f'test_files/{name}.jpg'
    img = Image.new('RGB', (width, height), color=color)
    img.save(filename, 'jpeg', exif=exif)
    return filename


class TestFile(unittest.TestCase):
    def setUp(self):
        if not os.path.exists('test_files'):
            os.mkdir('test_files')

    def tearDown(self):
        shutil.rmtree('test_files')

    def test_hashes(self):
        img_a = create_file(50, 50, 'blue')
        img_b = create_file(50, 50, 'blue')
        img_c = create_file(50, 50, 'red')

        photo_a = Photo(img_a, 'image/jpeg')

        self.assertTrue(photo_a.hashes_match(img_b))
        self.assertFalse(photo_a.hashes_match(img_c))

    def test_no_exif(self):
        img = create_file(50, 50, 'green', withExif=False)
        photo = Photo(img, 'image/jpeg')
        target = photo.target_path('foobar')

        basename = os.path.basename(img)
        self.assertTrue(target, f'/foobar/unknown/{basename}')

    def test_path_from_date(self):
        img_a = create_file(50, 50, 'red', name='foobar')
        photo = Photo(img_a, 'image/jpeg')
        target = photo.target_path('foobar')
        self.assertEqual(target, 'foobar/2099/September/29/foobar.jpg')

    def test_ignore_duplicate_at_target(self):
        img_a = create_file(50, 50, 'blue', name='ham')
        photo = Photo(img_a, 'image/jpeg')

        ret = photo.write_check(img_a)
        self.assertEqual(Safety.IDENTICAL, ret)

        target_path = photo.target_path('foobar')
        self.assertEqual(target_path, 'foobar/2099/September/29/ham.jpg')

    def test_no_file_at_target(self):
        img_a = create_file(50, 50, 'blue', name='ham')
        photo = Photo(img_a, 'image/jpeg')

        ret = photo.write_check('foobar/ham.jpg')
        self.assertEqual(Safety.SAFE, ret)

        target_path = photo.target_path('foobar')
        self.assertEqual(target_path, 'foobar/2099/September/29/ham.jpg')

    def test_file_at_target_non_duplicate(self):
        img_a = create_file(50, 50, 'blue', name='ham')

        # Create a non-identical file at the target.
        target_dir = os.path.join('test_files', '2099', 'September', '29')

        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        path = os.path.join(target_dir, os.path.basename(img_a))
        with open(path, "w") as f:
            f.write("Hello world!")

        photo = Photo(img_a, 'image/jpeg')

        ret = photo.write_check(path)
        self.assertEqual(Safety.UNSAFE, ret)

        target_path = photo.target_path('test_files/')
        self.assertTrue(target_path.endswith('_1.jpg'))

    def test_make_nested_dirs(self):
        img_a = create_file(50, 50, 'blue', name='ham')
        photo = Photo(img_a, 'image/jpeg')
        photo.make_nested_dirs('test_files/baz/ham.jpg')
        self.assertTrue(os.path.isdir('test_files/baz'))

    def test_move(self):
        img_a = create_file(50, 50, 'blue', name='ham')
        photo = Photo(img_a, 'image/jpeg')
        photo.move('test_files/move')
        self.assertTrue(os.path.exists('test_files/move/2099/September/' +
                                       '29/ham.jpg'))

    def test_copy(self):
        img_a = create_file(50, 50, 'blue', name='ham')
        photo = Photo(img_a, 'image/jpeg')
        photo.copy('test_files/copy')
        self.assertTrue(os.path.exists('test_files/copy/2099/September/' +
                                       '29/ham.jpg'))


class TestPhoto(unittest.TestCase):
    def test_heic(self):
        photo = Photo('tests/files/lime.heic', 'image/heic')
        target = photo.target_path('foo')
        self.assertEqual(target, 'foo/2017/October/19/lime.heic')


class TestUtil(unittest.TestCase):
    def test_read_mime(self):
        path = 'tests/files/lime.heic'
        mime = util.get_mimetype(path)
        self.assertEqual(mime, 'image/heic')

    def test_mime_video(self):
        self.assertTrue(util.is_video('video/mp4'))
        self.assertFalse(util.is_video('image/jpeg'))

    def test_mime_photo(self):
        self.assertTrue(util.is_photo('image/jpeg'))
        self.assertFalse(util.is_photo('video/mp4'))


class TestSortMedia(unittest.TestCase):
    def setUp(self):
        if not os.path.exists('test_files'):
            os.mkdir('test_files')

    def tearDown(self):
        if os.path.exists('test_files'):
            shutil.rmtree('test_files')

        if os.path.exists('test_move'):
            shutil.rmtree('test_move')

    def test_exclude_dir(self):
        ms = SortMedia(excludes=['foo/bar'])
        self.assertTrue(ms.is_exclude_dir('foo/bar/spam.jpg'))
        self.assertFalse(ms.is_exclude_dir('spam/eggs/blah.jpg'))

    def test_handle_no_process_dirs(self):
        img_a = create_file(50, 50, 'blue', name='spam')
        img_b = create_file(50, 50, 'red', name='eggs')

        ms = SortMedia(noprocess=['test_files'])
        ms.process_files('test_files/', 'test_move/')

        self.assertTrue(os.path.isdir('test_move/test_files'))

    def test_process_files(self):
        img_a = create_file(50, 50, 'blue', name='spam')
        img_b = create_file(50, 50, 'red', name='eggs')
        ms = SortMedia()
        ms.process_files('test_files/', 'test_move/')

        self.assertTrue(os.path.exists('test_move/2099/September/29/spam.jpg'))
        self.assertTrue(os.path.exists('test_move/2099/September/29/eggs.jpg'))

    def test_symlink(self):
        pass


if __name__ == "__main__":
    unittest.main()
