# pydegadeg
ネガティブ診断君のpythonバージョンです。

pynegadegってつけようとしたけど、ミスってしまった。

***

診断くんにリプライするとその人のネガティブ度を測定して、リプライで返してくれるBot

辞書上にネガティブな単語が多いためネガティブ度が高めに出る。

補正関数をもとは用いていたがバグが出ることがわかったので、今は出てきた値をそのままリプライしている。

***

`python app.py`:起動(ただし`.env`ファイルに以下記述(自分のものに書き換えること))

```
CONSUMER_KEY = "YOUR_CONSUMER_KEY"
CONSUMER_SECRET = "YOUR_CONSUMER_SECRET"
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
ACCESS_TOKEN_SECRET = "YOUR_ACCESS_TOKEN_SECRET"
```

`pip install ???`

はいくつかあります。

***

`test.js`, `calc_test.py`:補正関数の計算テスト用

`sentense.py`:ツイートから余計なものを除く処理のテスト用

`makedict.py`:ポジティブネガティブ単語を辞書化して呼び出すテスト

[辞書は
こちらからダウンロードして使っています：単語感情極性対応表](http://www.lr.pi.titech.ac.jp/~takamura/pndic_ja.html)

`keitaiso.py`:形態素解析モジュールjanomeのテストファイル
