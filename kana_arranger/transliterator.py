import re

class Transliterator:
    """
    入力方式を表すクラス
    """
    
    def __init__(self, name, table):
        """
        tableの定義
        - 1打鍵を1文字で表す
        - 文字キーは英小文字、数字、記号
        - シフトキーは英大文字
        """
        self.name = name
        self.table = table
        # [TODO] 同時打鍵の表現方法を考える

    def lookup(self, text):
        """
        最長一致を返す
        """
        for i in range(len(text), 0, -1):
            if text[:i] in self.table:
                return self.table[text[:i]] + self.lookup(text[i:])
        if len(text) > 1:
            return text[:1] + self.lookup(text[1:])
        return text
    
    def apply(self, text):
        """
        文字列を打鍵列に変換する
        """
        return self.lookup(text)

class Romaji(Transliterator):
    """
    ローマ字配列
    """
    def __init__(self):
        table = {
            'きゃ':'kya',  'きぃ':'kyi',  'きゅ':'kyu',  'きぇ':'kye',  'きょ':'kyo',
            'ぎゃ':'gya',  'ぎぃ':'gyi',  'ぎゅ':'gyu',  'ぎぇ':'gye',  'ぎょ':'gyo',
            'くぁ':'qa',   'くぃ':'qi',   'くぅ':'qwu',  'くぇ':'qe',   'くぉ':'qo',
            'ぐぁ':'gwa',  'ぐぃ':'gwi',  'ぐぅ':'gwu',  'ぐぇ':'gwe',  'ぐぉ':'qwo',
            'しゃ':'sya',  'しぃ':'syi',  'しゅ':'syu',  'しぇ':'sye',  'しょ':'syo',
            'じゃ':'ja',   'じぃ':'jyi',  'じゅ':'ju',   'じぇ':'je',   'じょ':'jo',
            'すぁ':'swa',  'すぃ':'swi',  'すぅ':'swu',  'すぇ':'swe',  'すぉ':'swo',
            'ちゃ':'tya',  'ちぃ':'tyi',  'ちゅ':'tyu',  'ちぇ':'tye',  'ちょ':'tyo',
            'ぢゃ':'dya',  'ぢぃ':'dyi',  'ぢゅ':'dyu',  'ぢぇ':'dye',  'ぢょ':'dyo',
            'つぁ':'tsa',  'つぃ':'tsi',                 'つぇ':'tse',  'つぉ':'tso',
            'てゃ':'tha',  'てぃ':'thi',  'てゅ':'thu',  'てぇ':'the',  'てょ':'tho',
            'でゃ':'dha',  'でぃ':'dhi',  'でゅ':'dhu',  'でぇ':'dhe',  'でょ':'dho',
            'とぁ':'twa',  'とぃ':'twi',  'とぅ':'twu',  'とぇ':'twe',  'とぉ':'two',
            'どぁ':'dwa',  'どぃ':'dwi',  'どぅ':'dwu',  'どぇ':'dwe',  'どぉ':'dwo',
            'にゃ':'nya',  'にぃ':'nyi',  'にゅ':'nyu',  'にぇ':'nye',  'にょ':'nyo',
            'ひゃ':'hya',  'ひぃ':'hyi',  'ひゅ':'hyu',  'ひぇ':'hye',  'ひょ':'hyo',
            'びゃ':'bya',  'びぃ':'byi',  'びゅ':'byu',  'びぇ':'bye',  'びょ':'byo',
            'ぴゃ':'pya',  'ぴぃ':'pyi',  'ぴゅ':'pyu',  'ぴぇ':'pye',  'ぴょ':'pyo',
            'ふぁ':'fa',   'ふぃ':'fi',   'ふぅ':'fwu',  'ふぇ':'fe',   'ふぉ':'fo',
            'ふゃ':'fya',                 'ふゅ':'fyu',                 'ふょ':'fyo',
            'みゃ':'mya',  'みぃ':'myi',  'みゅ':'myu',  'みぇ':'mye',  'みょ':'myo',
            'りゃ':'rya',  'りぃ':'ryi',  'りゅ':'ryu',  'りぇ':'rye',  'りょ':'ryo',
            'うぁ':'wha',  'うぃ':'wi',                  'うぇ':'we',   'うぉ':'who',
            'ゔぁ':'va',   'ゔぃ':'vi',   'ゔ'  :'vu',   'ゔぇ':'ve',   'ゔぉ':'vo',
            'ゔゃ':'vya',                 'ゔゅ':'vyu',                 'ゔょ':'vyo',
            'あ':'a',   'い':'i',   'う':'u',   'え':'e',   'お':'o',
            'か':'ka',  'き':'ki',  'く':'ku',  'け':'ke',  'こ':'ko',
            'が':'ga',  'ぎ':'gi',  'ぐ':'gu',  'げ':'ge',  'ご':'go',
            'さ':'sa',  'し':'si',  'す':'su',  'せ':'se',  'そ':'so',
            'ざ':'za',  'じ':'zi',  'ず':'zu',  'ぜ':'ze',  'ぞ':'zo',
            'た':'ta',  'ち':'ti',  'つ':'tu',  'て':'te',  'と':'to',
            'だ':'da',  'ぢ':'di',  'づ':'du',  'で':'de',  'ど':'do',
            'な':'na',  'に':'ni',  'ぬ':'nu',  'ね':'ne',  'の':'no',
            'は':'ha',  'ひ':'hi',  'ふ':'fu',  'へ':'he',  'ほ':'ho',
            'ば':'ba',  'び':'bi',  'ぶ':'bu',  'べ':'be',  'ぼ':'bo',
            'ぱ':'pa',  'ぴ':'pi',  'ぷ':'pu',  'ぺ':'pe',  'ぽ':'po',
            'ま':'ma',  'み':'mi',  'む':'mu',  'め':'me',  'も':'mo',
            'や':'ya',              'ゆ':'yu',              'よ':'yo',
            'ら':'ra',  'り':'ri',  'る':'ru',  'れ':'re',  'ろ':'ro',
            'わ':'wa',  'ゐ':'wyi',             'ゑ':'wye', 'を':'wo',
            'ん':'n',   'っ':'xtu', 'ゕ':'xka', 'ゖ':'xke', 'ゎ':'xwa',
            'ぁ':'xa',  'ぃ':'xi',  'ぅ':'xu',  'ぇ':'xe',  'ぉ':'xo',
            'ゃ':'xya',             'ゅ':'xyu',             'ょ':'xyo',
            'ー': '-',   '、':',',   '。':'.',
        }
        super().__init__('Romaji', table)

    def apply(self, text):
        """
        文字列をローマ字列に変換する
        """
        def roman(m):
            return self.lookup(m[0])
        text = re.sub(r'[ぁ-ぢつ-をゔゕゖー、。]+', roman, text) # 「ん」「っ」以外 
        text = re.sub(r'ん(?=[aeinouyん])', r'nn', text)
        text = re.sub(r'っ([bcdfghjkmpqrstvwz])', r'\1\1', text)
        text = re.sub(r'[んっ]+', roman, text)
        return text
