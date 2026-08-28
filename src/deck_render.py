"""Renders the deck spec into a self-contained, presentable HTML deck.
Charts are inlined as SVG so the slide type and the chart type are literally the
same webfont, and everything stays crisp at projector resolution."""
import html, json, re
from pathlib import Path
from deck_style import brl, pct

ROOT = Path(__file__).resolve().parent.parent
CH = ROOT/'output'/'charts'

def svg(name):
    p = CH/f'{name}.svg'
    if not p.exists(): return ''
    s = p.read_text()
    s = re.sub(r'<metadata>.*?</metadata>', '', s, flags=re.S)
    return f'<figure class="fig">{s}</figure>'

def e(x): return html.escape(str(x))

CSS = """
*{box-sizing:border-box}
:root{
 --ink:#101816; --ink2:#535d59; --ink3:#7c8681; --line:#dae0db; --line2:#b9c3bd;
 --paper:#fbfcfa; --paper2:#f1f4f1; --stage:#0d1211; --accent:#0d5b66;
 --s1:#2a78d6; --s2:#eb6834; --s3:#1baf7a; --neutral:#9aa5a0;
}
html,body{height:100%}
body{background:var(--stage);color:var(--ink);margin:0;
 font-family:"IBM Plex Sans",-apple-system,Segoe UI,Roboto,sans-serif;overflow:hidden}
.stage{position:fixed;inset:0;display:grid;place-items:center}
.slide{position:absolute;width:1280px;height:720px;background:var(--paper);
 padding:52px 62px 44px;display:none;flex-direction:column;gap:18px;
 box-shadow:0 30px 80px rgba(0,0,0,.45);transform-origin:center}
.slide.on{display:flex}
.eyebrow{display:flex;align-items:baseline;gap:12px;font-size:12px;letter-spacing:.16em;
 text-transform:uppercase;color:var(--accent);font-weight:600}
.eyebrow .n{font-variant-numeric:tabular-nums;color:var(--ink3)}
.eyebrow .rule{flex:1;height:1px;background:var(--line)}
h1{font-family:"Bricolage Grotesque","IBM Plex Sans",sans-serif;font-weight:700;
 letter-spacing:-.022em;line-height:1.07;margin:0;font-size:37px;text-wrap:balance;max-width:22ch}
h2{font-family:"Bricolage Grotesque","IBM Plex Sans",sans-serif;font-weight:700;
 letter-spacing:-.02em;line-height:1.1;margin:0;font-size:31px;text-wrap:balance}
.standfirst{font-size:18px;line-height:1.5;color:var(--ink2);max-width:70ch}
.body{flex:1;display:flex;gap:34px;min-height:0}
.body.col{flex-direction:column;gap:14px}
.fig{margin:0;flex:1;min-width:0;display:flex;align-items:center;justify-content:center}
.fig svg{width:100%;height:100%;max-height:100%}
.side{width:330px;flex:none;display:flex;flex-direction:column;gap:14px;justify-content:center}
ul.pts{margin:0;padding:0;list-style:none;display:flex;flex-direction:column;gap:13px}
ul.pts li{font-size:15.5px;line-height:1.45;color:var(--ink2);padding-left:17px;position:relative}
ul.pts li::before{content:"";position:absolute;left:0;top:.66em;width:9px;height:1px;background:var(--line2)}
ul.pts.row{flex-direction:row;gap:30px}
ul.pts.row li{flex:1}
b,strong{color:var(--ink);font-weight:600}
.kpis{display:grid;grid-template-columns:repeat(5,1fr);gap:1px;background:var(--line)}
.kpi{background:var(--paper);padding:16px 16px 18px;display:flex;flex-direction:column;gap:6px}
.kpi .l{font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--ink3);font-weight:600}
.kpi .v{font-family:"Bricolage Grotesque",sans-serif;font-size:33px;font-weight:700;
 letter-spacing:-.02em;line-height:1;font-variant-numeric:tabular-nums}
.kpi .n{font-size:12.5px;line-height:1.35;color:var(--ink2)}
.verdict{border-left:4px solid var(--s2);padding:12px 0 12px 20px;display:flex;flex-direction:column;gap:6px}
.verdict .t{font-family:"Bricolage Grotesque",sans-serif;font-size:17px;font-weight:700;color:var(--s2)}
.verdict .b{font-size:15.5px;line-height:1.5;color:var(--ink2);max-width:96ch}
.two{display:flex;gap:26px;flex:1;min-height:0}
.two .fig{flex:1}
.spec{display:grid;grid-template-columns:auto 1fr;gap:11px 26px;align-content:start;
 font-size:16px;line-height:1.4}
.spec dt{color:var(--ink3);font-size:12px;letter-spacing:.09em;text-transform:uppercase;
 font-weight:600;padding-top:3px;white-space:nowrap}
.spec dd{margin:0;color:var(--ink)}
.cmp{display:flex;flex-direction:column;gap:12px;width:430px;flex:none;justify-content:center}
.cmp .row{display:flex;flex-direction:column;gap:5px}
.cmp .lab{display:flex;justify-content:space-between;font-size:14px;color:var(--ink2)}
.cmp .lab b{font-size:15px}
.cmp .bar{height:14px;background:var(--paper2)}
.cmp .bar i{display:block;height:100%}
.cmp .tag{font-size:10.5px;letter-spacing:.09em;text-transform:uppercase;font-weight:600}
.steps{display:grid;grid-template-columns:repeat(4,1fr);gap:22px}
.step{display:flex;flex-direction:column;gap:7px;border-top:2px solid var(--accent);padding-top:11px}
.step .n{font-size:11px;letter-spacing:.12em;color:var(--accent);font-weight:600}
.step .t{font-family:"Bricolage Grotesque",sans-serif;font-size:16.5px;font-weight:700}
.step .d{font-size:13.5px;line-height:1.42;color:var(--ink2)}
.limits{border-top:1px solid var(--line);padding-top:12px;display:flex;gap:26px}
.limits .h{font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--ink3);
 font-weight:600;width:120px;flex:none;padding-top:2px}
.foot{display:flex;justify-content:space-between;align-items:baseline;border-top:1px solid var(--line);
 padding-top:11px;font-size:11.5px;color:var(--ink3);letter-spacing:.04em}
.foot .pg{font-variant-numeric:tabular-nums}
.tbl{width:100%;border-collapse:collapse;font-size:14px;font-variant-numeric:tabular-nums}
.tbl th{text-align:left;font-size:10.5px;letter-spacing:.09em;text-transform:uppercase;color:var(--ink3);
 font-weight:600;padding:0 12px 8px 0;border-bottom:1px solid var(--line2);white-space:nowrap}
.tbl td{padding:9px 12px 9px 0;border-bottom:1px solid var(--line);white-space:nowrap}
.tbl tr.rec td{background:#eaf2fc;font-weight:600}
.tbl tr.slv td{background:#e8f7f1}
.tbl tr.hyp td{color:var(--s2)}
ul.ev{margin:0;padding:0;list-style:none;display:grid;grid-template-columns:1fr 1fr;gap:9px 26px}
ul.ev li{font-size:13.5px;line-height:1.42;color:var(--ink2)}
.tagk{display:inline-block;font-size:9.5px;letter-spacing:.11em;font-weight:700;padding:1px 6px;
 margin-right:8px;vertical-align:1px;border:1px solid currentColor}
.tdado{color:var(--s3)} .thipótese{color:var(--s2)} .tinferido{color:var(--accent)}
.chain{display:flex;gap:0;align-items:stretch;border-top:1px solid var(--line);padding-top:14px}
.chain .link{flex:1;display:flex;flex-direction:column;gap:4px;padding:0 18px;border-left:1px solid var(--line)}
.chain .link:first-child{padding-left:0;border-left:none}
.chain .k{font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);font-weight:600}
.chain .v{font-size:14px;line-height:1.35;color:var(--ink)}
/* chrome */
.hud{position:fixed;bottom:18px;right:22px;display:flex;gap:14px;align-items:center;
 color:#7d8a86;font-size:12px;letter-spacing:.08em;z-index:20}
.hud button{background:none;border:1px solid #2a3431;color:#9fada8;font:inherit;
 padding:5px 11px;cursor:pointer;letter-spacing:.08em}
.hud button:hover{border-color:#4a5652;color:#d6e0dc}
.hud button:focus-visible{outline:2px solid var(--s3);outline-offset:2px}
.notes{position:fixed;left:0;right:0;bottom:0;background:#111917;color:#c7d2ce;
 padding:16px 26px 20px;font-size:14.5px;line-height:1.5;border-top:1px solid #223029;
 display:none;z-index:15;max-height:34vh;overflow:auto}
.notes.on{display:block}
.notes .h{font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:#5f6f6a;
 font-weight:600;margin-bottom:6px}
.grid{position:fixed;inset:0;background:#0d1211;overflow:auto;padding:34px;display:none;z-index:30}
.grid.on{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:18px;align-content:start}
.card{background:var(--paper);padding:14px 15px;cursor:pointer;display:flex;flex-direction:column;gap:7px;
 border:2px solid transparent}
.card:hover{border-color:var(--s3)}
.card .n{font-size:10px;letter-spacing:.13em;text-transform:uppercase;color:var(--accent);font-weight:600}
.card .t{font-family:"Bricolage Grotesque",sans-serif;font-size:14px;font-weight:700;line-height:1.2}
@media print{
 body{background:#fff;overflow:visible}
 .stage{position:static;display:block}
 .slide{display:flex!important;position:relative;transform:none!important;page-break-after:always;
  box-shadow:none;width:100%;height:auto;min-height:0;aspect-ratio:16/9}
 .hud,.notes,.grid{display:none!important}
 @page{size:1280px 720px;margin:0}
}
"""

