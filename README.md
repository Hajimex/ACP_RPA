# 背景
できるだけ人力作業を省くため、ルーティーンになっている作業は、言語解析やクラウドなどの技術を用いて自動化していく

# 各モジュール使い方
## ロジデータアップ前データ修正
### 
テスト購入行削除、ゆうパックかゆうパケット自動判別、住所エラーは下記の見方を参照

### コマンド
1. JapanOrderSystemCSVからダウンロードされたデータをdataフォルダ以下に一旦格納
2. 下記のコマンドを打つ
```
python bin/logicsv.py --file "ファイル名.csv"
```
（サンプル）
```
python bin/logicsv.py --file "order.csv"
```
3. output.sjis.csvというファイルが完成品です

### 見方
1. BG列を見てFALSEなら、都道府県列を直す。
2. BM列を見て0なら、市区町村レベルと町域レベルを直す。
3. それを元のCSVに貼る。
4. 元のCSVでテスト行を削除する。

![画像](https://raw.githubusercontent.com/Hajimex/acp_RPA/master/src/Screen_Shot_2019-06-08_at_0_55_04.png?token=AAKXSPIL4J7FZ6MK6D2GTQK5APC2E "画像")

=======
＊個人情報はダミーを利用しています
