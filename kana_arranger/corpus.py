import bz2
import os
import re
import requests
import tarfile
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit

class Corpus:
    """
    コーパスを表すクラス
    """
    def __init__(self):
        self.src = ''
        self.freq = Counter()

    def download_binary(self, url, save_dir=None, save_name=None):
        r = requests.get(url, stream=True)
        if not save_dir:
            save_dir = os.getcwd()
        save_dir = Path(save_dir)
        if not save_name:
            save_name = Path(urlsplit(url).path).name
        if not save_name:
            save_name = Path(urlsplit(r.url).path).name
        print("Downloading {}".format(url))
        with open(save_dir/save_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                f.write(chunk)

    def extract_tarfile(self, tar_path, dst_dir=None, members=[]):
        with tarfile.open(tar_path) as z:
            for item in z:
                if item.name in members:
                    print("Extracting {}".format(item.name))
                    z.extract(item, path=dst_dir)

class KkcBccwjCore(Corpus):
    """
    BCCWJコアデータ かな漢字変換用3-gram
    """
    url = 'http://www.ar.media.kyoto-u.ac.jp/member/gologo/kkc-BCCWJCore.tar'
    # この正規表現にマッチしない記号等を読み飛ばす
    rx0 = re.compile(r'[、。，．々〆〇\u3041-\u30FF\u4E00-\u9FFF]+/([、。ぁ-ろわをんヴー]+)$')

    def __init__(self, corpus_dir, cutoff=1):
        Corpus.__init__(self)
        # コーパスをダウンロードして読み込む
        corpus_dir = Path(corpus_dir).expanduser()
        bccwj_dir = corpus_dir/'bccwj'
        tar_path = corpus_dir/'kkc-BCCWJCore.tar'
        fwk_path = bccwj_dir/'3-gram.fwk.bz2'
        if not tar_path.exists():
            corpus_dir.mkdir(parents=True, exist_ok=True)
            self.download_binary(KkcBccwjCore.url, corpus_dir, tar_path.name)
        if not fwk_path.exists():
            bccwj_dir.mkdir(parents=True, exist_ok=True)
            self.extract_tarfile(tar_path, bccwj_dir, [fwk_path.name])
        self.load_fwk(fwk_path, cutoff)
        
    def load_fwk(self, bz2_path, cutoff=1):
        print("Loading {}".format(bz2_path))
        self.src = bz2_path
        self.freq.clear()
        with bz2.open(bz2_path, 'rt', encoding='euc_jp') as f:
            for line in f:
                e = line.split()
                n = int(e[0])
                if n < cutoff: break
                ws = [self.yomi(x) for x in e[1:]]
                for w in ''.join(ws).split():
                    self.freq[w] += n
        # [TODO] 2字連接頻度を計算する場合は、単語またぎの頻度を1.5倍する。
    
    def yomi(self, pair):
        m = KkcBccwjCore.rx0.match(pair)
        if not m: return ' '
        return m[1].replace('ヴ', 'ゔ')