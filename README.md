# REDEME of HEVENTARS

## 名称と概要
### 名称
本ソフトウェアの名称は"HEVENTARS"（ヘーヴェンタース）です。<br>

### 概要
本ソフトウェアは月の標高データを使用して、探査機目線で月地形の陰影付きシミュレーションを行います。<br>
[小型月着陸実証機SLIM](https://www.isas.jaxa.jp/home/slim/SLIM/index.html)の着陸地点同定での初使用を想定して開発され、実際に使用されました。<br>
今後実施される月探査にも役立てることを目指しています。<br>

### 由来
SLIMが着陸地点とする月にある**神酒の海**（みきのうみ、ラテン語: Mare Nectaris）は、ギリシャ神話における神々の飲み物ネクタール（生命の酒）に由来します。<br>
ネクタールをもたらす女神ヘーベー（ギリシャ神話）・ユウェンタース（ローマ神話）の二柱の名前の借り、組み合わせることで本ソフトウェアの名称としています。<br>
月探査におけるネクタールのような存在になることを期待しています。<br>

## 導入方法
Python環境を構築した上でクローン又はzipダウンロードしてください。<br>
使用するライブラリは以下を参照してください。<br>

- Python 標準ライブラリ
  - os
  - re
  - sys
- サードパーティライブラリ
  - numpy
  - requests
  - matplotlib
  - scipy
  - plotly
  - webbrowser
  - tifffile

実行環境に足りないライブラリは適宜追加してください。<br>

## ファイル構造
ファイルの展開後、以下のディレクトリとファイルが存在することを確認してください。<br>

```
HEVENTARS
│
├ README.md .. このファイル
│
├ data .. 標高データとそのラベルを格納するディレクトリ
│  └ data.txt
│
├ logo .. ロゴマークを格納するディレクトリ
│  ├ logo.txt
│  └ logo.png
│
├ result .. シミュレーション結果を格納するディレクトリ
│  └ sample.txt
│
└ src .. ソースコードを格納するディレクトリ
   ├ Apollo17.py
   ├ Area.py
   ├ Download.py
   ├ Effect.py
   ├ Input.py
   ├ main.py
   ├ Ortho.py
   ├ Plot.py
   ├ Read_lbl.py
   ├ Save.py
   ├ SLIM.py
   └ Tile.py
```

## 使用方法
ファイルの展開後、"src" ディレクトリに移動してください。<br>
その後、用途に応じて以下のファイルを実行してください。

- 通常のシュミレーションの場合
```
python main.py
```
KAGUYA Data Archive の [TC データ](https://data.darts.isas.jaxa.jp/pub/pds3/sln-l-tc-5-dtm-map-seamless-v2.0/)を使用してシミュレーションを行います。<br>
全球に対応しているので、画面の指示に従って実行してください。<br>

- SLIM 専用のシュミレーションの場合
```
python SLIM.py
```
Lunar Reconnaissance Orbiter(LRO)の [NAC データ](https://pds.lroc.asu.edu/data/LRO-L-LROC-5-RDR-V1.0/LROLRC_2001/DATA/SDP/NAC_DTM/THEOPHILUS3/)を使用してシミュレーションを行います。<br>
事前に上記URLにアクセスして、NAC_DTM_THEOPHILUS3.LBL と NAC_DTM_THEOPHILUS3.TIF を"data"ディレクトリに格納してください。<br>
特定範囲のみの対応であり、各種パラメータの変更は SLIM.py を確認してください。<br>

- Apollo 17 専用のシュミレーションの場合
```
python Apollo17.py
```
Lunar Reconnaissance Orbiter(LRO)の [NAC データ](https://pds.lroc.asu.edu/data/LRO-L-LROC-5-RDR-V1.0/LROLRC_2001/DATA/SDP/NAC_DTM/APOLLO17/)を使用してシミュレーションを行います。<br>
事前に上記URLにアクセスして、NAC_DTM_APOLLO17.LBL と NAC_DTM_APOLLO17.TIF を"data"ディレクトリに格納してください。<br>
特定範囲のみの対応であり、各種パラメータの変更は Apollo17.py を確認してください。<br>

※ "src" ディレクトリではなく、"HEVENTARS" ディレクトリからの実行も可能です。その際は実行コマンドを適切に変更してください。<br>
※ 各種コードエディタでの実行は、コードエディタのマニュアルを参照してください。<br>

## 操作方法
1. 実行後、ブラウザが自動で立ち上がります。
2. 初期視点はターゲット地点を真上から見下ろす状態でスタートします。（データによってはわずかにズレる可能性もあります。）
3. マウスの左ボタンを押したままの状態で、マウスを上下左右に移動することで視点を変更できます。
4. マウスの中央ホイールを回転させることでシミュレーションの拡大縮小が可能です。
5. 特定の視点での画像を保存したい場合は、画面右上に表示されるカメラマークを押してください。画像がダウンロードされます。

※ ターゲット地点には、ピンクのマーカーが設置されています。
※ シミュレーションにマウスを置くことで、その地点の緯度経度と標高が表示されます。<br>
※ 東西南北にマーカーが設置されています。配色は以下の通りです。

| マーカー名 | カラーコード | カラー名 |
| ---- | ---- | ---- |
| East（東） | #0000FF | Blue |
| West（西） | #DAA520 | Goldenrod |
| South（南）| #FF0000 | Red |
| North（北）| #8A2BE2 | BlueViolet |

## 製作
会津大学　28期生　s1280106<br>
Superviser: [Prof. Makiko Ohtake](https://u-aizu.ac.jp/research/faculty/detail?cd=90131)<br>

## 利用・改良について
ご自由に利用・改良いただいて構いませんが、完全な自作発言は容認いたしません。<br>
何らかの形で本ページをご紹介いただきますようお願い申し上げます。<br>
また、その際ご一報のほどよろしくお願いします。<br>

## 注意事項
- 本ソフトウェアは、開発中です。
- 予期せぬエラーが発生する可能性がありますので、ご了承ください。
