from PIL import Image
from PIL.ExifTags import TAGS
import os
import sys

ALLAWED_EXTENSIONS = set(['jpg', 'JPG', 'png', 'PNG'])

filename = sys.argv[1]

def allowed_file(filename):
    # eg. filaneme = hoge.txt
    # eg. '.' in filename -> True
    # eg. filaneme.rsplit('.', 1) -> ['hoge', 'txt']
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLAWED_EXTENSIONS

def get_date_from_exif(file):
    im = Image.open(file)
    exif = im._getexif()

    exif_table = {}
    for tag_id, value in exif.items():
        tag = TAGS.get(tag_id, tag_id)
        exif_table[tag] = value
    
    date_time = exif_table.get("DateTimeOriginal")
    date = date_time.split(" ")[0]
    date = "-".join(date.split(":"))
    
    return date

def main():
    filename = sys.argv[1]
    if filename and allowed_file(filename):
        date_str = get_date_from_exif(filename)
        print(date_str)


if __name__ == "__main__":
    main()