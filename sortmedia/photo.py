import PIL
import piexif
import pyheif
import PIL.Image
import PIL.ExifTags

from sortmedia.file import File
from datetime import datetime


class Photo(File):
    def creation_date(self):
        """ Returns the creation date based on the file's EXIF data. """
        super().creation_date()

        # If we do not have exif data, return `None`.
        if not self.exif:
            return None

        keys = ["DateCreated",
                "DateTimeCreated",
                "DateTimeOriginal",
                "DateTime",
                "DateTimeDigitized",
                "DigitalCreationDateTime"]

        created_str = None

        for k in keys:
            if k in self.exif:
                created_str = self.exif[k]
                break

        if isinstance(created_str, bytes):
            created_str = created_str.decode('utf-8')

        parsed = datetime.strptime(created_str, "%Y:%m:%d %H:%M:%S")

        return {
            'year': str(parsed.year),
            'month': str(parsed.strftime("%B")),
            'day': str(parsed.day)
        }

    def get_exif(self):
        """ Returns the EXIF data for a photo. Includes support for HEIC file
            format. """
        exif = {}

        # iOS now stores images in `heic`. PIL doesn't support this format.
        # This allows us to use the bindings to libheif to grab the EXIF data.
        if self.mime == "image/heic":
            heif = pyheif.read_heif(self.fp)
            for metadata in heif.metadata or []:
                if metadata['type'] == 'Exif':
                    data = metadata.get('data', {})
                    exif = piexif.load(data).get('Exif').items()

        # Otherwise, use PIL to process the image.
        else:
            img = PIL.Image.open(self.fp)
            exif = img._getexif().items()

        self.fp.seek(0)
        return {PIL.ExifTags.TAGS[k]: v for k, v in exif if k in
                PIL.ExifTags.TAGS}
