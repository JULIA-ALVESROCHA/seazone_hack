"""09 - Quality-adjusted screen + budget allocation, and model validation checks."""
import numpy as np, pandas as pd, json
from sklearn.model_selection import KFold
from sklearn.ensemble import GradientBoostingRegressor
OUT='/home/claude/proj/output/'; P=json.load(open(OUT+'assumptions.json'))
l=pd.read_csv(OUT+'listing_modelfeatures.csv'); s=pd.read_csv(OUT+'sale_scored.csv',low_memory=False)

# ---------- VALIDATION 1: does modelled occupancy track realised demand? ----
l['rev_bucket']=pd.qcut(l.rev_annual_gross,5,labels=[1,2,3,4,5])
print('validation 1 - modelled revenue quintile vs observed review counts (realised stays):')
print(l.groupby('rev_bucket',observed=True).agg(n=('occ','size'),occ=('occ','mean'),adr=('adr','median'),
      reviews=('number_of_reviews','median'),superhost=('is_superhost','mean')).round(2).to_string())
r=l[['rev_annual_gross','number_of_reviews']].corr(method='spearman').iloc[0,1]
print(f'   Spearman(modelled revenue, number of reviews) = {r:.3f}')

# ---------- VALIDATION 2: hold out whole listings from the price model ------
print('\nvalidation 2 - out-of-sample error of the revenue model (5-fold, by listing): see 06 output')

# ---------- VALIDATION 3: is the sale market priced on the same gradient? ---
sale=s[s.is_offplan==0].copy()
sale['log_ppsm']=np.log(sale.ppsm); sale['log_dist']=np.log(sale.dist_beach_km)
import numpy.linalg as la
Xs=np.column_stack([np.ones(len(sale)),sale.log_dist,np.log(sale.usable_area)])
b=la.lstsq(Xs,sale.log_ppsm.values,rcond=None)[0]
print(f'\nvalidation 3 - sale-price gradient: d log(price/m2) / d log(distance to sea) = {b[1]:+.3f}')
print(f'   Airbnb revenue gradient on the same variable was about -0.46 to -0.51.')
print('   => the sale market discounts distance LESS than the rental market rewards proximity'
      if abs(b[1])<0.45 else '   => the sale market already prices proximity as hard as the rental market.')

# ---------- quality-adjusted screen ---------------------------------------
r=s[(s.is_offplan==0)&(s.n_comps>=25)&(s.sale_price.between(400_000,2_000_000))].copy()
cell=r.groupby(['micro_zone','bed_bucket']).ppsm
med=cell.transform('median'); iqr=cell.transform(lambda x:x.quantile(.75)-x.quantile(.25))
r['ppsm_ratio']=r.ppsm/med
r=r[(r.ppsm-med)/iqr>-2.0]
# a unit priced below its comparables is probably older / worse positioned inside the
# zone; assume part of that discount also shows up in achievable revenue.
r['rev_adj']=r.rev_pred*np.clip(r.ppsm_ratio,0.5,1.3)**0.35
price=r.sale_price*(1-P['negotiation_disc'])
condo=r.monthly_condo_fee.fillna(450)*12
r['noi_adj']=r.rev_adj-(r.rev_adj*P['mgmt_fee']+condo+price*P['iptu_pct_fallback']
                        +r.occ*365*P['util_per_night']+12*P['fixed_monthly']+price*P['maint_pct_value'])
r['net_yield_adj']=r.noi_adj/r.capex
r['payback_adj']=r.capex/r.noi_adj
print('\n=== quality-adjusted shortlist (top 15) ===')
cols=['listing_id','micro_zone','bedrooms','usable_area','sale_price','ppsm','ppsm_ratio',
      'monthly_condo_fee','rev_adj','noi_adj','net_yield_adj','payback_adj']
print(r.nlargest(15,'net_yield_adj')[cols].round(
    {'ppsm':0,'ppsm_ratio':2,'rev_adj':0,'noi_adj':0,'net_yield_adj':4,'payback_adj':1}).to_string(index=False))
r.sort_values('net_yield_adj',ascending=False).to_csv(OUT+'buy_list_adjusted.csv',index=False)

print('\n=== quality-adjusted net yield by segment ===')
t=r.groupby(['micro_zone','bed_bucket']).agg(n=('net_yield_adj','size'),price=('sale_price','median'),
   ny=('net_yield_adj','median'),ny_p75=('net_yield_adj',lambda x:x.quantile(.75)))
print(t[t.n>=15].sort_values('ny',ascending=False).round({'price':0,'ny':4,'ny_p75':4}).to_string())

# ---------- budget allocation ---------------------------------------------
print('\n=== R$20M deployment, greedy on adjusted yield with concentration caps ===')
BUD=20_000_000; MAXSEG=0.45; MAXADV=0.30
picks=[]; spent=0; seg={}; adv={}
for _,row in r.sort_values('net_yield_adj',ascending=False).iterrows():
    c=row.capex
    if spent+c>BUD: continue
    k=(row.micro_zone,row.bed_bucket); a=row.advertiser_name
    if seg.get(k,0)+c>MAXSEG*BUD or adv.get(a,0)+c>MAXADV*BUD: continue
    picks.append(row); spent+=c; seg[k]=seg.get(k,0)+c; adv[a]=adv.get(a,0)+c
pf=pd.DataFrame(picks)
print(f'   {len(pf)} units, capital deployed R${spent/1e6:.1f}M, '
      f'blended net yield {pf.noi_adj.sum()/pf.capex.sum():.2%}, '
      f'payback {pf.capex.sum()/pf.noi_adj.sum():.1f} years, '
      f'annual NOI R${pf.noi_adj.sum()/1e6:.2f}M')
print(pf.groupby(['micro_zone','bed_bucket']).agg(units=('capex','size'),capital=('capex','sum'),
      noi=('noi_adj','sum')).assign(yld=lambda d:d.noi/d.capital).round(
      {'capital':0,'noi':0,'yld':4}).to_string())
pf.to_csv(OUT+'portfolio_20m.csv',index=False)
