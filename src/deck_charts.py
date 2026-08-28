"""Decision-oriented charts for the executive deck.

Every chart follows three rules: the title states the finding, not the variable;
the numbers that matter are printed on the marks; and a reader with no presenter
can still get the point. Rendered to SVG so slide type and chart type match.
"""
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import deck_style as ds
from deck_style import S1, S2, S3, NEUTRAL, INK, INK_2, INK_3, LINE, LINE_STR, ACCENT, BAD
from deck_data import seg_label, zpt

REC = ('Morretes', 2)          # recommended core segment
HYP = ('Centro', 1)            # the internal hypothesis
SLEEVE = ('Meia Praia (beach band)', 2)

def _c(z, b):
    if (z, b) == REC: return S1
    if (z, b) == HYP: return S2
    if (z, b) == SLEEVE: return S3
    return NEUTRAL


def _two_line(z, b):
    return f'{zpt(z)}\n{int(b)} dorm'

def place_labels(ax, pts, texts, colors, bold, radii, fontsize=10.2, pad=4):
    """Greedy collision-free labelling: eight candidate slots around each point,
    first non-overlapping one wins, faint leader line when the label is displaced."""
    fig = ax.figure; fig.canvas.draw()
    T = ax.transData.transform
    boxes = []
    def hit(b):
        return any(not (b[2] < o[0] or b[0] > o[2] or b[3] < o[1] or b[1] > o[3]) for o in boxes)
    order = sorted(range(len(pts)), key=lambda i: (0 if bold[i] else 1, -radii[i]))
    for i in order:
        x, y = T(pts[i])
        lines = texts[i].split('\n')
        w = max(len(s) for s in lines) * fontsize * 0.545
        h = fontsize * 1.28 * len(lines)
        r = radii[i] + 7
        cands = [( x+r,        y-h/2,   'left'),   ( x-r-w,      y-h/2,   'left'),
                 ( x-w/2,      y+r,     'left'),   ( x-w/2,      y-r-h,   'left'),
                 ( x+r*0.75,   y+r*0.6, 'left'),   ( x-r*0.75-w, y+r*0.6, 'left'),
                 ( x+r*0.75,   y-r*0.6-h,'left'),  ( x-r*0.75-w, y-r*0.6-h,'left')]
        chosen, ok = cands[0], False
        for c in cands:
            b = (c[0]-pad, c[1]-pad, c[0]+w+pad, c[1]+h+pad)
            if not hit(b):
                chosen, ok = c, True; break
        boxes.append((chosen[0]-pad, chosen[1]-pad, chosen[0]+w+pad, chosen[1]+h+pad))
        ax.annotate(texts[i], xy=(chosen[0], chosen[1]), xycoords='figure pixels',
                    fontsize=fontsize, color=colors[i], linespacing=1.25,
                    fontweight=600 if bold[i] else 400, ha='left', va='bottom',
                    annotation_clip=False, zorder=6)
        if chosen is not cands[0]:
            cx, cy = chosen[0]+w/2, chosen[1]+h/2
            dx, dy = cx-x, cy-y
            L = max((dx*dx+dy*dy) ** .5, 1)
            sx, sy = x + dx/L*radii[i], y + dy/L*radii[i]
            ex, ey = cx - dx/L*(w/2+3), cy - dy/L*(h/2+3)
            fig.add_artist(plt.Line2D([sx, ex], [sy, ey], transform=None,
                                      color=LINE_STR, lw=0.9, zorder=1))

def _w(z, b):  return 700 if (z, b) in (REC, HYP, SLEEVE) else 400

