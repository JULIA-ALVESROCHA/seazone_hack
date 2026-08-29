"""04 - Segment-level investment model.

Joins the Airbnb demand side (revenue per listing) with the VivaReal supply side
(acquisition cost per comparable unit) on zone x bedroom segments, then computes
gross yield, net yield (cap rate) and payback under explicit assumptions.
Every assumption is a named parameter so it can be swept in 06_robustness.py.
"""
import numpy as np, pandas as pd, json, itertools
import _paths
RAW, OUT = _paths.setup()
_paths.tee('log_04_investment_model.txt')

# ----------------------------- ASSUMPTIONS ---------------------------------
P = dict(
    lead_star        = 3,     # lead-time horizon treated as "final" availability
    booked_share     = 0.90,  # share of unavailable nights that are paid bookings (rest = owner blocks)
    host_take        = 0.90,  # share of the displayed nightly price the host receives (OTA fee)
    season_low_mult  = 0.50,  # May-Sep RevPAN as a multiple of observed April
    season_oct_mult  = 0.70,  # October
    season_nov_mult  = 1.00,  # November
    season_dec_mult  = 1.10,  # December as a multiple of observed January
    negotiation_disc = 0.07,  # discount from asking price to closing price
    closing_costs    = 0.05,  # ITBI + deed + registry
    furnish_per_m2   = 1200,  # STR-ready furnishing / equipping, R$ per m2
    mgmt_fee         = 0.20,  # management fee on gross booking revenue
    util_per_night   = 45,    # utilities + consumables per occupied night, R$
    fixed_monthly    = 250,   # internet/TV/insurance per month, R$
    maint_pct_value  = 0.005, # annual maintenance/reserve as % of property value
    iptu_pct_fallback= 0.005, # if IPTU not disclosed
)

# ----------------------------- DEMAND SIDE ---------------------------------
g=pd.read_csv(OUT/'listing_date_grid.csv.gz', parse_dates=['date'])
h=pd.Series({int(k):v for k,v in json.load(open(OUT/'booking_curve.json'))['h_lead'].items()})
g['lin_s']=g.lin - h.loc[0] + h.loc[P['lead_star']]
g['occ']=1-1/(1+np.exp(-g.lin_s))
g['rev']=g.occ*g.price_hat
mon=g.date.dt.month
obs_month=g.groupby(mon).rev.mean()          # observed RevPAN by month
jan, apr = obs_month.loc[1], obs_month.loc[4]