JS = """
const slides=[...document.querySelectorAll('.slide')];let i=0;
function fit(){const s=slides[i];if(!s)return;
 const k=Math.min(innerWidth/1280,(innerHeight-(document.getElementById('notes').classList.contains('on')?260:0))/720)*0.94;
 slides.forEach(x=>x.style.transform='scale('+k+')');}
function go(n){i=Math.max(0,Math.min(slides.length-1,n));
 slides.forEach((s,j)=>s.classList.toggle('on',j===i));
 document.getElementById('cur').textContent=(i+1)+' / '+slides.length;
 document.getElementById('nt').innerHTML='<div class="h">Notas do apresentador · lâmina '+(i+1)+'</div>'+(slides[i].dataset.notes||'—');
 fit();}
addEventListener('keydown',e=>{
 if(e.key==='ArrowRight'||e.key===' '||e.key==='PageDown'){e.preventDefault();go(i+1)}
 else if(e.key==='ArrowLeft'||e.key==='PageUp'){e.preventDefault();go(i-1)}
 else if(e.key==='Home'){go(0)} else if(e.key==='End'){go(slides.length-1)}
 else if(e.key==='n'||e.key==='N'){toggleNotes()}
 else if(e.key==='g'||e.key==='G'||e.key==='Escape'){toggleGrid()}
 else if(e.key==='p'||e.key==='P'){print()}});
function toggleNotes(){document.getElementById('notes').classList.toggle('on');fit()}
function toggleGrid(){document.getElementById('grid').classList.toggle('on')}
document.querySelectorAll('.card').forEach((c,j)=>c.addEventListener('click',()=>{go(j);toggleGrid()}));
addEventListener('resize',fit);go(0);
"""