# ---------------------------------------------------------------- 1. market
def market(ms, path):
    fig, ax = plt.subplots(figsize=(11.4, 5.4))
    ms = ms[ms.net_yield.notna()].copy()
    pts, txt, cols, bold, rad = [], [], [], [], []
    for _, r in ms.iterrows():
        c = _c(r.micro_zone, r.bed_bucket)
        ax.scatter(r.net_yield*100, r.value/1e6, s=max(60, r.n/2.2), color=c,
                   alpha=.30, edgecolors=c, linewidths=2, zorder=3)
        pts.append((r.net_yield*100, r.value/1e6))
        txt.append(_two_line(r.micro_zone, r.bed_bucket))
        rad.append(max(60, r.n/2.2) ** .5 / 2)
        cols.append(INK if c != NEUTRAL else INK_2); bold.append(c != NEUTRAL)
    ax.set_yscale('log')
    ax.set_ylim(ms.value.min()/1e6*0.55, ms.value.max()/1e6*2.6)
    ax.set_xlabel('Retorno líquido de caixa ao ano')
    ax.set_ylabel('Capital anunciado no segmento (R$ milhões, escala log)')
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f'{v:.0f}%'.replace('.', ',')))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f'{v:,.0f}'.replace(',', '.')))
    ax.grid(axis='both')
    ax.set_xlim(2.6, 9.0)
    ax.axvspan(2.6, 4.5, color=BAD, alpha=.045, zorder=0)
    share = ms[ms.net_yield < 0.045].value.sum()/ms.value.sum()
    ax.text(2.68, ms.value.min()/1e6*0.62,
            f'{share*100:.0f}% do capital anunciado da cidade está\nnesta faixa — a de pior retorno',
            fontsize=10.4, color=BAD, va='bottom', ha='left', fontweight=600)
    place_labels(ax, pts, txt, cols, bold, rad)
    ds.footnote(fig, 'Cada bolha é um segmento (zona × dormitórios) com pelo menos 15 unidades prontas à venda; '
                     'o tamanho é o número de unidades. Retorno líquido sob operação Seazone, premissas base.')
    return ds.save_svg(fig, path)

# ---------------------------------------------------------------- 2. seasonality
def seasonality(week, path):
    fig, ax = plt.subplots(figsize=(7.6, 4.3))
    x = np.arange(len(week)); y = [w[1] for w in week]
    ax.fill_between(x, 0, y, color=S1, alpha=.10, zorder=2)
    ax.plot(x, y, color=S1, lw=2.4, zorder=3)
    ax.scatter(x, y, s=26, color=S1, edgecolors='white', linewidths=1.4, zorder=4)
    ax.set_xticks(x[::3]); ax.set_xticklabels([week[i][0] for i in range(0, len(week), 3)])
    ax.set_ylim(0, max(y)*1.22)
    ax.set_ylabel('Receita por noite disponível (R$)')
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f'{v:,.0f}'.replace(',', '.')))
    lo = int(np.argmin(y))
    ax.annotate(f'R$ {y[1]:.0f}\npico de janeiro', (1, y[1]), xytext=(1.6, max(y)*1.13),
                fontsize=10.5, color=INK, fontweight=600,
                arrowprops=dict(arrowstyle='-', color=INK_3, lw=1))
    ax.annotate(f'R$ {y[lo]:.0f}\nfim de março', (lo, y[lo]), xytext=(lo-3.4, y[lo]*0.42),
                fontsize=10.5, color=INK, fontweight=600,
                arrowprops=dict(arrowstyle='-', color=INK_3, lw=1))
    drop = 1 - y[lo]/max(y); wks = lo - int(np.argmax(y))
    ax.text(len(x)-0.3, max(y)*1.16, f'queda de {drop*100:.0f}%\nem {wks} semanas', fontsize=10.2,
            color=S2, ha='right', fontweight=600)
    ds.footnote(fig, 'Ocupação × diária, semana a semana, para os 1.005 anúncios com calendário. '
                     'Base observada: 06/jan a 20/abr/2025 — os outros oito meses são premissa declarada.')
    return ds.save_svg(fig, path)

