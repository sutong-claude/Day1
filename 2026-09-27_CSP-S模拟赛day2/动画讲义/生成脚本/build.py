# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import g0, gA, gB, gC, gD

TITLE = 'Day2 四题动画复盘'
parts = [g0.head(), g0.summary(), g0.tl(), gA.build(), gB.build(), gC.build(), gD.build(), g0.env(), g0.how(), g0.cheat()]
body = '\n'.join(parts).replace('{NANIM}', str(COUNT['fp'] + COUNT['ca']))
css = D1CSS + EXTRA
js = bundle_js()
inner = '<title>%s</title>\n<style>%s</style>\n<div class="wrap">\n%s\n</div>\n<script>%s</script>\n' % (TITLE, css, body, js)
out_dir = sys.argv[1]
os.makedirs(out_dir, exist_ok=True)
# 仓库里的版本：完整文档，双击就能打开
open(os.path.join(out_dir, 'Day2四题动画复盘.html'), 'w', encoding='utf-8').write(
    '<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
    + inner.replace('<div class="wrap">', '</head><body><div class="wrap">', 1) + '</body></html>\n')
# 发布版：不带外壳（发布时会自动套上）
open(os.path.join(out_dir, 'publish.html'), 'w', encoding='utf-8').write(inner)
print('动画 %d 段（逐帧 %d，代码 %d）' % (COUNT['fp'] + COUNT['ca'], COUNT['fp'], COUNT['ca']))
