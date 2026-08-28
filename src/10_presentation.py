"""10 - Presentation layer.

Turns the analysis already produced by steps 01-09 into an executive deck for an
investment meeting. Reads only from output/; recomputes nothing. Run it again
after any change upstream and the deck rebuilds itself, numbers and all.

    python src/10_presentation.py            # charts + deck
    python src/10_presentation.py --charts   # charts only
    python src/10_presentation.py --png      # also emit PNG copies of every chart

Revise copy without touching code by creating presentation/overrides.json, e.g.
    {"slides": {"0": {"headline": "Nova manchete"}}}
"""
import sys, json, os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import pandas as pd, numpy as np
import deck_style as ds; ds.apply()
import deck_data as D, deck_charts as C, deck_spec, deck_render

ROOT = Path(__file__).resolve().parent.parent
CH = ROOT/'output'/'charts'; CH.mkdir(parents=True, exist_ok=True)
(ROOT/'docs').mkdir(exist_ok=True)
PNG = '--png' in sys.argv

REC, HYP, SLEEVE = ('Morretes', 2), ('Centro', 1), ('Meia Praia (beach band)', 2)
WEEK = [("6 jan",691.6),("13 jan",711.3),("20 jan",665.5),("27 jan",567.5),("3 fev",563.4),
        ("10 fev",519.2),("17 fev",488.2),("24 fev",512.1),("3 mar",483.6),("10 mar",396.5),
        ("17 mar",375.1),("24 mar",324.9),("31 mar",318.6),("7 abr",338.8),("14 abr",413.5)]

if PNG:
    _orig = ds.save_svg
    def _dual(fig, path):
        fig.savefig(str(path).replace('.svg', '.png'), format='png', dpi=140, facecolor=ds.SURFACE)
        return _orig(fig, path)
    ds.save_svg = _dual; C.ds.save_svg = _dual

def main():
    d = D.load()
    R = dict(rec=REC, hyp=HYP, sleeve=SLEEVE)
    R['market']  = D.market_structure(d)
    R['bridge']  = D.cost_bridge(d, *REC)
    R['tornado'] = D.tornado(d, *REC)
    R['dstress'], R['ref'] = D.distance_stress(d, *REC, *SLEEVE)
    R['pf'], R['roll'] = D.portfolio(d)
    curve = pd.Series({int(k): v for k, v in d['curve']['h_lead'].items()}).sort_index()

    # ---- chart catalogue: each entry declares when it is worth showing -----
    base_t, tor = R['tornado']
    catalogue = [
        ('c1_market',    lambda p: C.market(R['market'], p),           lambda: len(R['market']) >= 6),
        ('c2_season',    lambda p: C.seasonality(WEEK, p),             lambda: len(WEEK) >= 8),
        ('c3_curve',     lambda p: C.booking_curve(curve, p),          lambda: curve.max()-curve.min() > 1.0),
        ('c4_ppsm',      lambda p: C.ppsm(d['cap'], p),                lambda: True),
        ('c5_frontier',  lambda p: C.frontier(d['cap'], p),            lambda: True),
        ('c6_yields',    lambda p: C.yields(d['ci'], p),               lambda: len(d['ci']) >= 5),
        ('c7_bridge',    lambda p: C.bridge(R['bridge'], p),           lambda: True),
        ('c8_tornado',   lambda p: C.tornado(base_t, tor, p),          lambda: tor.span.max() > 0.005),
        ('c9_distance',  lambda p: C.distance(R['dstress'], R['ref'], p),
                                                                       lambda: REC[0] not in ('Meia Praia (beach band)',)),
        ('c10_portfolio',lambda p: C.portfolio(R['roll'], p),          lambda: len(R['roll']) >= 2),
    ]
    built = []
    for name, fn, rule in catalogue:
        if not rule():
            print(f'  skip  {name}  (não relevante para estes resultados)'); continue
        fn(CH/f'{name}.svg'); built.append(name)
        print(f'  ok    {name}')

    spec = deck_spec.build(d, R)
    # drop any chart reference the catalogue decided not to build
    for s in spec['slides']:
        if s.get('chart') and s['chart'] not in built: s.pop('chart', None)
        if s.get('secondary') and s['secondary'] not in built: s.pop('secondary', None)
        if s.get('charts'): s['charts'] = [c for c in s['charts'] if c in built]
    spec['slides'] = [s for s in spec['slides']
                      if s.get('layout') in ('kpi', 'profile', 'segments', 'matrix') or s.get('chart')
                      or s.get('charts') or s.get('steps')]
    json.dump(spec, open(ROOT/'output'/'deck_spec.json', 'w'), ensure_ascii=False, indent=1, default=str)
    html = deck_render.render(spec)
    (ROOT/'docs'/'apresentacao.html').write_text(html)
    print(f'\n{len(spec["slides"])} lâminas · {len(built)} gráficos · '
          f'{len(html)/1024:.0f} KB → docs/apresentacao.html')
    print('output/deck_spec.json guardado — edite presentation/overrides.json para revisar textos.')

if __name__ == '__main__':
    main()
