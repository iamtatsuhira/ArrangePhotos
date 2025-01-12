from PIL import Image
from PIL.ExifTags import TAGS
import os
import sys
import shutil
import glob
import datetime

PIC_ALLAWED_EXTENSIONS = set(['jpg', 'JPG', 'png', 'PNG'])
MOV_ALLAWED_EXTENSIONS = set(['arw', 'ARW', 'MP4', 'mp4', 'MTS', 'mts', 'THM', 'thm', 'DNG', 'dng', 'mov', 'MOV'])
# GRIIIx の DNG が PIL による Exifよみこみに対応していないっぽいから、とりあえず MOV チームにいれて処理

def allowed_pic(filename):
    # eg. filaneme = hoge.txt
    # eg. '.' in filename -> True
    # eg. filaneme.rsplit('.', 1) -> ['hoge', 'txt']
    return '.' in filename and filename.rsplit('.', 1)[1] in PIC_ALLAWED_EXTENSIONS

def allowed_mov(filename):
    # eg. filaneme = hoge.txt
    # eg. '.' in filename -> True
    # eg. filaneme.rsplit('.', 1) -> ['hoge', 'txt']
    return '.' in filename and filename.rsplit('.', 1)[1] in MOV_ALLAWED_EXTENSIONS


def get_date_from_exif(file):
    im = Image.open(file)
    exif = im._getexif()

    exif_table = {}
    for tag_id, value in exif.items():
        tag = TAGS.get(tag_id, tag_id)
        exif_table[tag] = value
    
    date_time = exif_table.get("DateTimeOriginal")
    # 'yyyy:mm:dd hh:mm:ss'というフォーマットなので
    # split(" ")により" "で分割し、最初の要素（日付に関する部分）のみ取得
    date = date_time.split(" ")[0]
    # ディレクトリ作成用にフォーマットを'yyyy:mm:dd'から'yyyy-mm-dd'に変更
    date = "-".join(date.split(":"))
    
    return date

def get_date_from_mtime(file):
    timestamp = os.path.getmtime(file)
    dt = datetime.datetime.fromtimestamp(timestamp)
    date = dt.strftime('%Y-%m-%d')

    return date

def main():
    filename = sys.argv[1]

    # 画像だったら
    if allowed_pic(filename):
        # 日付の情報を取得
        date_str = get_date_from_exif(filename)
    # 動画だったら
    elif allowed_mov(filename):
        date_str = get_date_from_mtime(filename)

    else:
        print (f"{filename} は画像でも動画でもない。")
        sys.exit()

    # 日付のディレクトリがないなら
    if not os.path.isdir(date_str):
        # ディレクトリを作成
        os.mkdir(date_str)

    if os.path.isfile(filename):
        shutil.move(filename, date_str)
        print (f"{filename} was transferred to {date_str}/")

if __name__ == "__main__":
    main()