def annual_factor(p):
    """annual revenue / observed-window revenue, from the observed monthly shape"""
    days={1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
    rp={1:obs_month.loc[1],2:obs_month.loc[2],3:obs_month.loc[3],4:obs_month.loc[4]}
    for m in [5,6,7,8,9]: rp[m]=apr*p['season_low_mult']
    rp[10]=apr*p['season_oct_mult']; rp[11]=apr*p['season_nov_mult']; rp[12]=jan*p['season_dec_mult']
    annual=sum(rp[m]*days[m] for m in days)
    window=g.rev.sum()/g.airbnb_listing_id.nunique()
    return annual/window, annual
AF, annual_revpan_yr = annual_factor(P)
print(f'observed monthly RevPAN: {obs_month.round(0).to_dict()}')
print(f'annualisation factor (annual / observed 105-night window) = {AF:.2f}')

lst=g.groupby('airbnb_listing_id').agg(occ=('occ','mean'), rev_window=('rev','sum'),
                                       adr=('price_hat','mean'), nights=('date','size')).reset_index()
det=pd.read_csv(RAW/'Details_Itapema.csv', low_memory=False)
geo=pd.read_csv(OUT/'geo_features.csv')
lst=lst.merge(det[['airbnb_listing_id','number_of_bedrooms','number_of_guests','listing_type',
                   'number_of_reviews','star_rating','is_professional','cleaning_fee','picture_count',
                   'min_nights','number_of_bathrooms','is_guest_favorite','can_instant_book']],
              on='airbnb_listing_id', how='inner')
lst=lst.merge(geo[['airbnb_listing_id','suburb','micro_zone','dist_beach_km','comp_300m','comp_1km']],
              on='airbnb_listing_id', how='left')
lst=lst[lst.listing_type=='apartamento'].copy()          # the investable asset class
lst['rev_annual_gross']=lst.rev_window*AF*P['booked_share']*P['host_take']
lst['occ_paid']=lst.occ*P['booked_share']
lst['bed_bucket']=lst.number_of_bedrooms.clip(0,4)
lst.to_csv(OUT/'listing_investable.csv', index=False)
print('investable Airbnb listings with demand data:', len(lst))

# ----------------------------- SUPPLY SIDE ---------------------------------
sale=pd.read_csv(OUT/'sale_clean.csv', low_memory=False)
sale['bed_bucket']=sale.bedrooms.clip(0,4)
sale['micro_zone']=sale.micro_zone.replace({'Meia Praia (beach band)':'Meia Praia (beach band)',
    'Andorinha (inland Meia Praia)':'Meia Praia (inland)','Castelo Branco (inland Meia Praia)':'Meia Praia (inland)',
    'Jardim Praia Mar':'Jardim Praia Mar'})

def seg_table(zone_col):
    dem=lst.groupby([zone_col,'bed_bucket']).agg(
        n_ab=('rev_annual_gross','size'), occ=('occ_paid','median'), adr=('adr','median'),
        rev_med=('rev_annual_gross','median'), rev_p75=('rev_annual_gross',lambda s: s.quantile(.75)),
        rev_mean=('rev_annual_gross','mean')).reset_index()
    sup=sale.groupby([zone_col,'bed_bucket']).agg(
        n_sale=('sale_price','size'), price=('sale_price','median'),
        price_p25=('sale_price',lambda s: s.quantile(.25)),
        area=('usable_area','median'), ppsm=('ppsm','median'),
        condo=('monthly_condo_fee','median'), iptu=('yearly_iptu','median')).reset_index()
    return dem.merge(sup, on=[zone_col,'bed_bucket'], how='inner').rename(columns={zone_col:'zone'})

def economics(t, p, rev_col='rev_med', price_col='price'):
    t=t.copy()
    price=t[price_col]*(1-p['negotiation_disc'])
    capex=price*(1+p['closing_costs'])+t.area*p['furnish_per_m2']
    iptu=t.iptu.fillna(price*p['iptu_pct_fallback'])
    condo=t.condo.fillna(price*0.0)*12
    nights_booked=t.occ*365
    opex=(t[rev_col]*p['mgmt_fee'] + condo + iptu + nights_booked*p['util_per_night']
          + 12*p['fixed_monthly'] + price*p['maint_pct_value'])
    t['capex']=capex; t['noi']=t[rev_col]-opex; t['opex']=opex
    t['gross_yield']=t[rev_col]/capex
    t['net_yield']=t.noi/capex
    t['payback_yrs']=capex/t.noi
    t['rev_per_m2']=t[rev_col]/t.area
    return t

for zc in ['suburb','micro_zone']:
    t=seg_table(zc)
    t=economics(t,P)
    t=t[(t.n_ab>=8)&(t.n_sale>=15)].sort_values('net_yield',ascending=False)
    print(f'\n===== segment economics by {zc} (median listing) =====')
    cols=['zone','bed_bucket','n_ab','n_sale','occ','adr','rev_med','area','price','condo',
          'capex','noi','gross_yield','net_yield','payback_yrs','rev_per_m2']
    print(t[cols].round({'occ':2,'adr':0,'rev_med':0,'area':0,'price':0,'condo':0,'capex':0,'noi':0,
                         'gross_yield':4,'net_yield':4,'payback_yrs':1,'rev_per_m2':0}).to_string(index=False))
    t.to_csv(OUT/f'segments_{zc}.csv', index=False)
json.dump(P, open(OUT/'assumptions.json','w'), indent=1)