def render(spec):
    n = len(spec['slides'])
    out = []
    for k, s in enumerate(spec['slides']):
        out.append(slide_html(s, k+1, n, spec))
    cards = ''.join(
        f'<div class="card"><div class="n">{j+1:02d} · {e(s["section"])}</div>'
        f'<div class="t">{e(s["headline"])}</div></div>' for j, s in enumerate(spec['slides']))
    return f"""<title>{e(spec['title'])}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,700&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<style>{CSS}</style>
<div class="stage">{''.join(out)}</div>
<div class="grid" id="grid">{cards}</div>
<div class="notes" id="notes"><div id="nt"></div></div>
<div class="hud">
  <span id="cur"></span>
  <button onclick="go(i-1)" aria-label="lâmina anterior">◀</button>
  <button onclick="go(i+1)" aria-label="próxima lâmina">▶</button>
  <button onclick="toggleGrid()">Índice · G</button>
  <button onclick="toggleNotes()">Notas · N</button>
  <button onclick="print()">PDF · P</button>
</div>
<script>{JS}</script>"""

def slide_html(s, k, n, spec):
    lay = s.get('layout', 'chart')
    head = (f'<div class="eyebrow"><span class="n">{k:02d}</span><span>{e(s["section"])}</span>'
            f'<span class="rule"></span></div><h1>{e(s["headline"])}</h1>')
    body = ''
    if lay == 'kpi':
        kp = ''.join(f'<div class="kpi"><span class="l">{e(x["label"])}</span>'
                     f'<span class="v">{e(x["value"])}</span><span class="n">{e(x["note"])}</span></div>'
                     for x in s['kpis'])
        v = s['verdict']
        body = (f'<div class="body col"><p class="standfirst">{e(s["standfirst"])}</p>'
                f'<div class="kpis">{kp}</div>'
                f'<div class="verdict"><span class="t">{e(v["title"])}</span>'
                f'<span class="b">{e(v["body"])}</span></div></div>')
    elif lay == 'profile':
        sp = ''.join(f'<dt>{e(a)}</dt><dd>{e(b)}</dd>' for a, b in s['spec'])
        mx = max(c['yield_'] for c in s['compare'])
        colmap = {'recomendado': 'var(--s1)', 'parcela de liquidez': 'var(--s3)',
                  'a hipótese': 'var(--s2)', 'evitar': 'var(--neutral)'}
        rows = ''.join(
            f'<div class="row"><div class="lab"><span>{e(c["label"])}'
            f' <span class="tag" style="color:{colmap[c["tag"]]}">{e(c["tag"])}</span></span>'
            f'<b>{pct(c["yield_"])}</b></div>'
            f'<div class="bar"><i style="width:{c["yield_"]/mx*100:.1f}%;background:{colmap[c["tag"]]}"></i></div></div>'
            for c in s['compare'])
        body = (f'<div class="body"><dl class="spec">{sp}</dl>'
                f'<div class="cmp">{rows}</div></div>')
    elif lay == 'segments':
        hdr = ''.join(f'<th>{e(h)}</th>' for h in
                      ['Segmento','Anúncios','Hóspedes','Dorm','Diária','Ocupação','Receita/ano','Concentração na alta'])
        rws = ''.join('<tr>' + ''.join(f'<td>{e(v)}</td>' for v in
                      [r['seg'], r['n'], r['guests'], r['dorm'], r['adr'], r['occ'], r['rev'], r['season']]) + '</tr>'
                      for r in s['rows'])
        ev = ''.join(f'<li><span class="tagk t{k.lower()}">{e(k)}</span>{e(v)}</li>' for k, v in s['evidence'])
        body = (f'<div class="body col"><p class="standfirst">{e(s["standfirst"])}</p>'
                f'<table class="tbl"><thead><tr>{hdr}</tr></thead><tbody>{rws}</tbody></table>'
                f'<ul class="ev">{ev}</ul></div>')
    elif lay == 'matrix':
        hdr = ''.join(f'<th>{e(h)}</th>' for h in s['cols'])
        rws = ''.join(f'<tr class="{r["tone"]}">' + ''.join(f'<td>{e(c)}</td>' for c in r['cells']) + '</tr>'
                      for r in s['rows'])
        ch = ''.join(f'<div class="link"><span class="k">{e(k)}</span><span class="v">{e(v)}</span></div>'
                     for k, v in s['chain'])
        body = (f'<div class="body col"><table class="tbl"><thead><tr>{hdr}</tr></thead><tbody>{rws}</tbody></table>'
                f'<div class="chain">{ch}</div></div>')
    elif 'steps' in s:
        st = ''.join(f'<div class="step"><span class="n">PASSO {j+1}</span>'
                     f'<span class="t">{e(t)}</span><span class="d">{e(d)}</span></div>'
                     for j, (t, d) in enumerate(s['steps']))
        body = (f'<div class="body col">{svg(s["chart"])}<div class="steps">{st}</div></div>')
    elif 'charts' in s:
        figs = ''.join(svg(c) for c in s['charts'])
        pts = ''.join(f'<li>{e(b)}</li>' for b in s.get('bullets', []))
        lim = ''
        if s.get('limits'):
            lim = ('<div class="limits"><span class="h">O que a base não sustenta</span>'
                   '<ul class="pts row">' + ''.join(f'<li>{e(x)}</li>' for x in s['limits']) + '</ul></div>')
        body = (f'<div class="body col"><div class="two">{figs}</div>'
                f'<ul class="pts row">{pts}</ul>{lim}</div>')
    else:
        pts = ''.join(f'<li>{e(b)}</li>' for b in s.get('bullets', []))
        second = svg(s['secondary']) if s.get('secondary') else ''
        if second:
            body = (f'<div class="body col"><div class="two">{svg(s["chart"])}{second}</div>'
                    f'<ul class="pts row">{pts}</ul></div>')
        else:
            body = (f'<div class="body">{svg(s["chart"])}'
                    f'<div class="side"><ul class="pts">{pts}</ul></div></div>')
    m = spec['meta']
    foot = (f'<div class="foot"><span>{e(spec["title"])} · {e(m["source"])}</span>'
            f'<span class="pg">{k:02d} / {n:02d}</span></div>')
    notes = e(s.get('notes', ''))
    return f'<section class="slide" data-notes="{notes}">{head}{body}{foot}</section>'