# ---------------------------------------------------------------- 3. booking curve
def booking_curve(curve, path):
    fig, ax = plt.subplots(figsize=(7.6, 4.3))
    c = curve[curve.index <= 90]
    ax.plot(c.index, c.values, color=ACCENT, lw=2.4, zorder=3)
    ax.axvline(3, color=S2, lw=1.6, ls='--', zorder=2)
    ax.set_xlabel('Dias de antecedência em relação à estadia')
    ax.set_ylabel('Disponibilidade aparente (log-odds)')
    ax.invert_xaxis()
    ax.annotate('projetamos todos os anúncios\npara 3 dias de antecedência',
                (3, c.loc[3]), xytext=(26, c.loc[3]-1.15), fontsize=10.4, color=S2, fontweight=600,
                arrowprops=dict(arrowstyle='-', color=S2, lw=1))
    ax.annotate('abaixo de 3 dias a queda é o corte\nde reserva da plataforma, não demanda',
                (0.6, c.loc[0]), xytext=(20, c.loc[0]+0.15), fontsize=9.8, color=INK_2,
                arrowprops=dict(arrowstyle='-', color=INK_3, lw=1))
    ax.text(88, c.max()*0.96, 'a 90 dias, quase tudo\nainda parece disponível',
            fontsize=10.2, color=INK_2, va='top')
    ds.footnote(fig, 'Três capturas do calendário (06, 07 e 20/jan/2025) enxergam a mesma data de estadia em '
                     'horizontes diferentes, o que identifica a curva. 209.846 noites-anúncio.')
    return ds.save_svg(fig, path)

# ---------------------------------------------------------------- 4. price per m2
def ppsm(cap, path):
    fig, ax = plt.subplots(figsize=(11.4, 4.9))
    c = cap.sort_values('ppsm', ascending=True).copy()
    labels = [seg_label(z, b) for z, b in zip(c.zone, c.bed)]
    colors = [_c(z, b) for z, b in zip(c.zone, c.bed)]
    y = np.arange(len(c))
    ax.barh(y, c.ppsm, color=colors, height=.62, zorder=3)
    ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=10.6)
    for i, (v, col) in enumerate(zip(c.ppsm, colors)):
        ax.text(v+230, i, f'R$ {v:,.0f}'.replace(',', '.'), va='center', fontsize=10.4,
                color=INK, fontweight=600 if col != NEUTRAL else 400)
    ax.set_xlim(0, c.ppsm.max()*1.16)
    ax.set_xlabel('Preço pedido por m² (R$)')
    ax.grid(axis='x'); ax.grid(axis='y', visible=False)
    ax.set_xticks([0, 5000, 10000, 15000, 20000])
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f'{v/1000:.0f} mil'))
    hyp_i = [i for i, (z, b) in enumerate(zip(c.zone, c.bed)) if (z, b) == HYP]
    if hyp_i:
        ax.annotate('o m² mais caro da cidade é\njustamente o de 1 dormitório',
                    (c.ppsm.iloc[hyp_i[0]]*0.62, hyp_i[0]), xytext=(c.ppsm.max()*0.80, hyp_i[0]-3.4),
                    fontsize=10.8, color=S2, fontweight=600, ha='center', va='center',
                    arrowprops=dict(arrowstyle='-', color=S2, lw=1.1,
                                    connectionstyle='arc3,rad=0.24'))
    ds.footnote(fig, 'Mediana do preço pedido por m² entre as unidades prontas à venda em cada segmento (VivaReal, jan/2025).')
    return ds.save_svg(fig, path)

