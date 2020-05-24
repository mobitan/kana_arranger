from collections import Counter
from . import evaluator

class Keyboard():
    """
    キーボードを表すクラス
    """
    def __init__(self, name, keytop, hand, finger, row, column, arpcol):
        """
        # レイアウト名（Heatmapのレイアウト名に合わせる）
        'QWERTY',
        # 文字
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
        """
        self.name = name
        self.keytop = keytop
        self.tx_han = str.maketrans(keytop, hand)
        self.tx_fin = str.maketrans(keytop, finger)
        self.tx_row = str.maketrans(keytop, row)
        self.tx_col = str.maketrans(keytop, column)
        self.arpcol = arpcol

    def evaluate(self, corpus, method):
        print("Evaluating {} for {} on {}".format(method.__class__.__name__, corpus.__class__.__name__, self.name))
        r = evaluator.Evaluation(corpus, method, self)
        for word, n in corpus.freq.items():
            key = method.apply(word)
            han = key.translate(self.tx_han)
            fin = key.translate(self.tx_fin)
            row = key.translate(self.tx_row)
            col = key.translate(self.tx_col)
#             print("{:>10} {} {} {} {} {} {}".format(n, word, key, han, fin, row, col))
            for i in range(len(key)):
                if key[i] not in self.keytop:
                    r.ignored.add(key[i])
                    continue
                r.c_key[key[i]] += n
                r.c_han[han[i]] += n
                r.c_fin[fin[i]] += n
                r.c_row[row[i]] += n
                r.c_col[col[i]] += n
                r.total += n
                if i == 0:
                    continue
                if key[i-1] not in self.keytop:
                    continue
                if han[i-1] != han[i]:
#                     print('           交互')
                    r.alt += n
                elif fin[i-1] == fin[i]:
                    z = abs(int(row[i-1]) - int(row[i]))
#                     print('           同指{}段違い'.format(z))
                    r.sf[z] += n
                elif row[i-1] == row[i] and col[i-1] in self.arpcol and col[i] in self.arpcol:
#                     print("           アルペジオ")
                    r.arp += n
        if r.ignored:
            print("  Did not count: {}".format(''.join(r.ignored)))
        return r

class JisKeyboard(Keyboard):
    """
    JISキーボード
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃1 │2 │3 │4 │5 ┃6 │7 │8 │9 │0 │- │^ │| │┃
    ┃│q │w │e │r │t ┃y │u │i │o │p │@ │[ │  ┃
    ┃ │a │s │d │f │g ┃h │j │k │l │; │: │] │ ┃
    ┃S  │z │x │c │v │b ┃n │m │, │. │/ │_ │S  ┃
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    """
    def __init__(self):
        super().__init__(
            'QWERTY',
            '1234567890-^|qwertyuiop@[asdfghjkl;:]zxcvbnm,./_',
            '<<<<<>>>>>>>><<<<<>>>>>>><<<<<>>>>>>><<<<<>>>>>>',
            'abcddgghijjjjabcddgghijjjabcddgghijjjabcddgghijj',
            '444444444444433333333333322222222222211111111111',
            'MNOPQRSTUVWXYMNOPQRSTUVWXMNOPQRSTUVWXMNOPQRSTUVW',
            'MNOPSTUV'
        )

class MicrotronKeyboard(Keyboard):
    """
    μTRONキーボード
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃   │1 │2 │3 │4 │5 │6    ┃   7 │8 │9 │0 │- │^ │|  ┃
    ┃  │  │q │w │e │r │t │  ┃  │y │u │i │o │p │@ │[ ┃
    ┃ │  │a │s │d │f │g │   ┃   │h │j │k │l │; │: │]┃
    ┃   │ z │x │c │v │b │    ┃    │n │m │, │. │/  │_  ┃
    ┃          │     │S │       ┃       │S │     │          ┃
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    """
    def __init__(self):
        super().__init__(
            'MicroTRON_QWERTY',
            '1234567890-^|qwertyuiop@[asdfghjkl;:]zxcvbnm,./_',
            '<<<<<>>>>>>>><<<<<>>>>>>><<<<<>>>>>>><<<<<>>>>>>',
            'aabcddgghijjjabcddgghijjjabcddgghijjjabcddgghijj',
            '444444444444433333333333322222222222211111111111',
            'LMNOPQRSTUVWXMNOPQRSTUVWXMNOPQRSTUVWXMNOPQRSTUVW',
            'MNOPSTUV'
        )