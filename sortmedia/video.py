import json

from datetime import datetime
from sortmedia.file import File
from subprocess import check_output


class Video(File):
    def creation_date(self):
        """ Returns the creation date based on the file's EXIF data. """
        super().creation_date()

        created_str = self.exif.get('creation_time')

        if not created_str:
            return None

        parsed = datetime.strptime(created_str, "%Y-%m-%dT%H:%M:%S.000000Z")
        return {
            'year': str(parsed.year),
            'month': str(parsed.strftime("%B")),
            'day': str(parsed.day)
        }

    def get_exif(self):
        """ Returns the EXIF data for a photo. Includes support for HEIC file
            format. """
        cmd = ['ffprobe', '-v', 'quiet', self.fp.name, '-print_format', 'json',
               '-show_entries',
               'stream=index,codec_type:stream_tags=creation_time:' +
               'format_tags=creation_time']
        out = check_output(cmd)
        j = json.loads(out)
        streams = j.get("streams", {})

        if len(streams) == 0:
            return None

        return streams[0].get("tags", None)
