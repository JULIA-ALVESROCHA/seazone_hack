"""09 - Quality-adjusted screen + budget allocation, and model validation checks."""
import numpy as np, pandas as pd, json
from sklearn.model_selection import KFold
from sklearn.ensemble import GradientBoostingRegressor
import _paths
RAW, OUT = _paths.setup()
_paths.tee('log_09_portfolio.txt')
P=json.load(open(OUT/'assumptions.json'))
l=pd.read_csv(OUT/'listing_modelfeatures.csv'); s=pd.read_csv(OUT/'sale_scored.csv',low_memory=False)

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
print(f'   Airbnb revenue gradient on the same variable was -0.09 (revenue) / -0.07 (ADR).')
print(f'   => the sale market discounts distance MORE than (' + 
      f'{b[1]:+.3f} vs -0.09) the rental market rewards proximity.'
      if abs(b[1])>=0.10 else
      f'   => the sale market discounts distance similarly to the rental market ({b[1]:+.3f} vs -0.09).')

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
r.sort_values('net_yield_adj',ascending=False).to_csv(OUT/'buy_list_adjusted.csv',index=False)

print('\n=== quality-adjusted net yield by segment ===')
t=r.groupby(['micro_zone','bed_bucket']).agg(n=('net_yield_adj','size'),price=('sale_price','median'),
   ny=('net_yield_adj','median'),ny_p75=('net_yield_adj',lambda x:x.quantile(.75)))
print(t[t.n>=15].sort_values('ny',ascending=False).round({'price':0,'ny':4,'ny_p75':4}).to_string())

# ---------- budget allocation ---------------------------------------------
print('\n=== R$20M deployment, greedy on adjusted yield with concentration caps ===')
print('    restricted to the recommended compact-2BR profile, honoring the')
print('    recommended weights: core Morretes/Tabuleiro 55-60% (the bet),')
print('    compact 2BR sleeve on the Meia Praia split as insurance.')
CORE = {('Morretes', 2), ('Tabuleiro dos Oliveiras', 2)}
SLEEVE = {('Meia Praia (beach band)', 2), ('Meia Praia (inland)', 2)}
PROFILE = CORE | SLEEVE
key = list(zip(r.micro_zone, r.bed_bucket))
r = r[pd.Series(key, index=r.index).isin(PROFILE)].copy()
BUD=20_000_000; CORE_BUD=0.60*BUD; MAXADV=0.30
picks=[]; spent=0; core_spent=0; adv={}

def _take(row, role):
    global picks, spent, core_spent
    c=row.capex
    a=row.advertiser_name
    if adv.get(a,0)+c>MAXADV*BUD: return False
    picks.append(row); spent+=c
    if role=='core': core_spent+=c
    adv[a]=adv.get(a,0)+c
    return True

# stage 1: the core bet (Morretes/Tabuleiro 2BR) up to 60% of budget
core_r = r[pd.Series(list(zip(r.micro_zone, r.bed_bucket)), index=r.index).isin(CORE)]
for _,row in core_r.sort_values('net_yield_adj',ascending=False).iterrows():
    if spent+row.capex>BUD or core_spent+row.capex>CORE_BUD: continue
    _take(row,'core')
# stage 2: sleeve fills toward the full budget (compact 2BR on the Meia Praia split)
slv_r = r[pd.Series(list(zip(r.micro_zone, r.bed_bucket)), index=r.index).isin(SLEEVE)]
for _,row in slv_r.sort_values('net_yield_adj',ascending=False).iterrows():
    if spent+row.capex>BUD: continue
    _take(row,'sleeve')
pf=pd.DataFrame(picks)
print(f'   {len(pf)} units, capital deployed R${spent/1e6:.1f}M, '
      f'blended net yield {pf.noi_adj.sum()/pf.capex.sum():.2%}, '
      f'payback {pf.capex.sum()/pf.noi_adj.sum():.1f} years, '
      f'annual NOI R${pf.noi_adj.sum()/1e6:.2f}M')
print(f'   core share {core_spent/spent:.0%} (target 55-60%), sleeve share {1-core_spent/spent:.0%}')
print(f'   asking-price range R${pf.sale_price.min():,.0f}–R${pf.sale_price.max():,.0f}'
      f' · median R${pf.sale_price.median():,.0f} · '
      f'{100*(pf.sale_price.between(680_000, 850_000).mean()):.0f}% within the R$680–850k band'
      .replace(',', '.'))
print(pf.groupby(['micro_zone','bed_bucket']).agg(units=('capex','size'),
      capital=('capex','sum'), noi=('noi_adj','sum')).assign(yld=lambda d:d.noi/d.capital).round(
      {'capital':0,'noi':0,'yld':4}).to_string())
pf.to_csv(OUT/'portfolio_20m.csv',index=False)

# ---- unconstrained reference for the appendix (discipline vs value) -------
MAXSEG = 0.45  # per-segment cap for the opportunistic mix
rALL = s[(s.is_offplan==0)&(s.n_comps>=25)&(s.sale_price.between(400_000,2_000_000))].copy()
cellA=rALL.groupby(['micro_zone','bed_bucket']).ppsm
medA=cellA.transform('median'); iqrA=cellA.transform(lambda x:x.quantile(.75)-x.quantile(.25))
rALL['ppsm_ratio']=rALL.ppsm/medA
rALL=rALL[(rALL.ppsm-medA)/iqrA>-2.0]
rALL['rev_adj']=rALL.rev_pred*np.clip(rALL.ppsm_ratio,0.5,1.3)**0.35
priceA=rALL.sale_price*(1-P['negotiation_disc'])
condoA=rALL.monthly_condo_fee.fillna(450)*12
rALL['noi_adj']=rALL.rev_adj-(rALL.rev_adj*P['mgmt_fee']+condoA+priceA*P['iptu_pct_fallback']
                            +rALL.occ*365*P['util_per_night']+12*P['fixed_monthly']+priceA*P['maint_pct_value'])
rALL['net_yield_adj']=rALL.noi_adj/rALL.capex
picksA=[]; spentA=0; a1={}; a2={}
for _,row in rALL.sort_values('net_yield_adj',ascending=False).iterrows():
    c=row.capex
    if spentA+c>BUD: continue
    k=(row.micro_zone,row.bed_bucket); a=row.advertiser_name
    if a1.get(k,0)+c>MAXSEG*BUD or a2.get(a,0)+c>MAXADV*BUD: continue
    picksA.append(row); spentA+=c; a1[k]=a1.get(k,0)+c; a2[a]=a2.get(a,0)+c
pfA=pd.DataFrame(picksA)
print('\n=== appendix: unconstrained mix (any cell, incl. cheap 3-4BR orla) for contrast ===')
print(f'   {len(pfA)} units, R${spentA/1e6:.1f}M, blended {pfA.noi_adj.sum()/pfA.capex.sum():.2%}, '
      f'payback {pfA.capex.sum()/pfA.noi_adj.sum():.1f}y, NOI R${pfA.noi_adj.sum()/1e6:.2f}M')
print(pfA.groupby(['micro_zone','bed_bucket']).agg(units=('capex','size'),
      capital=('capex','sum')).round(0).to_string())
pfA.to_csv(OUT/'portfolio_unconstrained.csv',index=False)