# ---------------------------------------------------------------- 5. frontier
def frontier(cap, path):
    fig, ax = plt.subplots(figsize=(11.4, 5.6))
    for g in [0.06, 0.09, 0.12, 0.15]:
        xs = np.array([9000, 19500]); ys = xs*g
        ax.plot(xs, ys, color=LINE_STR, lw=1, ls=(0, (3, 4)), zorder=1)
        xi = min(19500, 2150/g)
        ax.text(xi, min(2150, 19500*g)+22, f'{g*100:.0f}% bruto', fontsize=9.6, color=INK_3, ha='right')
    pts, txt, cols, bold, rad = [], [], [], [], []
    for _, r in cap.iterrows():
        col = _c(r.zone, r.bed)
        ax.scatter(r.ppsm, r.rev_per_m2, s=max(70, r.n_sale/2.4), color=col, alpha=.30,
                   edgecolors=col, linewidths=2, zorder=3)
        pts.append((r.ppsm, r.rev_per_m2)); txt.append(_two_line(r.zone, r.bed))
        rad.append(max(70, r.n_sale/2.4) ** .5 / 2)
        cols.append(INK if col != NEUTRAL else INK_2); bold.append(col != NEUTRAL)
    ax.set_xlim(9000, 21200); ax.set_ylim(930, 2200)
    place_labels(ax, pts, txt, cols, bold, rad)
    ax.set_xlabel('Preço pedido por m² (R$)')
    ax.set_ylabel('Receita anual por m² (R$)')
    for a in (ax.xaxis, ax.yaxis):
        a.set_major_formatter(FuncFormatter(lambda v, _: f'{v:,.0f}'.replace(',', '.')))
    ds.footnote(fig, 'Receita sob operação profissional. As diagonais são retorno bruto constante: quanto mais alto '
                     'e mais à esquerda, mais reais de receita por real investido.')
    return ds.save_svg(fig, path)

# ---------------------------------------------------------------- 6. yields + CI
def yields(ci, path):
    fig, ax = plt.subplots(figsize=(11.4, 5.2))
    c = ci.sort_values('net_yield', ascending=True).copy()
    labels = [seg_label(z, b) for z, b in zip(c.zone, c.bed)]
    colors = [_c(z, b) for z, b in zip(c.zone, c.bed)]
    y = np.arange(len(c))
    ax.barh(y, c.net_yield*100, color=colors, height=.60, zorder=3)
    ax.hlines(y, c.lo*100, c.hi*100, color=INK_2, lw=1.6, zorder=4)
    for xx in (c.lo*100, c.hi*100):
        ax.vlines(xx, y-.16, y+.16, color=INK_2, lw=1.6, zorder=4)
    for i, (v, hi, col) in enumerate(zip(c.net_yield, c.hi, colors)):
        ax.text(hi*100+0.14, i, f'{v*100:.1f}%'.replace('.', ',') + f'   ·   {1/v:.0f} anos',
                va='center', fontsize=10.3, color=INK, fontweight=600 if col != NEUTRAL else 400)
    ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=10.6)
    ax.set_xlim(0, 11.4); ax.set_xlabel('Retorno líquido de caixa ao ano · e payback')
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f'{v:.0f}%'))
    ax.grid(axis='x'); ax.grid(axis='y', visible=False)
    ds.footnote(fig, 'Barras: retorno líquido sob premissas base. Traço: intervalo de confiança de 90% por bootstrap '
                     'sobre os anúncios de cada célula. Payback sem alavancagem e sem valorização.')
    return ds.save_svg(fig, path)

