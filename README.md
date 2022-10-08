# arrangephotos.pyとは
`hoge.JPG`みたいな`jpg`ファイルと、`hoge.*`みたいな拡張子以外は同じ名前のファイルを、`hoge.JPG`のExifから得られる日付の情報をもとに作成されたディレクトリに移動させるコード。

# 使い方
## python仮想環境の構築、必要なライブラリのインストール
Macの`Homebrew`で入れた`python3`を使用し、そしてシェルは`fish`である場合。

```sh
$ python3 -m venv myenv
# activate
$ source ./myenv/bin/activate.fish
$ pip install -r requirements.txt
```

## コードの使い方

```sh
$ python arrangephotos.py hoge.JPG
```

これでexif情報を元に`2019-01-13`みたいなディレクトリに`hoge.*`が移動される。

## ディレクトリ内の全てのファイルに対して適用する
`fish`の場合
```sh
$ for i in (ls):
    python arrangephotos.py $i
end
```

