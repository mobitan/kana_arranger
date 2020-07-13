# かな入力方式の開発を支援する kana_arranger

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/mobitan/kana_arranger/master)

kana_arranger は、独自の日本語入力方式（かな入力やローマ字入力など）を開発する人のための Python ライブラリです。
kana_arranger を使うと、次のことを行うプログラムを簡単に書くことができます。

- 日本語コーパスのダウンロードと解析
- かな列から打鍵列への変換（「はんにんやんけ」→ "hannninnyanke"）
- キーボードによって異なる運指の定義
- 以上の組合せに基づくタイピングの定量的な評価（各段各列の負担率や交互打鍵率など）
- 各指負担率のヒートマップによる可視化

サンプルとして、次のプログラムが付属します。

- eval.ipynb: ローマ字入力方式を QWERTY キーボードで評価・可視化する Jupyter Notebook
- ~~2gram.ipynb: コーパスの 2-gram 出現頻度表を表示する Jupyter Notebook~~ 未実装

次のコーパスが利用できるようになっています。

- [国立国語研究所 現代日本語書き言葉コーパス](https://pj.ninjal.ac.jp/corpus_center/bccwj/)のうち、人手によるアノテーションが行われたコアデータ（874万字）
    - を元に作られた、京都大学 学術情報メディアセンター 大規模テキストアーカイブ研究分野のサイトで配布されている[仮名漢字変換用 N-gram](http://www.ar.media.kyoto-u.ac.jp/member/gologo/lm.html#kkc) (kkc-BCCWJCore.tar) に含まれる 3-gram 頻度データ

## クラウドで試してみる

1. [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/mobitan/kana_arranger/master) ←この [launch binder] ボタンを押します。しばらく待つと mybinder.org のサーバー上で Jupyter が起動します。
1. eval.ipynb を開きます。
1. Ctrl+Enter か Shift+Enter を押して、セルを上から順に実行します。

mybinder.org は無料で使えますが、ブラウザを閉じて10分経過するとセッションがタイムアウトし、12時間経過するとインスタンスが消えます。
編集したファイルを残しておきたい場合は、タイムアウトする前にダウンロードするか、ローカルにインストールした Jupyter を使いましょう。

## ローカルで試してみる

1. [Jupyter をインストールする](https://jupyter.org/install)
1. `$ git clone https://github.com/mobitan/kana_arranger.git`
1. `$ cd kana_arranger`
1. `$ jupyter notebook eval.ipynb`

## かな入力方式を定義する

かな入力方式は Transliterator クラスのインスタンスとして定義され、apply メソッドによって かな列を打鍵列に変換します。

単純な入力方式は Transliterator クラスのコンストラクタに名前と変換テーブルを与えるだけで定義できます。
次の例は、[ブリ中トロ配列](https://mobitan.hateblo.jp/entry/2020/04/30/233245)の一部を抜き出した入力方式です。

    table = {
        'う':'l', 'り':'kj', 'りょ':'mz', 'りょう':'mda', 'ょ':'z'
    }
    buriburi = ka.Transliterator('buriburi', table)
    buriburi.apply('りょうり')
    #=> 'mdakj'

このように、Transliterator クラスの apply メソッドは、かな列を最長一致で区切って打鍵列に変換します。
上の例では、かな列「りょうり」を、「り/ょ/う/り」でも「りょ/う/り」でもなく「りょう/り」と区切って、打鍵列 "mdakj" に変換しています。

打鍵列は、次のルールに従う文字列です。

- 1打鍵を1文字で表す
- シフトキーは英大文字（'L', 'R', 'X' など）
- 文字キーは英小文字、数字、または記号（'a', '1', '!' など）
- シフトキーと文字キーがキーボードのキー（後述）に含まれていること

ローマ字入力は「ん」「っ」の特殊処理が必要となるため最長一致では正しく変換できません。
こうような複雑な入力方式を定義するときは、Transliterator クラスを継承したサブクラスを作り、apply メソッドを適切に実装する必要があります。
kana_arranger/transliterator.py を参考に実装してください。

## キーボードを定義する

キーボードは Keyboard クラスのインスタンスまたはサブクラスとして定義され、evaluate メソッドによって評価値を計算します。

次の例は、JIS キーボードの定義です。

    jisx6002 = ka.Keyboard(
        # レイアウト名（Heatmapのレイアウト名に合わせる）
        'QWERTY',
        # キー
        '1234567890-^|qwertyuiop@[asdfghjkl;:]zxcvbnm,./_',
        # 担当手（<=左手, >=右手）
        '<<<<<>>>>>>>><<<<<>>>>>>><<<<<>>>>>>><<<<<>>>>>>',
        # 担当指（a=左小指, ..., d=左人差指, e=左親指, f=右親指, g=右人差指, ..., j=右小指）
        'abcddgghijjjjabcddgghijjjabcddgghijjjabcddgghijj',
        # 段（0=親指, 1=下段, 2=中段, 3=上段, 4=最上段）
        '444444444444433333333333322222222222211111111111',
        # 列（..., Q=左手最右列, R=右手最左列, ...）
        'MNOPQRSTUVWXYMNOPQRSTUVWXMNOPQRSTUVWXMNOPQRSTUVW',
        # アルペジオに含める列
        'MNOPSTUV'
    )

コンストラクタの第2引数にキーを任意の順序で羅列します。この順序に合わせて、第3引数に各キーを打つ手、第4引数に各キーを打つ指、第5引数に各キーの置かれる段、第6引数に各キーの置かれる列をそれぞれ羅列します。手・指・段・列を表す文字は、互いに異なっていれば何でも構いません。

キーボードのヒートマップを正しく描画するには、次の作業を別途行う必要があります。

- kana_arranger/img/<レイアウト名>.png に800×373ピクセルの画像を作る
- kana_arranger/lib/keyboard-layouts.js に画像上の各キーの中心座標を書く


## 評価値の計算を拡張する

kana_arranger/keyboard.py と kana_arranger/evaluator.py を参考に実装してください。

## 別のコーパスを利用する

kana_arranger/corpus.py を参考に実装してください。

## TODO

以下の機能が未実装です。プルリク歓迎！

- シフトキーの評価（シフトキーを押しながら文字キーを押す。これを1打鍵・1シフトと数える？　それとも2打鍵・1シフトと数える？）
- 同時打鍵の評価（文字キーを押しながら文字キーを押す。これを2打鍵・1動作と数える。打鍵と動作を区別するため、打鍵列に何らかの文法を導入する必要がある）

## Acknowledgement

kana_arranger は、以下のオープンソースソフトウェアを一部改変して利用しています。

- [heatmap.js](https://www.patrick-wied.at/static/heatmapjs/)