# ---------------------------------------------------------------- 7. cost bridge
def bridge(cb, path):
    fig, ax = plt.subplots(figsize=(11.4, 4.9))
    items = cb['items']; labels = [i[0] for i in items] + ['Resultado operacional']
    vals = [i[1] for i in items]
    run = 0; lefts = []; heights = []; colors = []
    for i, v in enumerate(vals):
        if i == 0:
            lefts.append(0); heights.append(v); colors.append(S1); run = v
        else:
            lefts.append(run+v); heights.append(-v); colors.append(NEUTRAL); run += v
    lefts.append(0); heights.append(run); colors.append(S3)
    x = np.arange(len(labels))
    ax.bar(x, heights, bottom=lefts, color=colors, width=.62, zorder=3)
    for i in range(len(labels)-1):
        top = lefts[i]+heights[i] if i == 0 else lefts[i]
        ax.plot([i+.31, i+1-.31], [top, top], color=LINE_STR, lw=1, ls=(0, (2, 3)), zorder=2)
    for i, (l, h) in enumerate(zip(lefts, heights)):
        v = vals[i] if i < len(vals) else run
        txt = f'{v:,.0f}'.replace(',', '.')
        ax.text(i, l+h+2600, ('+' if i == 0 else '') + txt if i == 0 else
                (txt if i == len(labels)-1 else f'−{abs(v):,.0f}'.replace(',', '.')),
                ha='center', fontsize=10.4, color=INK,
                fontweight=600 if i in (0, len(labels)-1) else 400)
    ax.set_xticks(x); ax.set_xticklabels([l.replace(' ', '\n', 1) for l in labels], fontsize=10)
    ax.set_ylabel('R$ por ano')
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f'{v:,.0f}'.replace(',', '.')))
    ax.grid(axis='y'); ax.grid(axis='x', visible=False)
    ax.set_ylim(0, cb['rev']*1.18)
    ax.text(len(labels)-1, run*0.5, f'{run/cb["rev"]*100:.0f}%\nda receita', ha='center',
            va='center', fontsize=11, color='white', fontweight=700)
    price_s = f'{cb["price"]:,.0f}'.replace(',', '.')
    capex_s = f'{cb["capex"]/1000:,.0f}'.replace(',', '.')
    gy = f'{cb["gross_yield"]*100:.1f}'.replace('.', ',')
    ny = f'{cb["net_yield"]*100:.1f}'.replace('.', ',')
    ds.footnote(fig, f'Unidade mediana do segmento recomendado: {seg_label(cb["zone"], cb["bed"])}, '
                     f'{cb["area"]:.0f} m², pedido de R$ {price_s}. '
                     f'Bruto {gy}% · líquido {ny}% sobre o custo total de R$ {capex_s} mil.')
    return ds.save_svg(fig, path)

# ---------------------------------------------------------------- 8. tornado
def tornado(base, tor, path):
    fig, ax = plt.subplots(figsize=(11.4, 4.4))
    y = np.arange(len(tor))
    ax.barh(y, (tor.high-tor.low)*100, left=tor.low*100, color=NEUTRAL, height=.55, zorder=3)
    ax.axvline(base*100, color=S1, lw=2, zorder=4)
    for i, r in enumerate(tor.itertuples()):
        ax.text(r.low*100-0.09, i, f'{r.low*100:.1f}'.replace('.', ','), ha='right', va='center',
                fontsize=10, color=INK_2)
        ax.text(r.high*100+0.09, i, f'{r.high*100:.1f}%'.replace('.', ','), ha='left', va='center',
                fontsize=10, color=INK_2)
    ax.set_yticks(y); ax.set_yticklabels(tor.label, fontsize=10.6)
    ax.set_xlabel('Retorno líquido de caixa ao ano')
    ax.set_xticks([5, 5.5, 6, 6.5, 7, 7.5, 8])
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f'{v:.1f}%'.replace('.', ',')))
    ax.grid(axis='x'); ax.grid(axis='y', visible=False)
    ax.set_xlim(4.6, 8.4)
    ax.text(base*100+0.06, len(tor)-0.35, f'caso base {base*100:.1f}%'.replace('.', ','),
            color=S1, fontsize=10.6, fontweight=600)
    ds.footnote(fig, 'Cada premissa movida sozinha até as pontas da faixa defensável, mantendo as demais no caso base. '
                     'Nenhuma isolada leva o segmento recomendado abaixo de 5,2%.')
    return ds.save_svg(fig, path)

