import json
import re
from collections import Counter
from IPython.display import HTML, Javascript
from pathlib import Path

class Evaluation:
    """
    評価値を表すクラス
    """
    def __init__(self, corpus, method, layout):
        self.corpus = corpus
        self.method = method
        self.layout = layout
        self.c_key = Counter() # キーごとの打鍵数
        self.c_han = Counter() # 手ごとの打鍵数
        self.c_fin = Counter() # 指ごとの打鍵数
        self.c_row = Counter() # 段ごとの打鍵数
        self.c_col = Counter() # 列ごとの打鍵数
        self.total = 0 # 打鍵数
        self.act = 0 # 動作数（同時打鍵を1と数える）
        self.sft = 0 # シフト数
        self.alt = 0 # 両手交互
        self.arp = 0 # 片手異指同段（アルペジオ）
        self.sf = [0, 0, 0, 0, 0] # 片手同指 [同段, 1段違い, 2段違い, 3段違い]
        self.ignored = set() # 数えなかった文字
        
    def __str__(self):
        r = \
        "{:>10} 打鍵\n" \
        "{:>10} 動作\n" \
        "{:>10} シフト\n" \
        "{:>10} 交互\n" \
        "{:>10} アルペジオ\n" \
        "{:>10} 同指連続（同段）\n" \
        "{:>10} 同指連続（1段違い）\n" \
        "{:>10} 同指連続（2～3段違い）" \
        .format(self.total, self.act, self.sft, self.alt, self.arp, self.sf[0], self.sf[1], self.sf[2] + self.sf[3])
        return r

    def heatmap(self):
        mydir = Path(__file__).parent
        buf = '''
<style type="text/css">
    #keyboard {{
        position:relative;
        width:800px;
        margin:auto;
        height:373px;
        bottom:0;
        padding:0;
        background-image:url({imgdir}/{name}.png);
    }}
</style>
<div id="customize">
    <select id="layout">
        <option value="MicroTRON_QWERTY">MicroTRON QWERTY</option>
        <option value="QWERTY">QWERTY</option>
    </select>
</div>
<div id="keyboard"></div>
<script type="text/javascript">
    var app = {{}};
    app.config = {{
        imgdir: "{imgdir}",
    }};
    app.data = {data};
</script>
<script src="{libdir}/heatmap.js"></script>
<script src="{libdir}/keyboard-layouts.js"></script>
<script src="{libdir}/app.js"></script>
        '''.format(
            imgdir=mydir.joinpath('../img').resolve().relative_to(Path.cwd()),
            libdir=mydir.joinpath('../js').resolve().relative_to(Path.cwd()), 
            data=json.dumps(self.c_key, sort_keys=True),
            name=self.layout.name
        )
        buf = re.sub(r'<(option .+?)>({}</option>)'.format(self.layout.name), r'<\1 selected>\2', buf)
        return HTML(buf)
