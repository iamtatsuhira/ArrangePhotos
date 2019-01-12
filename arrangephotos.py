from PIL import Image
from PIL.ExifTags import TAGS
import os
import sys
import shutil
import glob

ALLAWED_EXTENSIONS = set(['jpg', 'JPG', 'png', 'PNG'])

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
    # 'yyyy:mm:dd hh:mm:ss'というフォーマットなので
    # split(" ")により" "で分割し、最初の要素（日付に関する部分）のみ取得
    date = date_time.split(" ")[0]
    # ディレクトリ作成用にフォーマットを'yyyy:mm:dd'から'yyyy-mm-dd'に変更
    date = "-".join(date.split(":"))
    
    return date

def main():
    filename = sys.argv[1]

    # ファイルが存在し、かつ拡張子が指定のものなら
    if filename and allowed_file(filename):
        # 日付の情報を取得
        date_str = get_date_from_exif(filename)
        
        # 日付のディレクトリがないなら
        if not os.path.isdir(date_str):
            # ディレクトリを作成
            os.mkdir(date_str)
        
        # 移動するファイル群を取得
        # 'hoge.JPG'や'hoge.ARW'、つまり'hoge.*'を取得
        files_to_be_moved = glob.glob(filename.split('.')[0] + ".*")

        # ファイル群を日付の名前がついたディレクトリに移動
        for f in files_to_be_moved:
            shutil.move(f, date_str)
        
if __name__ == "__main__":
    main()
