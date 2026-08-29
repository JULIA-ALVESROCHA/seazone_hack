"""07b - Correct estimate of the distance-to-sea gradient on BOTH sides of the
market, holding product constant, and a corrected location stress test."""
import numpy as np, pandas as pd, json, numpy.linalg as la
import _paths
RAW, OUT = _paths.setup()
_paths.tee('log_07b_distance.txt')
P=json.load(open(OUT/'assumptions.json'))
l=pd.read_csv(OUT/'listing_modelfeatures.csv'); s=pd.read_csv(OUT/'sale_scored.csv',low_memory=False)

def ols(X,y):
    b=la.lstsq(X,y,rcond=None)[0]; e=y-X@b
    se=np.sqrt(np.diag(np.linalg.pinv(X.T@X))*e.var(ddof=X.shape[1]))
    return b,se

print('=== distance-to-sea gradient, product held constant ===')
d=l[l.dist_beach_km>0]
B=pd.get_dummies(d.bed_bucket,prefix='b').astype(float).values
X=np.column_stack([np.log(d.dist_beach_km),np.log(d.number_of_guests),d.is_professional,d.star,B])
for tgt,name in [(np.log(d.rev_annual_gross),'Airbnb annual revenue'),(np.log(d.adr),'Airbnb ADR'),
                 (np.log(d.occ/(1-d.occ)),'Airbnb occupancy (log-odds)')]:
    b,se=ols(X,tgt.values); print(f'  {name:32s} elasticity {b[0]:+.3f} (se {se[0]:.3f})')
sale=s[(s.is_offplan==0)&(s.dist_beach_km>0)]
Bs=pd.get_dummies(sale.bed_bucket,prefix='b').astype(float).values
Xs=np.column_stack([np.log(sale.dist_beach_km),np.log(sale.usable_area),Bs])
b,se=ols(Xs,np.log(sale.ppsm.values)); print(f'  {"VivaReal asking price per m2":32s} elasticity {b[0]:+.3f} (se {se[0]:.3f})')
ELAST=b[0]
b2,se2=ols(Xs,np.log(sale.sale_price.values)); print(f'  {"VivaReal asking price (total)":32s} elasticity {b2[0]:+.3f} (se {se2[0]:.3f})')

print('\n  => revenue falls ~%.0f%% and asking price ~%.0f%% for each doubling of distance'
      %(100*(1-2**ols(X,np.log(d.rev_annual_gross).values)[0][0]),100*(1-2**b2[0])))

# corrected location stress test
SEGS=[('Morretes',3),('Morretes',2),('Tabuleiro dos Oliveiras',2),('Meia Praia (beach band)',2),
      ('Meia Praia (inland)',2),('Centro',1),('Centro',2),('Meia Praia (beach band)',3),
      ('Meia Praia (inland)',3),('Centro',3),('Meia Praia (beach band)',4)]
def seg_yield(p,dist_adj=None,rev_elast=-0.12):
    out={}
    for z,b in SEGS:
        sl=s[(s.micro_zone==z)&(s.bed_bucket==b)&(s.is_offplan==0)]; ab=l[(l.micro_zone==z)&(l.bed_bucket==b)]
        if len(ab)<8 or len(sl)<15: continue
        rev=sl.rev_pred.median()
        if dist_adj and z in dist_adj: rev*= dist_adj[z]**rev_elast
        pr=sl.sale_price.median()*(1-p['negotiation_disc']); area=sl.usable_area.median()
        capex=pr*(1+p['closing_costs'])+area*p['furnish_per_m2']
        condo=(sl.monthly_condo_fee.median() if np.isfinite(sl.monthly_condo_fee.median()) else 450)*12
        occ=ab.occ.median()*p['booked_share']
        opex=rev*p['mgmt_fee']+condo+pr*p['iptu_pct_fallback']+occ*365*p['util_per_night']+12*p['fixed_monthly']+pr*p['maint_pct_value']
        out[(z,b)]=(rev-opex)/capex
    return pd.Series(out)
print('\n=== corrected stress test: off-beach sale stock is X times further from the sea')
print('    than its Airbnb comparables (revenue elasticity -0.12, pessimistic -0.30) ===')
for el in [-0.12,-0.30]:
    for x in [1.0,2.0,3.0]:
        y=seg_yield(P,{z:x for z in ['Morretes','Tabuleiro dos Oliveiras','Meia Praia (inland)']},el)
        print(f'  elast {el:+.2f}, distance x{x:.0f}: '+', '.join(f'{k[0][:13]} {k[1]}BR {v:.3f}' for k,v in y.nlargest(4).items()))
