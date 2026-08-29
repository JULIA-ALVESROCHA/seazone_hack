"""11 - Demand-side layer: who the guest actually is.

We never observe guests. We observe (a) how each unit is *configured* — capacity,
beds per bedroom, bathrooms, amenities, house rules, ad copy — and (b) the demand
that configuration achieves — occupancy, rate, weekend premium, seasonal
concentration. Segments are therefore revealed preference, not personas: the
configuration is the hypothesis and the demand pattern is the test.

Everything printed here is tagged:
  [DADO]      measured directly in the base
  [INFERIDO]  derived from measured signals with a stated rule
  [HIPÓTESE]  strategic reading that the base cannot confirm
"""
import numpy as np, pandas as pd, json, re
from pathlib import Path
import _paths
RAW, OUT = _paths.setup()
_paths.tee('log_11_guest_segments.txt')
pd.set_option('display.width', 220)

# ------------------------------------------------------------------ 1. demand pattern
def weekend_and_season():
    """Weekend premium and seasonal concentration, straight from the scraped calendar.
    Lead time is held constant (1-13 nights out) so weekday/weekend availability is
    compared like with like without needing the booking-curve model."""
    p = pd.read_csv(RAW/'Price_AV_Itapema.csv', low_memory=False)
    p['date'] = pd.to_datetime(p.date); p['cap'] = pd.to_datetime(p.aquisition_date).dt.normalize()
    p['lead'] = (p.date - p.cap).dt.days
    p['dow']  = p.date.dt.dayofweek
    p['wknd'] = p.dow.isin([4, 5])                     # Friday + Saturday nights

    # --- price side: every observed night, no lead restriction needed
    pr = (p.groupby(['airbnb_listing_id', 'wknd']).price.median().unstack())
    pr.columns = ['price_wd', 'price_we']
    pr['weekend_price_premium'] = pr.price_we/pr.price_wd - 1

    # --- availability side: fixed short-lead window, listings present in that capture
    near = p[p.lead.between(1, 13)]
    frames = []
    for cap, g in near.groupby('cap'):
        ids = np.sort(p[p.cap == cap].airbnb_listing_id.unique())
        dates = pd.date_range(cap + pd.Timedelta(days=1), cap + pd.Timedelta(days=13))
        idx = pd.MultiIndex.from_product([ids, dates], names=['airbnb_listing_id', 'date'])
        f = pd.DataFrame(index=idx).reset_index()
        f['avail'] = f.set_index(['airbnb_listing_id', 'date']).index.isin(
            g.set_index(['airbnb_listing_id', 'date']).index).astype(int)
        frames.append(f)
    n = pd.concat(frames, ignore_index=True)
    n['wknd'] = n.date.dt.dayofweek.isin([4, 5])
    occ = 1 - n.groupby(['airbnb_listing_id', 'wknd']).avail.mean().unstack()
    occ.columns = ['occ_wd', 'occ_we']
    occ['weekend_occ_lift'] = occ.occ_we - occ.occ_wd

    # --- seasonal concentration: January vs late March/April availability
    hi = p[p.date.between('2025-01-06', '2025-02-02')]
    lo = p[p.date.between('2025-03-15', '2025-04-20')]
    def rate(x, days):
        s = x.groupby('airbnb_listing_id').date.nunique()/days
        return 1 - s
    seas = pd.DataFrame({'occ_high': rate(hi, 28), 'occ_low': rate(lo, 37)})
    seas['season_concentration'] = seas.occ_high - seas.occ_low
    return pr.join(occ, how='outer').join(seas, how='outer')

# ------------------------------------------------------------------ 2. configuration
AMEN = {
    'am_crib':      r'Berço|Cadeira alta|Brinquedos|Berco|Portão de segurança',
    'am_workspace': r'Espaço de trabalho|Mesa de trabalho',
    'am_pool':      r'Piscina',
    'am_grill':     r'Churrasqueira',
    'am_gym':       r'Academia',
    'am_elevator':  r'Elevador',
    'am_beach':     r'Acesso à praia|Frente para a praia',
    'am_seaview':   r'[Vv]ista para o mar',
    'am_spa':       r'hidromassagem|Sauna',
    'am_parking':   r'Estacionamento',
    'am_dishwasher':r'Lava-louças',
}
TXT = {
    'tx_family':  r'famíli|criança|infantil',
    'tx_couple':  r'casal|casais|romântic|lua de mel',
    'tx_group':   r'amigos|grupo|galera|turma',
    'tx_biz':     r'executiv|negóci|corporativ|home office',
    'tx_long':    r'mensal|temporada longa|30 dias|longa estadia',
    'tx_luxury':  r'luxo|alto padrão|sofisticad|premium',
    'tx_seafront':r'frente ao mar|frente mar|beira-mar|pé na areia',
}

