"""07 - Bootstrap confidence intervals and assumption sweeps on the segment ranking."""
import numpy as np, pandas as pd, json, itertools
OUT='/home/claude/proj/output/'
P=json.load(open(OUT+'assumptions.json'))
rng=np.random.default_rng(11)
l=pd.read_csv(OUT+'listing_modelfeatures.csv')
s=pd.read_csv(OUT+'sale_scored.csv',low_memory=False)
g=pd.read_csv(OUT+'listing_date_grid.csv.gz',parse_dates=['date'])
h=pd.Series({int(k):v for k,v in json.load(open(OUT+'booking_curve.json'))['h_lead'].items()})

SEGS=[('Morretes',3),('Morretes',2),('Tabuleiro dos Oliveiras',2),('Meia Praia (beach band)',2),
      ('Meia Praia (inland)',2),('Centro',1),('Centro',2),('Meia Praia (beach band)',3),
      ('Meia Praia (inland)',3),('Centro',3),('Meia Praia (beach band)',4)]

# ---------- A. revenue-per-m2 vs price-per-m2: the core ratio ---------------
print('=== capacity density: what a buyer gets per m2 and per R$ ===')
rows=[]
for z,b in SEGS:
    ab=l[(l.micro_zone==z)&(l.bed_bucket==b)]
    sl=s[(s.micro_zone==z)&(s.bed_bucket==b)&(s.is_offplan==0)]
    if len(ab)<8 or len(sl)<15: continue
    rows.append(dict(zone=z,bed=b,n_ab=len(ab),n_sale=len(sl),
        guests=ab.number_of_guests.median(), area=sl.usable_area.median(),
        guests_per_m2=ab.number_of_guests.median()/sl.usable_area.median(),
        ppsm=sl.ppsm.median(), rev_market=ab.rev_annual_gross.median(),
        rev_prof=sl.rev_pred.median(),
        rev_per_m2=sl.rev_pred.median()/sl.usable_area.median(),
        price_med=sl.sale_price.median()))
R=pd.DataFrame(rows); R['rev_per_m2_over_ppsm']=R.rev_per_m2/R.ppsm
print(R.sort_values('rev_per_m2_over_ppsm',ascending=False).round(
    {'guests':1,'area':0,'guests_per_m2':3,'ppsm':0,'rev_market':0,'rev_prof':0,'rev_per_m2':0,
     'price_med':0,'rev_per_m2_over_ppsm':4}).to_string(index=False))

# ---------- B. bootstrap CI on segment net yield ---------------------------
def seg_yield(p, rev_scale=1.0, dist_adj=None, use_prof=True, boot=False):
    out={}
    for z,b in SEGS:
        sl=s[(s.micro_zone==z)&(s.bed_bucket==b)&(s.is_offplan==0)]
        ab=l[(l.micro_zone==z)&(l.bed_bucket==b)]
        if len(ab)<8 or len(sl)<15: continue
        if boot:
            sl=sl.iloc[rng.integers(0,len(sl),len(sl))]; ab=ab.iloc[rng.integers(0,len(ab),len(ab))]
        rev=(sl.rev_pred.median() if use_prof else ab.rev_annual_gross.median())*rev_scale
        if dist_adj and z in dist_adj: rev*= dist_adj[z]
        price=sl.sale_price.median()*(1-p['negotiation_disc'])
        area=sl.usable_area.median()
        capex=price*(1+p['closing_costs'])+area*p['furnish_per_m2']
        condo=(sl.monthly_condo_fee.median() if np.isfinite(sl.monthly_condo_fee.median()) else 450)*12
        iptu=price*p['iptu_pct_fallback']
        occ=ab.occ.median()*p['booked_share']
        opex=rev*p['mgmt_fee']+condo+iptu+occ*365*p['util_per_night']+12*p['fixed_monthly']+price*p['maint_pct_value']
        out[(z,b)]=(rev-opex)/capex
    return pd.Series(out)

base=seg_yield(P)
B=pd.DataFrame([seg_yield(P,boot=True) for _ in range(500)])
ci=B.quantile([.05,.95]).T
print('\n=== net yield, Seazone-operated scenario, with bootstrap 90% CI ===')
tab=pd.DataFrame({'net_yield':base,'lo':ci[0.05],'hi':ci[0.95]}).sort_values('net_yield',ascending=False)
tab['payback']=1/tab.net_yield
print((tab*[1,1,1,1]).round({'net_yield':4,'lo':4,'hi':4,'payback':1}).to_string())

# ---------- C. assumption sweep -------------------------------------------
print('\n=== assumption sweep: how often is each segment in the top 3? ===')
grid=dict(booked_share=[0.80,0.90,1.00], host_take=[0.85,0.90,1.00],
          season_low_mult=[0.35,0.50,0.65], furnish_per_m2=[800,1200,1800],
          mgmt_fee=[0.15,0.20,0.25], negotiation_disc=[0.0,0.07,0.12],
          util_per_night=[30,45,65])
keys=list(grid); counts={}; ranks={k:[] for k in base.index}; n=0
for combo in itertools.product(*[grid[k] for k in keys]):
    p=dict(P); p.update(dict(zip(keys,combo)))
    scale=(p['booked_share']/P['booked_share'])*(p['host_take']/P['host_take'])
    # season multiplier changes the annualisation factor roughly linearly on the low months
    scale*= (0.60+0.40*p['season_low_mult']/P['season_low_mult'])
    y=seg_yield(p, rev_scale=scale)
    r=y.rank(ascending=False)
    for k in y.index: ranks[k].append(r[k])
    for k in y.nlargest(3).index: counts[k]=counts.get(k,0)+1
    n+=1
sw=pd.DataFrame({'top3_freq':pd.Series(counts)/n,
                 'mean_rank':pd.Series({k:np.mean(v) for k,v in ranks.items()})}).sort_values('mean_rank')
print(f'({n} assumption combinations)'); print(sw.round(3).to_string())

# ---------- D. the Morretes location risk ----------------------------------
print('\n=== stress test: what if the off-beach sale stock is further from the sea')
print('    than the Airbnb comparables suggest? (elasticity -0.5 on log distance) ===')
for extra in [1.0,1.5,2.0,3.0]:
    adj={z: extra**-0.5 for z in ['Morretes','Tabuleiro dos Oliveiras','Meia Praia (inland)']}
    y=seg_yield(P,dist_adj=adj)
    print(f'  distance x{extra:.1f} for off-beach zones -> ' +
          ', '.join(f'{k[0][:14]} {k[1]}BR {v:.3f}' for k,v in y.nlargest(4).items()))

# ---------- E. market-quality (not Seazone-operated) view ------------------
print('\n=== same ranking using the MEDIAN EXISTING listing instead of a professional operator ===')
y2=seg_yield(P,use_prof=False).sort_values(ascending=False)
print(y2.round(4).to_string())
tab.to_csv(OUT+'segment_yields_ci.csv'); sw.to_csv(OUT+'assumption_sweep.csv'); R.to_csv(OUT+'capacity_density.csv',index=False)
