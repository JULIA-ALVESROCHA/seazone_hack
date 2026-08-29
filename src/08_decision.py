"""08 - Decision layer: controlled tests, deployable-capital view, robust buy list,
and the headline investment case with sensitivity."""
import numpy as np, pandas as pd, json
from sklearn.linear_model import RidgeCV
import _paths
RAW, OUT = _paths.setup()
_paths.tee('log_08_decision.txt')
P=json.load(open(OUT/'assumptions.json')); rng=np.random.default_rng(3)
l=pd.read_csv(OUT/'listing_modelfeatures.csv'); s=pd.read_csv(OUT/'sale_scored.csv',low_memory=False)

# ---- A. is the Centro occupancy gap real once we control for what we can? --
X=pd.DataFrame({'log_guests':np.log(l.number_of_guests),'log_dist':np.log(l.dist_beach_km.clip(0.03,5)),
  'star':l.star,'log_reviews':l.log_reviews,'prof':l.is_professional,'superhost':l.is_superhost,
  'pics':np.log1p(l.picture_count),'comp':np.log1p(l.comp_300m),'minn':np.log1p(l.min_nights),
  'centro':(l.suburb=='Centro').astype(int),'compact':(l.number_of_bedrooms<=1).astype(int)})
X['centro_x_compact']=X.centro*X.compact
for tgt,name in [(np.log(l.occ/(1-l.occ)),'log-odds occupancy'),(np.log(l.adr),'log ADR')]:
    m=RidgeCV(alphas=np.logspace(-3,3,25)).fit(X,tgt)
    bs=pd.DataFrame([pd.Series(RidgeCV(alphas=np.logspace(-3,3,12)).fit(X.iloc[i],tgt.iloc[i]).coef_,index=X.columns)
                     for i in (rng.integers(0,len(X),len(X)) for _ in range(300))])
    print(f'\n{name}: R2={m.score(X,tgt):.3f}')
    for k in ['centro','compact','centro_x_compact','log_dist','log_guests','prof','star']:
        c=pd.Series(m.coef_,index=X.columns)[k]; lo,hi=bs[k].quantile([.025,.975])
        star='*' if lo*hi>0 else ' '
        print(f'   {k:18s} {c:+.3f} [{lo:+.3f},{hi:+.3f}] {star}')

# ---- B. how much capital can each segment actually absorb? ----------------
print('\n=== deployable stock: listed, ready-to-use apartments (asking-price value) ===')
cap=s[s.is_offplan==0].groupby(['micro_zone','bed_bucket']).agg(
    n_listed=('sale_price','size'), med_price=('sale_price','median'),
    stock_value=('sale_price','sum'))
cap=cap[cap.n_listed>=15].sort_values('stock_value',ascending=False)
cap['stock_value_Rmi']=(cap.stock_value/1e6).round(0)
print(cap[['n_listed','med_price','stock_value_Rmi']].round(0).to_string())

# ---- C. robust individual buy list ---------------------------------------
print('\n=== robust buy list: outlier-guarded, ready stock, credible comparables ===')
r=s[(s.is_offplan==0)&(s.n_comps>=25)&(s.sale_price.between(400_000,2_000_000))].copy()
cell=r.groupby(['micro_zone','bed_bucket']).ppsm
r['ppsm_z']=(r.ppsm-cell.transform('median'))/cell.transform(lambda x: x.quantile(.75)-x.quantile(.25))
guard=r[(r.ppsm_z>-1.5)]                     # drop implausibly cheap / likely-erroneous ads
print(f'   {len(r)-len(guard)} listings dropped as price outliers vs their own cell')
top=guard.nlargest(20,'net_yield')[['listing_id','micro_zone','bedrooms','usable_area','sale_price',
     'ppsm','monthly_condo_fee','rev_pred','noi','net_yield','payback_yrs','advertiser_name']]
print(top.round({'ppsm':0,'rev_pred':0,'noi':0,'net_yield':4,'payback_yrs':1}).to_string(index=False))
guard.sort_values('net_yield',ascending=False).to_csv(OUT/'buy_list.csv',index=False)

# ---- D. headline case vs the hypothesis case ------------------------------
def case(zone,bed,label,price=None):
    sl=s[(s.micro_zone==zone)&(s.bed_bucket==bed)&(s.is_offplan==0)]
    ab=l[(l.micro_zone==zone)&(l.bed_bucket==bed)]
    pr=(price or sl.sale_price.median())*(1-P['negotiation_disc']); area=sl.usable_area.median()
    capex=pr*(1+P['closing_costs'])+area*P['furnish_per_m2']
    rev=sl.rev_pred.median(); occ=ab.occ.median()*P['booked_share']
    condo=(sl.monthly_condo_fee.median() if np.isfinite(sl.monthly_condo_fee.median()) else 450)*12
    iptu=pr*P['iptu_pct_fallback']
    opex=rev*P['mgmt_fee']+condo+iptu+occ*365*P['util_per_night']+12*P['fixed_monthly']+pr*P['maint_pct_value']
    return dict(case=label,area=area,ask=(price or sl.sale_price.median()),capex=capex,adr=ab.adr.median(),
                occ=occ,rev=rev,opex=opex,noi=rev-opex,net_yield=(rev-opex)/capex,payback=capex/(rev-opex),
                n_listed=len(sl))
cases=pd.DataFrame([case('Morretes',2,'RECOMMENDED: compact 2BR, Morretes'),
                    case('Tabuleiro dos Oliveiras',2,'compact 2BR, Tabuleiro'),
                    case('Morretes',3,'compact 3BR, Morretes (higher yield, higher location risk)'),
                    case('Meia Praia (beach band)',2,'SLEEVE / liquidity: compact 2BR, beach band'),
                    case('Centro',1,'HYPOTHESIS: 1BR in Centro'),
                    case('Meia Praia (beach band)',4,'large 4BR, beach band (avoid)')])
print('\n=== investment cases (Seazone-operated, base assumptions) ===')
print(cases.round({'area':0,'ask':0,'capex':0,'adr':0,'occ':2,'rev':0,'opex':0,'noi':0,
                   'net_yield':4,'payback':1}).to_string(index=False))
cases.to_csv(OUT/'investment_cases.csv',index=False)