def configuration():
    det = pd.read_csv(RAW/'Details_Itapema.csv', low_memory=False)
    a = det.amenities.fillna(''); r = det.house_rules.fillna('')
    t = (det.ad_name.fillna('') + ' ' + det.ad_description.fillna('') + ' ' + det.space.fillna('')).str.lower()
    c = pd.DataFrame({'airbnb_listing_id': det.airbnb_listing_id})
    for k, v in AMEN.items(): c[k] = a.str.contains(v, regex=True).astype(int)
    for k, v in TXT.items():  c[k] = t.str.contains(v, regex=True).astype(int)
    c['pets_ok']       = (~r.str.contains('Não é permitido animais')).astype(int)
    c['guests']        = det.number_of_guests
    c['bedrooms']      = det.number_of_bedrooms
    c['beds']          = det.number_of_beds
    c['baths']         = det.number_of_bathrooms.fillna(1)
    c['beds_per_bed']  = det.number_of_beds/det.number_of_bedrooms.clip(lower=1)
    c['guests_per_bed']= det.number_of_guests/det.number_of_bedrooms.clip(lower=1)
    c['cleaning_fee']  = det.cleaning_fee
    return c

# ------------------------------------------------------------------ 3. segmentation
def assign(df):
    """Rule taxonomy over configuration. Rules are ordered: the first that fires wins,
    so every listing lands in exactly one segment and the definition is auditable."""
    seg = pd.Series('Não classificado', index=df.index)
    lux = (df.adr >= df.adr.quantile(.90)) | ((df.am_seaview == 1) & (df.adr >= df.adr.quantile(.75)))
    grp = (df.guests >= 8) & (df.baths >= 2)
    fam = (df.guests.between(4, 7)) & ((df.am_crib == 1) | (df.tx_family == 1) |
                                       ((df.bedrooms >= 2) & (df.am_pool + df.am_elevator >= 1)))
    cpl = (df.guests <= 4) | (df.bedrooms <= 1)
    seg[fam] = 'Famílias'
    seg[grp] = 'Grupos e amigos'
    seg[cpl & ~grp] = 'Casais e escapadas curtas'
    seg[lux] = 'Alto padrão e frente-mar'
    seg[seg == 'Não classificado'] = 'Famílias'      # residual: 2-3 dorm, 5-7 hóspedes
    return seg

