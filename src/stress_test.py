"""Stress tests for the recommendation.

Probes whether the recommended compact-2BR-in-Morretes core and the
off-beach thesis survive: excluding the cheap price tail, dropping the
thin Morretes-3BR cell, conservative / realistic assumption sets, and the
market-revenue (non-operator) view. Output is printed and mirrored to
output/logs/log_stress.txt. This script reads outputs only; it does not
retrain models.
"""
import json
import numpy as np
import pandas as pd
import _paths
RAW, OUT = _paths.setup()
_paths.tee('log_stress.txt')
P = json.load(open(OUT / 'assumptions.json'))
l = pd.read_csv(OUT / 'listing_modelfeatures.csv')
s = pd.read_csv(OUT / 'sale_scored.csv', low_memory=False)

SEGS = [('Morretes', 3), ('Morretes', 2), ('Tabuleiro dos Oliveiras', 2),
        ('Meia Praia (beach band)', 2), ('Meia Praia (inland)', 2),
        ('Centro', 1), ('Centro', 2), ('Meia Praia (beach band)', 3),
        ('Meia Praia (inland)', 3), ('Centro', 3), ('Meia Praia (beach band)', 4)]


def seg_yield(p, price_floor=None, price_cap=None, rev_scale=1.0, use_prof=True):
    out = {}
    for z, b in SEGS:
        sl = s[(s.micro_zone == z) & (s.bed_bucket == b) & (s.is_offplan == 0)].copy()
        if price_floor:
            sl = sl[sl.sale_price >= price_floor]
        if price_cap:
            sl = sl[sl.sale_price <= price_cap]
        ab = l[(l.micro_zone == z) & (l.bed_bucket == b)]
        if len(ab) < 8 or len(sl) < 15:
            continue
        rev = (sl.rev_pred.median() if use_prof else ab.rev_annual_gross.median()) * rev_scale
        price = sl.sale_price.median() * (1 - p['negotiation_disc'])
        area = sl.usable_area.median()
        capex = price * (1 + p['closing_costs']) + area * p['furnish_per_m2']
        condo = (sl.monthly_condo_fee.median() if np.isfinite(sl.monthly_condo_fee.median()) else 450) * 12
        iptu = price * p['iptu_pct_fallback']
        occ = ab.occ.median() * p['booked_share']
        opex = (rev * p['mgmt_fee'] + condo + iptu + occ * 365 * p['util_per_night']
                + 12 * p['fixed_monthly'] + price * p['maint_pct_value'])
        out[(z, b)] = (rev - opex) / capex
    return pd.Series(out)


def fmt(ser, k=5):
    return ', '.join(f'{z[:13]} {b}BR {v:.3f}' for (z, b), v in ser.sort_values(ascending=False).head(k).items())


print('=' * 70)
print('BASE')
base = seg_yield(P)
print(fmt(base))

print('\n[1] cheap tail excluded (asking >= R$550k, ~segment median for Morretes 2BR)')
y = seg_yield(P, price_floor=550_000)
print(fmt(y))

print('\n[2] strict target band only (R$600k–R$900k asking)')
y = seg_yield(P, price_floor=600_000, price_cap=900_000)
print(fmt(y))

print('\n[3] Morretes 3BR dropped (10 comparables — thin evidence)')
segs3 = [seg for seg in SEGS if seg != ('Morretes', 3)]
globals()['SEGS'] = segs3
y = seg_yield(P)
print(fmt(y))
globals()['SEGS'] = SEGS

print('\n[4] realistic-revenue view (median EXISTING host, not professional operator)')
y = seg_yield(P, use_prof=False)
print(fmt(y))

print('\n[5] conservative assumptions (pessimistic corners)')
Pc = dict(P)
Pc.update(booked_share=0.80, host_take=0.85, season_low_mult=0.35,
          furnish_per_m2=1800, mgmt_fee=0.25, negotiation_disc=0.0,
          util_per_night=65)
scale = (Pc['booked_share']/P['booked_share']) * (Pc['host_take']/P['host_take'])
scale *= (0.60 + 0.40*Pc['season_low_mult']/P['season_low_mult'])
y = seg_yield(Pc, rev_scale=scale)
print(fmt(y))

print('\n[6] optimistic-but-realistic assumptions')
Po = dict(P)
Po.update(booked_share=0.95, host_take=0.92, season_low_mult=0.60,
          furnish_per_m2=1000, mgmt_fee=0.18, negotiation_disc=0.10)
scale = (Po['booked_share']/P['booked_share']) * (Po['host_take']/P['host_take'])
scale *= (0.60 + 0.40*Po['season_low_mult']/P['season_low_mult'])
y = seg_yield(Po, rev_scale=scale)
print(fmt(y))

print('\n[7] revenue inflated +30% (revenue upside) — does any large/orla cell jump ahead?')
y = seg_yield(P) * 1.0
y2 = seg_yield(P, rev_scale=1.30)
print('   with +30% revenue on ALL cells:')
print(fmt(y2))

print('\n[8] revenue DOWN -25% (broad demand miss) — does the ranking survive?')
print(fmt(seg_yield(P, rev_scale=0.75)))

print('\n[9] recompute investment cases with market-revenue (honesty view)')
cases = pd.read_csv(OUT / 'investment_cases.csv')
print(cases[['case', 'net_yield', 'payback']].round(4).to_string(index=False))
print('\nNote: professional-operator yields are the deck headline; market '
      '(median host) yields are shown separately in the docs.')