# ---------------------------------------------------------------- 9. distance stress
def distance(dstress, ref, path):
    fig, ax = plt.subplots(figsize=(7.9, 4.4))
    for el, style, lab in [(-0.12, '-', 'elasticidade estimada (−0,12)'),
                           (-0.30, (0, (5, 3)), 'cenário pessimista (−0,30)')]:
        s = dstress[dstress.elast == el]
        ax.plot(s.mult, s.net_yield*100, color=S1, lw=2.3, ls=style, zorder=3, label=lab)
    ax.axhline(ref*100, color=S3, lw=2, zorder=2)
    ax.text(3.02, ref*100+0.13, f'Meia Praia · orla · 2 dorm  {ref*100:.1f}%'.replace('.', ','),
            fontsize=10.3, color=S3, ha='right', va='bottom', fontweight=600)
    ax.set_xlabel('Quanto mais longe do mar o estoque à venda pode estar\n(múltiplo da distância assumida)')
    ax.set_ylabel('Retorno líquido — Morretes 2 dorm')
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f'{v:.1f}×'.replace('.', ',')))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f'{v:.1f}%'.replace('.', ',')))
    ax.legend(fontsize=10, loc='upper right')
    ax.set_xlim(0.95, 3.05)
    cross = {}
    for el in (-0.12, -0.30):
        s = dstress[dstress.elast == el].sort_values('mult')
        xs, ys = s.mult.values, s.net_yield.values
        below = np.where(ys < ref)[0]
        cross[el] = float(np.interp(ref, ys[::-1], xs[::-1])) if len(below) else None
    xc = cross[-0.12] or 3.05
    ax.axvspan(cross[-0.30] or xc, 3.05, color=S2, alpha=.06, zorder=0)
    lo_c = cross[-0.30]
    msg = (f'entre {lo_c:.1f}× e {xc:.1f}× de distância a mais, a orla passa à frente'
           .replace('.', ',')) if lo_c else f'a partir de {xc:.1f}× a orla passa à frente'.replace('.', ',')
    ax.text((min(lo_c or xc, xc)+3.05)/2, ax.get_ylim()[0]+0.12, msg,
            fontsize=10.2, color=S2, ha='center', fontweight=600)
    ds.footnote(fig, 'O VivaReal não traz coordenadas: esta é a única incerteza capaz de inverter a ordem dos segmentos. '
                     'É exatamente por isso que a recomendação carrega uma parcela na orla.')
    return ds.save_svg(fig, path)

# ---------------------------------------------------------------- 10. portfolio
def portfolio(roll, path):
    fig, ax = plt.subplots(figsize=(11.4, 3.2))
    left = 0
    for _, r in roll.iterrows():
        col = S1 if r.label.startswith('Morretes') else (S3 if 'orla' in r.label else NEUTRAL)
        w = r.capital/1e6
        ax.barh([0], [w], left=[left], color=col, height=.50, zorder=3,
                edgecolor=ds.SURFACE, linewidth=2.5)
        cap_s = f'{w:.1f}'.replace('.', ',')
        yld_s = f'{r.yld*100:.1f}'.replace('.', ',')
        txt = f'{r.label}\n{r.units} un · R$ {cap_s} mi · {yld_s}%'
        if w > 2.6:
            ax.text(left+w/2, 0, txt, ha='center', va='center', fontsize=10,
                    color='white', fontweight=600, zorder=4)
        else:
            ax.annotate(txt, xy=(left+w/2, -.25), xytext=(left+w/2, -.62),
                        ha='center', va='top', fontsize=9.6, color=INK_2,
                        arrowprops=dict(arrowstyle='-', color=LINE_STR, lw=1))
        left += w
    ax.set_xlim(0, left*1.004); ax.set_ylim(-1.15, .45)
    ax.set_yticks([]); ax.grid(False)
    ax.set_xlabel('Capital alocado (R$ milhões)')
    ax.set_xticks([0, 5, 10, 15, 20])
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f'{v:.0f}'))
    ax.spines['bottom'].set_color(LINE)
    ds.footnote(fig, 'Alocação gulosa sobre os anúncios reais da base, com teto de 45% por segmento e 30% por '
                     'corretor, após descarte de outliers de preço e deságio de qualidade.')
    return ds.save_svg(fig, path)