def main():
    dem = weekend_and_season()
    cfg = configuration()
    l = pd.read_csv(OUT/'listing_investable.csv')
    df = (l.merge(cfg, on='airbnb_listing_id', how='left', suffixes=('', '_c'))
            .merge(dem, left_on='airbnb_listing_id', right_index=True, how='left'))
    df['segment'] = assign(df)
    df.to_csv(OUT/'guest_segments.csv', index=False)

    print('=== [DADO] o que a base mostra sobre quem procura Itapema ===')
    print(f'  menções a viagem de negócios no texto dos anúncios : {df.tx_biz.mean():.1%}')
    print(f'  menções a estadia longa / mensal                   : {df.tx_long.mean():.1%}')
    print(f'  anúncios que aceitam animais                       : {df.pets_ok.mean():.1%}')
    print(f'  anúncios com item infantil (berço, cadeira alta)   : {df.am_crib.mean():.1%}')
    print('  => negócios e estadia longa não são segmentos deste mercado; não vamos inventá-los.\n')

    agg = (df.groupby('segment')
             .agg(n=('adr','size'), guests=('guests','median'), dorm=('bedrooms','median'),
                  adr=('adr','median'), occ=('occ','median'),
                  rev=('rev_annual_gross','median'),
                  wk_price=('weekend_price_premium','median'),
                  wk_occ=('weekend_occ_lift','median'),
                  season=('season_concentration','median'),
                  fee=('cleaning_fee','median'),
                  prof=('is_professional','mean'), star=('star_rating','median'))
             .sort_values('rev', ascending=False))
    print('=== [DADO] cada segmento tem um padrão de demanda distinto ===')
    print(agg.round({'guests':1,'dorm':1,'adr':0,'occ':3,'rev':0,'wk_price':3,'wk_occ':3,
                     'season':3,'fee':0,'prof':2,'star':2}).to_string())

    zone = pd.crosstab(df.micro_zone, df.segment, normalize='index').round(3)
    print('\n=== [DADO] onde cada segmento está instalado (share dos anúncios da zona) ===')
    print(zone.to_string())
    cnt = pd.crosstab(df.micro_zone, df.segment)
    print('\n(contagens)'); print(cnt.to_string())

    zs = (df.groupby(['micro_zone','segment'])
            .agg(n=('adr','size'), adr=('adr','median'), occ=('occ','median'),
                 rev=('rev_annual_gross','median'), wk=('weekend_price_premium','median'))
            .reset_index())
    zs = zs[zs.n >= 10].sort_values('rev', ascending=False)
    print('\n=== [DADO] receita por zona × segmento (>=10 anúncios) ===')
    print(zs.round({'adr':0,'occ':3,'rev':0,'wk':3}).to_string(index=False))
    zs.to_csv(OUT/'zone_segment.csv', index=False)
    agg.to_csv(OUT/'segment_demand.csv')
    zone.to_csv(OUT/'zone_segment_mix.csv')

if __name__ == '__main__':
    main()

# ------------------------------------------------------------------ 4. opportunity matrix
def opportunity_matrix():
    """Investment profile → area → customer → demand → revenue → attractiveness.
    Cost comes from the sale market, demand from the Airbnb side, and the customer
    column is the dominant configured segment in that zone × size cell."""
    df   = pd.read_csv(OUT/'guest_segments.csv')
    sale = pd.read_csv(OUT/'sale_scored.csv', low_memory=False)
    ci   = pd.read_csv(OUT/'segment_yields_ci.csv'); ci.columns = ['zone','bed'] + list(ci.columns[2:])
    rows = []
    for _, y in ci.iterrows():
        z, b = y.zone, int(y.bed)
        ab = df[(df.micro_zone == z) & (df.bed_bucket == b)]
        sl = sale[(sale.micro_zone == z) & (sale.bed_bucket == b) & (sale.is_offplan == 0)]
        if len(ab) < 8 or len(sl) < 15: continue
        mix = ab.segment.value_counts(normalize=True)
        rows.append(dict(
            zone=z, bed=b, n_ab=len(ab), n_sale=len(sl),
            customer=mix.index[0], customer_share=float(mix.iloc[0]),
            customer_2=mix.index[1] if len(mix) > 1 else '',
            guests=float(ab.guests.median()), adr=float(ab.adr.median()),
            occ=float(ab.occ.median()), rev=float(ab.rev_annual_gross.median()),
            price=float(sl.sale_price.median()), area=float(sl.usable_area.median()),
            ppsm=float(sl.ppsm.median()), net_yield=float(y.net_yield),
            payback=float(1/y.net_yield), season=float(ab.season_concentration.median()),
            wk_price=float(ab.weekend_price_premium.median())))
    m = pd.DataFrame(rows).sort_values('net_yield', ascending=False)
    m['rev_rank']   = m.rev.rank(ascending=False).astype(int)
    m['yield_rank'] = m.net_yield.rank(ascending=False).astype(int)
    m['evidence']   = np.where(m.n_ab >= 40, 'forte', np.where(m.n_ab >= 15, 'média', 'fina'))
    m.to_csv(OUT/'opportunity_matrix.csv', index=False)
    print('\n=== [INFERIDO] matriz de oportunidades: perfil → área → cliente → retorno ===')
    cols = ['zone','bed','customer','customer_share','guests','adr','occ','rev','price','net_yield','payback','evidence','n_ab','n_sale']
    print(m[cols].round({'customer_share':2,'guests':1,'adr':0,'occ':2,'rev':0,'price':0,
                         'net_yield':4,'payback':1}).to_string(index=False))
    return m

if __name__ == '__main__':
    opportunity_matrix()
