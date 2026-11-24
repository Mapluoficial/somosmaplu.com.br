"""Usado pelo GitHub Actions: baixa as imagens das matérias (img_url) e gera o site com build.py."""
import json, glob, os, io, urllib.request
from PIL import Image
import build


def baixa_imagens():
    os.makedirs('img', exist_ok=True)
    for f in glob.glob('_dados/*.json'):
        for m in json.load(open(f))['materias']:
            if m.get('img_url') and not os.path.exists('img/' + m['img']):
                req = urllib.request.Request(m['img_url'], headers={'User-Agent': 'Mozilla/5.0'})
                im = Image.open(io.BytesIO(urllib.request.urlopen(req, timeout=60).read())).convert('RGB')
                w, h = im.size; t = 16 / 9
                if w / h > t:
                    nw = int(h * t); im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
                else:
                    nh = int(w / t); y = max(0, (h - nh) // 3); im = im.crop((0, y, w, y + nh))
                im.resize((1200, 675), Image.LANCZOS).save('img/' + m['img'], quality=82, optimize=True)
                print('imagem', m['img'])


baixa_imagens()
build.main()
