"""Shared presentation style: the platform's existing design tokens, applied to matplotlib.

Charts are rendered to SVG with `svg.fonttype='none'`, so text stays as real text and the
deck's webfont renders it. That keeps chart type and slide type in one visual system and
makes every label selectable and crisp at any projector resolution.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rcParams
import io, re

# --- tokens lifted from docs/recomendacao.html (the platform's design system) ---
INK       = '#101816'
INK_2     = '#535d59'
INK_3     = '#7c8681'
LINE      = '#dae0db'
LINE_STR  = '#b9c3bd'
SURFACE   = '#fbfcfa'
SURF_2    = '#eef2ef'
ACCENT    = '#0d5b66'
S1        = '#2a78d6'   # recommended / primary series
S2        = '#eb6834'   # the hypothesis / warning series
S3        = '#1baf7a'   # positive third series
NEUTRAL   = '#9aa5a0'   # everything else
BAD       = '#c0392b'

FONT = 'IBM Plex Sans, Carlito, Liberation Sans, DejaVu Sans, sans-serif'

def apply():
    rcParams.update({
        'svg.fonttype': 'none',
        'text.parse_math': False,
        'font.family': 'sans-serif',
        'font.sans-serif': ['Carlito', 'Liberation Sans', 'DejaVu Sans'],
        'font.size': 11.5,
        'axes.facecolor': 'none', 'figure.facecolor': 'none', 'savefig.facecolor': 'none',
        'axes.edgecolor': LINE, 'axes.labelcolor': INK_2, 'axes.titlecolor': INK,
        'axes.grid': True, 'grid.color': LINE, 'grid.linewidth': 0.9, 'grid.alpha': 1,
        'axes.spines.top': False, 'axes.spines.right': False,
        'axes.spines.left': False, 'axes.spines.bottom': True,
        'xtick.color': INK_3, 'ytick.color': INK_3,
        'xtick.labelcolor': INK_2, 'ytick.labelcolor': INK_2,
        'xtick.major.size': 0, 'ytick.major.size': 0,
        'legend.frameon': False, 'legend.labelcolor': INK_2,
        'figure.dpi': 110, 'savefig.bbox': 'tight', 'savefig.pad_inches': 0.06,
    })

def brl(v, short=True):
    if v is None: return '—'
    a = abs(v)
    if short and a >= 1e6:  return f'R$ {v/1e6:,.2f} mi'.replace(',', 'X').replace('.', ',').replace('X', '.')
    if short and a >= 1e3:  return f'R$ {v/1e3:,.0f} mil'.replace(',', '.')
    return f'R$ {v:,.0f}'.replace(',', '.')

def num(v, d=0):
    s = f'{v:,.{d}f}'
    return s.replace(',', 'X').replace('.', ',').replace('X', '.')

def pct(v, d=1):
    return f'{v*100:.{d}f}%'.replace('.', ',')

def save_svg(fig, path):
    buf = io.StringIO()
    fig.savefig(buf, format='svg')
    plt.close(fig)
    svg = buf.getvalue()
    svg = svg[svg.index('<svg'):]
    # let the deck's webfont and CSS take over the type
    svg = svg.replace('font-family: Carlito', f'font-family: {FONT}')
    svg = re.sub(r'font-family:\s*(Carlito|Liberation Sans|DejaVu Sans)[^;"]*', f'font-family: {FONT}', svg)
    svg = svg.replace('<svg ', '<svg class="chart" preserveAspectRatio="xMidYMid meet" ', 1)
    svg = re.sub(r'width="[\d.]+pt" height="[\d.]+pt"', '', svg, count=1)
    with open(path, 'w') as f: f.write(svg)
    return path

def annotate(ax, text, xy, xytext, color=None, arrow=True, size=10.5, **kw):
    ax.annotate(text, xy=xy, xytext=xytext, color=color or INK, fontsize=size,
                arrowprops=dict(arrowstyle='-', color=color or INK_3, lw=1,
                                connectionstyle='arc3,rad=0.12') if arrow else None,
                **kw)

def footnote(fig, text):
    fig.text(0.0, -0.03, text, fontsize=9.5, color=INK_3, ha='left', va='top')


def save_png(fig, path):
    fig.savefig(path, format='png', dpi=125, facecolor='#fbfcfa')
    return path
