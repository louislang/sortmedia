import os
import shutil
import piexif
import unittest
import random, string

from PIL import Image
from mediasort.util import Safety
from mediasort import util
from mediasort.photo import Photo

class TestFile(unittest.TestCase):
    def randomword(self, n):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(n))

    def __faux_exif(self):
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
                piexif.ExifIFD.LensSpecification: ((1, 1), (1, 1), (1, 1), (1, 1)),
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

    def __create_file(self, width, height, color, name='', withExif=True):
        if not name:
            name = self.randomword(5)

        exif = self.__faux_exif() if withExif else piexif.dump({})

        filename = f'test_files/{name}.jpg' 
        img = Image.new('RGB', (width, height), color=color)
        img.save(filename, 'jpeg', exif=exif)
        return filename

    def setUp(self):
        if not os.path.exists('test_files'):
            os.mkdir('test_files')

    def tearDown(self):
        shutil.rmtree('test_files')

    def test_hashes(self):
        img_a = self.__create_file(50, 50, 'blue')
        img_b = self.__create_file(50, 50, 'blue')
        img_c = self.__create_file(50, 50, 'red')

        fp_a = open(img_a, 'rb')
        fp_c = open(img_c, 'rb')

        photo_a = Photo(fp_a, 'image/jpeg')
        photo_c = Photo(fp_c, 'image/jpeg')

        self.assertTrue(photo_a.hashes_match(img_b))
        self.assertFalse(photo_a.hashes_match(img_c))

    def test_no_exif(self):
        img = self.__create_file(50, 50, 'green', withExif=False)
        fp = open(img, 'rb')
        photo = Photo(fp, 'image/jpeg')
        target = photo.target_path('foobar')

        basename = os.path.basename(img)
        self.assertTrue(target, f'/foobar/unknown/{basename}')

    def test_path_from_date(self):
        img_a = self.__create_file(50, 50, 'red', name='foobar')
        fp = open(img_a, 'rb')
        photo = Photo(fp, 'image/jpeg')
        target = photo.target_path('foobar')
        self.assertEqual(target, 'foobar/2099/September/foobar.jpg')

    def test_ignore_duplicate_at_target(self):
        img_a = self.__create_file(50, 50, 'blue', name='ham')
        fp = open(img_a, 'rb')
        photo = Photo(fp, 'image/jpeg')

        ret = photo.write_check(img_a)
        self.assertEqual(Safety.IDENTICAL, ret)

        target_path = photo.target_path('foobar')
        self.assertEqual(target_path, 'foobar/2099/September/ham.jpg')

    def test_no_file_at_target(self):
        img_a = self.__create_file(50, 50, 'blue', name='ham')
        fp = open(img_a, 'rb')
        photo = Photo(fp, 'image/jpeg')

        ret = photo.write_check('foobar/ham.jpg')
        self.assertEqual(Safety.SAFE, ret)

        target_path = photo.target_path('foobar')
        self.assertEqual(target_path, 'foobar/2099/September/ham.jpg')

    def test_file_at_target_non_duplicate(self):
        img_a = self.__create_file(50, 50, 'blue', name='ham')

        # Create a non-identical file at the target.
        target_dir = os.path.join('test_files', '2099', 'September')

        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        path = os.path.join(target_dir, os.path.basename(img_a))
        with open(path, "w") as f:
            f.write("Hello world!")

        fp = open(img_a, 'rb')
        photo = Photo(fp, 'image/jpeg')

        ret = photo.write_check(path)
        self.assertEqual(Safety.UNSAFE, ret)

        target_path = photo.target_path('test_files/')
        self.assertTrue(target_path.endswith('_1.jpg'))

    def test_make_nested_dirs(self):
        img_a = self.__create_file(50, 50, 'blue', name='ham')
        fp = open(img_a, 'rb')
        photo = Photo(fp, 'image/jpeg')
        photo.make_nested_dirs('test_files/baz/ham.jpg')
        self.assertTrue(os.path.isdir('test_files/baz'))

    def test_move(self):
        img_a = self.__create_file(50, 50, 'blue', name='ham')
        fp = open(img_a, 'rb')
        photo = Photo(fp, 'image/jpeg')
        photo.move('test_files/move')
        self.assertTrue(os.path.exists('test_files/move/2099/September/ham.jpg'))

    def test_copy(self):
        img_a = self.__create_file(50, 50, 'blue', name='ham')
        fp = open(img_a, 'rb')
        photo = Photo(fp, 'image/jpeg')
        photo.copy('test_files/copy')
        self.assertTrue(os.path.exists('test_files/copy/2099/September/ham.jpg'))

class TestPhoto(unittest.TestCase):
    def test_heic(self):
        fp = open('tests/files/lime.heic', 'rb')
        photo = Photo(fp, 'image/heic')
        target = photo.target_path('foo')
        self.assertEqual(target, 'foo/2017/October/lime.heic')

class TestUtil(unittest.TestCase):
    def test_read_mime(self):
        with open('tests/files/lime.heic', 'rb') as f:
            mime = util.get_mimetype(f)
            self.assertEqual(mime, 'image/heic')

    def test_mime_video(self):
        self.assertTrue(util.is_video('video/mp4'))
        self.assertFalse(util.is_video('image/jpeg'))

    def test_mime_photo(self):
        self.assertTrue(util.is_photo('image/jpeg'))
        self.assertFalse(util.is_photo('video/mp4'))

if __name__ == "__main__":
    unittest.main()
