"""Deck data layer: reads what the platform already computed and derives only the few
series the meeting needs that no earlier step produced (cost bridge, one-at-a-time
sensitivity, market structure, portfolio roll-up). Nothing here re-runs the analysis."""
import json, numpy as np, pandas as pd
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / 'output'

ZONE_PT = {
    'Meia Praia (beach band)': 'Meia Praia · orla',
    'Meia Praia (inland)':     'Meia Praia · interior',
    'Morretes':                'Morretes',
    'Tabuleiro dos Oliveiras': 'Tabuleiro dos Oliveiras',
    'Centro':                  'Centro',
    'Casa Branca':             'Casa Branca',
    'Jardim Praia Mar':        'Jardim Praia Mar',
    'Canto da Praia':          'Canto da Praia',
}
def zpt(z): return ZONE_PT.get(z, z)
def seg_label(z, b): return f'{zpt(z)} · {int(b)} dorm'

def load():
    d = {}
    d['P']        = json.load(open(OUT/'assumptions.json'))
    d['curve']    = json.load(open(OUT/'booking_curve.json'))
    d['cap']      = pd.read_csv(OUT/'capacity_density.csv')
    d['cases']    = pd.read_csv(OUT/'investment_cases.csv')
    d['pf']       = pd.read_csv(OUT/'portfolio_20m.csv')
    d['listing']  = pd.read_csv(OUT/'listing_modelfeatures.csv')
    d['sale']     = pd.read_csv(OUT/'sale_scored.csv', low_memory=False)
    ci = pd.read_csv(OUT/'segment_yields_ci.csv')
    ci.columns = ['zone','bed'] + list(ci.columns[2:])
    d['ci']       = ci
    d['segm']     = pd.read_csv(OUT/'segments_micro_zone.csv')
    return d

# ---------------------------------------------------------------- market structure
def market_structure(d):
    s = d['sale']; s = s[s.is_offplan == 0]
    g = (s.groupby(['micro_zone','bed_bucket'])
           .agg(n=('sale_price','size'), value=('sale_price','sum'),
                price=('sale_price','median'), area=('usable_area','median'),
                ppsm=('ppsm','median'))
           .reset_index())
    g = g[g.n >= 15].copy()
    g['label'] = [seg_label(z,b) for z,b in zip(g.micro_zone, g.bed_bucket)]
    ab = (d['listing'].groupby(['micro_zone','bed_bucket']).size()
            .rename('n_airbnb').reset_index())
    g = g.merge(ab, on=['micro_zone','bed_bucket'], how='left').fillna({'n_airbnb':0})
    g['net_yield'] = [None if r.n_airbnb < 8 else
                      _yield_with(d, r.micro_zone, int(r.bed_bucket), d['P'])
                      for r in g.itertuples()]
    g['size_class'] = np.where(g.bed_bucket <= 2, 'compacto (até 2 dorm)', 'grande (3+ dorm)')
    return g.sort_values('value', ascending=False)

# ---------------------------------------------------------------- cost bridge
def cost_bridge(d, zone, bed):
    P = d['P']; s = d['sale']; l = d['listing']
    sl = s[(s.micro_zone==zone) & (s.bed_bucket==bed) & (s.is_offplan==0)]
    ab = l[(l.micro_zone==zone) & (l.bed_bucket==bed)]
    rev   = sl.rev_pred.median()
    price = sl.sale_price.median()*(1-P['negotiation_disc'])
    area  = sl.usable_area.median()
    capex = price*(1+P['closing_costs']) + area*P['furnish_per_m2']
    condo = (sl.monthly_condo_fee.median() if np.isfinite(sl.monthly_condo_fee.median()) else 450)*12
    iptu  = price*P['iptu_pct_fallback']
    occ   = ab.occ.median()*P['booked_share']
    items = [('Receita de reservas',        rev),
             ('Taxa de administração 20%', -rev*P['mgmt_fee']),
             ('Condomínio',                -condo),
             ('IPTU',                      -iptu),
             ('Consumo por noite ocupada', -occ*365*P['util_per_night']),
             ('Custos fixos',              -12*P['fixed_monthly']),
             ('Reserva de manutenção',     -price*P['maint_pct_value'])]
    noi = rev + sum(v for _,v in items[1:])
    return dict(zone=zone, bed=bed, items=items, noi=noi, capex=capex, rev=rev,
                price=sl.sale_price.median(), area=area, occ=occ,
                adr=ab.adr.median(), n_sale=len(sl), n_ab=len(ab),
                gross_yield=rev/capex, net_yield=noi/capex, payback=capex/noi)

