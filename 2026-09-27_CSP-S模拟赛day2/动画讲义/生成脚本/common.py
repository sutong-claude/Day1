# -*- coding: utf-8 -*-
"""Day2 讲义公共组件：沿用 Day1 讲义的样式（d1all.css）和两个播放器（逐帧 fp、代码逐行 codeanim）。"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
D1CSS = open(os.path.join(HERE, '..', 'd1all.css'), encoding='utf-8').read()

EXTRA = r'''
nav{top:env(safe-area-inset-top,0px)}
.tlt{font-size:.9rem}
.tlt td.tm{white-space:nowrap;font-family:"JetBrains Mono","Consolas",monospace;font-size:.85rem;color:var(--soft)}
.tlt tr.ph td{background:var(--now);font-weight:700;color:var(--blue);font-family:"Songti SC","Noto Serif SC","STSong","SimSun",serif}
.tlt tr.bad td:last-child{color:var(--red);font-weight:600}
.tlt tr.key td:last-child{color:var(--green);font-weight:600}
.tlt code{font-size:.85em}
.fix{border:1px solid var(--line);border-left:6px solid var(--green);background:var(--card);padding:10px 16px;margin:14px 0}
.fix b{color:var(--green)}
.grid64{display:block;margin:0 auto;max-width:100%;height:auto}
.okc{fill:var(--gbg);stroke:var(--green);stroke-width:1.2}
.noc{fill:var(--rbg);stroke:var(--red);stroke-width:2}
.big{font-size:26px;font-weight:700;font-family:"JetBrains Mono","Consolas",monospace}
.arrow-r{stroke:var(--red);stroke-width:2.6;fill:none}
.arrow-b{stroke:var(--blue);stroke-width:2.6;fill:none}
.ah-r{fill:var(--red)} .ah-b{fill:var(--blue)}
.pt{fill:var(--card);stroke:var(--ink);stroke-width:1.6}
.pt-on{fill:var(--ybg);stroke:#B8860B;stroke-width:2.6}
.pt-good{fill:var(--gbg);stroke:var(--green);stroke-width:2.6}
.bar{fill:var(--bbg);stroke:var(--blue);stroke-width:1.4}
.bar-up{fill:var(--ybg);stroke:#B8860B;stroke-width:2.4}
.hline{stroke:var(--red);stroke-width:2;stroke-dasharray:6 4}
'''

JS_RUNTIME = r'''
document.documentElement.classList.add('js');
document.querySelectorAll('.codeanim').forEach(function(box){
  var name=box.getAttribute('data-ca'); var steps=(typeof CA!=='undefined')?CA[name]:null;
  if(!steps||!steps.length) return;
  var lines=box.querySelectorAll('.ca-l'), vars=box.querySelector('.ca-vars'),
      note=box.querySelector('.ca-note'), pos=box.querySelector('.ca-pos'),
      bp=box.querySelector('.ca-prev'), bn=box.querySelector('.ca-next'),
      bpl=box.querySelector('.ca-play'), br=box.querySelector('.ca-reset');
  var cur=0, timer=null;
  function render(){
    var s=steps[cur], i;
    for(i=0;i<lines.length;i++){
      var ln=+lines[i].getAttribute('data-l');
      lines[i].className='ca-l'+(ln===s.l?' ca-cur':'');
    }
    var html='<table>',k;
    var pv=(cur>0)?steps[cur-1].v:{};
    for(k in s.v){ var chg=(pv[k]===undefined)||(pv[k]!==s.v[k]);
      html+='<tr'+(chg&&cur>0?' class="chg"':'')+'><td>'+k+'</td><td>'+s.v[k]+'</td></tr>'; }
    html+='</table>'; vars.innerHTML=html;
    note.innerHTML=s.n;
    pos.textContent='第 '+(cur+1)+' / '+steps.length+' 步';
    bp.disabled=(cur===0); bn.disabled=(cur===steps.length-1);
  }
  function stop(){ if(timer){clearInterval(timer);timer=null;bpl.textContent='▶ 自动播放';} }
  bp.addEventListener('click',function(){stop();if(cur>0){cur--;render();}});
  bn.addEventListener('click',function(){stop();if(cur<steps.length-1){cur++;render();}});
  br.addEventListener('click',function(){stop();cur=0;render();});
  bpl.addEventListener('click',function(){
    if(timer){stop();return;}
    if(cur>=steps.length-1) cur=0;
    bpl.textContent='❚❚ 暂停';
    timer=setInterval(function(){ if(cur<steps.length-1){cur++;render();} else stop(); },1100);
    render();
  });
  render();
});
document.querySelectorAll('.fp').forEach(function(box){
  var fr=(typeof FP!=='undefined')?FP[box.getAttribute('data-fp')]:null; if(!fr||!fr.length) return;
  var fig=box.querySelector('.fp-fig'),note=box.querySelector('.fp-note'),pos=box.querySelector('.fp-pos'),
      bp=box.querySelector('.fp-prev'),bn=box.querySelector('.fp-next'),bpl=box.querySelector('.fp-play'),
      br=box.querySelector('.fp-reset'),bs=box.querySelector('.fp-spd');
  var cur=0,timer=null,spd=[[2600,'慢'],[1700,'中'],[950,'快']],si=1;
  function render(){fig.innerHTML=fr[cur].s;note.innerHTML=fr[cur].n;
    pos.textContent='第 '+(cur+1)+' / '+fr.length+' 帧';bp.disabled=cur===0;bn.disabled=cur===fr.length-1;}
  function stop(){if(timer){clearInterval(timer);timer=null;bpl.textContent='▶ 自动播放';}}
  function go(){timer=setInterval(function(){if(cur<fr.length-1){cur++;render();}else stop();},spd[si][0]);}
  bp.addEventListener('click',function(){stop();if(cur>0){cur--;render();}});
  bn.addEventListener('click',function(){stop();if(cur<fr.length-1){cur++;render();}});
  br.addEventListener('click',function(){stop();cur=0;render();});
  bs.addEventListener('click',function(){si=(si+1)%3;bs.textContent='速度：'+spd[si][1];if(timer){clearInterval(timer);go();}});
  bpl.addEventListener('click',function(){if(timer){stop();return;}if(cur>=fr.length-1)cur=0;bpl.textContent='❚❚ 暂停';render();go();});
  render();
});
'''

FP = {}
CA = {}
COUNT = {'fp': 0, 'ca': 0}


def esc(t):
    return str(t).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def fp(name, title, frames, cap=''):
    """frames: [(svg字符串, 说明html)]"""
    COUNT['fp'] += 1
    FP[name] = [{'s': s, 'n': n} for s, n in frames]
    allnotes = ''.join('<li>%s</li>' % n for _, n in frames)
    return ('<div class="fp" data-fp="%s"><div class="fp-hd">%s　·　共 %d 帧</div>'
            '<div class="fp-fig">%s</div><div class="fp-note">%s</div>'
            '<div class="fp-bar"><button type="button" class="fp-prev">上一步</button><span class="fp-pos"></span>'
            '<button type="button" class="fp-next next">下一步</button><button type="button" class="fp-play">▶ 自动播放</button>'
            '<button type="button" class="fp-reset">回到开头</button><button type="button" class="fp-spd">速度：中</button></div>'
            '<details class="fp-all"><summary>把每一帧的文字说明一次看完</summary><ol>%s</ol></details>%s</div>'
            ) % (name, title, len(frames), frames[0][0], frames[0][1], allnotes,
                 ('<p class="cap">%s</p>' % cap) if cap else '')


def codeanim(name, title, code, steps, cap=''):
    COUNT['ca'] += 1
    CA[name] = steps
    lines = ''.join('<div class="ca-l" data-l="%d"><span class="ca-n">%d</span>%s</div>' % (i + 1, i + 1, esc(t))
                    for i, t in enumerate(code))
    fb = steps[0]['n'].replace('<b>', '').replace('</b>', '')
    return ('<div class="codeanim" data-ca="%s"><div class="ca-hd">%s　·　共 %d 步</div>'
            '<div class="ca-top"><pre class="ca-code">%s</pre><div class="ca-vars"></div></div>'
            '<div class="ca-note"></div><div class="ca-bar"><button type="button" class="ca-prev">上一步</button>'
            '<span class="ca-pos"></span><button type="button" class="ca-next">下一步</button>'
            '<button type="button" class="ca-play">▶ 自动播放</button><button type="button" class="ca-reset">回到开头</button></div>'
            '<div class="ca-fallback">%s</div>%s</div>'
            ) % (name, title, len(steps), lines, fb, ('<p class="cap">%s</p>' % cap) if cap else '')


# ---------- SVG 小工具 ----------
def svg(w, h, body):
    return '<svg viewBox="0 0 %d %d" width="%d" height="%d" role="img" class="fpsvg">%s</svg>' % (w, h, w, h, ''.join(body))


def R(x, y, w, h, cls='bx', rx=6):
    return '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%d" class="%s"/>' % (x, y, w, h, rx, cls)


def Tx(x, y, t, cls='tlab', anchor='middle'):
    return '<text x="%.1f" y="%.1f" text-anchor="%s" class="%s">%s</text>' % (x, y, anchor, cls, esc(t))


def L(x1, y1, x2, y2, cls='ed'):
    return '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" class="%s"/>' % (x1, y1, x2, y2, cls)


def C(x, y, r, cls='nd'):
    return '<circle cx="%.1f" cy="%.1f" r="%.1f" class="%s"/>' % (x, y, r, cls)


def arrow(x1, y1, x2, y2, color='r'):
    import math
    dx, dy = x2 - x1, y2 - y1
    d = math.hypot(dx, dy)
    if d < 1e-9:
        return ''
    ux, uy = dx / d, dy / d
    hx, hy = x2 - ux * 9, y2 - uy * 9
    px, py = -uy * 5, ux * 5
    return (L(x1, y1, hx, hy, 'arrow-' + color) +
            '<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" class="ah-%s"/>' % (x2, y2, hx + px, hy + py, hx - px, hy - py, color))


def table(head, rows, cls=''):
    h = '<div class="tw"><table%s><tr>%s</tr>' % ((' class="%s"' % cls) if cls else '', ''.join('<th>%s</th>' % x for x in head))
    for r in rows:
        h += '<tr>%s</tr>' % ''.join('<td>%s</td>' % x for x in r)
    return h + '</table></div>'


def bundle_js():
    return ('var FP=%s;\nvar CA=%s;\n' % (json.dumps(FP, ensure_ascii=False), json.dumps(CA, ensure_ascii=False))) + JS_RUNTIME