# ---------------------------------------------------------------- sensitivity
SWEEP = {   # parameter -> (low, high, human label)
    'booked_share':     (0.80, 1.00, 'Noites indisponíveis que são reservas pagas'),
    'host_take':        (0.85, 1.00, 'Fatia da diária que fica com o anfitrião'),
    'season_low_mult':  (0.35, 0.65, 'Baixa temporada (mai–set) vs abril'),
    'mgmt_fee':         (0.25, 0.15, 'Taxa de administração'),
    'negotiation_disc': (0.00, 0.12, 'Desconto de negociação'),
    'furnish_per_m2':   (1800, 800,  'Mobília e enxoval por m²'),
    'util_per_night':   (65,   30,   'Consumo por noite ocupada'),
}
def _yield_with(d, zone, bed, P):
    s = d['sale']; l = d['listing']
    sl = s[(s.micro_zone==zone)&(s.bed_bucket==bed)&(s.is_offplan==0)]
    ab = l[(l.micro_zone==zone)&(l.bed_bucket==bed)]
    base = d['P']
    scale = (P['booked_share']/base['booked_share'])*(P['host_take']/base['host_take'])
    scale *= (0.60 + 0.40*P['season_low_mult']/base['season_low_mult'])
    rev = sl.rev_pred.median()*scale
    price = sl.sale_price.median()*(1-P['negotiation_disc']); area = sl.usable_area.median()
    capex = price*(1+P['closing_costs']) + area*P['furnish_per_m2']
    condo = (sl.monthly_condo_fee.median() if np.isfinite(sl.monthly_condo_fee.median()) else 450)*12
    occ = ab.occ.median()*P['booked_share']
    opex = (rev*P['mgmt_fee'] + condo + price*P['iptu_pct_fallback']
            + occ*365*P['util_per_night'] + 12*P['fixed_monthly'] + price*P['maint_pct_value'])
    return (rev-opex)/capex

def tornado(d, zone, bed):
    base = _yield_with(d, zone, bed, d['P'])
    rows = []
    for k,(lo,hi,label) in SWEEP.items():
        a = _yield_with(d, zone, bed, {**d['P'], k: lo})
        b = _yield_with(d, zone, bed, {**d['P'], k: hi})
        rows.append(dict(param=k, label=label, low=min(a,b), high=max(a,b),
                         span=abs(b-a), lo_val=lo, hi_val=hi))
    return base, pd.DataFrame(rows).sort_values('span', ascending=True)

def distance_stress(d, zone, bed, alt_zone, alt_bed):
    """Yield of an off-beach segment if its sale stock is X times further from the sea."""
    out=[]
    for mult in [1.0, 1.5, 2.0, 2.5, 3.0]:
        for el in [-0.12, -0.30]:
            s=d['sale']; l=d['listing']; P=d['P']
            sl=s[(s.micro_zone==zone)&(s.bed_bucket==bed)&(s.is_offplan==0)]
            ab=l[(l.micro_zone==zone)&(l.bed_bucket==bed)]
            rev=sl.rev_pred.median()*(mult**el)
            price=sl.sale_price.median()*(1-P['negotiation_disc']); area=sl.usable_area.median()
            capex=price*(1+P['closing_costs'])+area*P['furnish_per_m2']
            condo=(sl.monthly_condo_fee.median() if np.isfinite(sl.monthly_condo_fee.median()) else 450)*12
            occ=ab.occ.median()*P['booked_share']
            opex=(rev*P['mgmt_fee']+condo+price*P['iptu_pct_fallback']+occ*365*P['util_per_night']
                  +12*P['fixed_monthly']+price*P['maint_pct_value'])
            out.append(dict(mult=mult, elast=el, net_yield=(rev-opex)/capex))
    ref = _yield_with(d, alt_zone, alt_bed, d['P'])
    return pd.DataFrame(out), ref

# ---------------------------------------------------------------- demand series
def demand_series(d):
    l = d['listing']
    wk = pd.read_csv(OUT/'listing_demand.csv')  # listing-level, for distributions
    curve = pd.Series({int(k): v for k, v in d['curve']['h_lead'].items()}).sort_index()
    return curve, l

def portfolio(d):
    pf = d['pf'].copy()
    pf['label'] = [seg_label(z,b) for z,b in zip(pf.micro_zone, pf.bed_bucket)]
    roll = (pf.groupby('label').agg(units=('capex','size'), capital=('capex','sum'),
                                    noi=('noi_adj','sum')).reset_index())
    roll['yld'] = roll.noi/roll.capital
    return pf, roll.sort_values('capital', ascending=False)
