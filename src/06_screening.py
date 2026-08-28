"""06 - Screen every VivaReal apartment: predicted STR revenue under Seazone
operation, full-cost investment economics, and a ranked buy list.

Bridging problem: Airbnb has capacity but not floor area; VivaReal has floor area
but not capacity. We bridge them with rank-preserving quantile matching inside
each (zone x bedrooms) cell, so a unit in the 70th area percentile is assigned
the 70th-percentile capacity of comparable Airbnb units in the same cell.
"""
import numpy as np, pandas as pd, json, re
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import KFold, cross_val_predict
OUT='/home/claude/proj/output/'
P=json.load(open(OUT+'assumptions.json'))

l=pd.read_csv(OUT+'listing_modelfeatures.csv')
s=pd.read_csv(OUT+'sale_clean.csv', low_memory=False)
s['bed_bucket']=s.bedrooms.clip(0,4)
s['micro_zone']=s.micro_zone.replace({'Andorinha (inland Meia Praia)':'Meia Praia (inland)',
    'Castelo Branco (inland Meia Praia)':'Meia Praia (inland)','Jardim Praia Mar':'Jardim Praia Mar'})

# ---- 1. distance-to-sea hints in the sale ad text -------------------------
txt=(s.listing_title.fillna('')+' ').str.lower()
mts=txt.str.extract(r'(\d{2,4})\s*(?:m|mts|metros)\s*d[oa]\s*mar')[0].astype(float)
s['txt_dist_m']=mts.where(mts.between(20,3000))
s['txt_frentemar']=txt.str.contains('frente mar|frente ao mar|beira[- ]mar').astype(int)
s['txt_quadra_mar']=txt.str.contains('quadra do mar|quadra mar').astype(int)
s['is_offplan']=txt.str.contains('lançamento|lancamento|na planta|em construção|em construcao|entrega ').astype(int)
print('sale ads with an explicit distance-to-sea:', int(s.txt_dist_m.notna().sum()),
      '| frente-mar:', int(s.txt_frentemar.sum()), '| off-plan:', int(s.is_offplan.sum()))

# zone median distance from the Airbnb side, refined by ad text where present
zmed=l.groupby('micro_zone').dist_beach_km.median()
s['dist_beach_km']=s.micro_zone.map(zmed)
s.loc[s.txt_dist_m.notna(),'dist_beach_km']=s.txt_dist_m/1000
s.loc[s.txt_frentemar==1,'dist_beach_km']=0.05
s['dist_beach_km']=s.dist_beach_km.fillna(l.dist_beach_km.median()).clip(0.03,5)

# ---- 2. capacity bridge: quantile match area -> guests inside each cell ----
s['guests_est']=np.nan
for (z,b),grp in s.groupby(['micro_zone','bed_bucket']):
    ref=l[(l.micro_zone==z)&(l.bed_bucket==b)].number_of_guests.dropna()
    if len(ref)<10: ref=l[l.bed_bucket==b].number_of_guests.dropna()
    q=grp.usable_area.rank(pct=True)
    s.loc[grp.index,'guests_est']=np.quantile(ref, q.clip(0.02,0.98))
s['guests_est']=s.guests_est.fillna((2*s.bedrooms+2)).clip(2,16)
print('capacity bridge -> median guests by bedrooms:',
      s.groupby('bed_bucket').guests_est.median().round(1).to_dict())

# ---- 3. revenue model trained on Airbnb, scored at "Seazone-operated" quality
FEA=['log_guests','dist_beach','baths','comp','pool','elevator','grill','bed']
def build(df, guests, dist, baths, comp, pool, elev, grill, bed, zone):
    X=pd.DataFrame({'log_guests':np.log(guests),'dist_beach':np.log(dist),'baths':baths,
                    'comp':np.log1p(comp),'pool':pool,'elevator':elev,'grill':grill,'bed':bed})
    Z=pd.get_dummies(pd.Categorical(zone, categories=sorted(l.micro_zone.dropna().unique())),prefix='z')
    return pd.concat([X.reset_index(drop=True), Z.astype(float).reset_index(drop=True)],axis=1)

Xtr=build(l, l.number_of_guests, l.dist_beach_km.clip(0.03,5), l.number_of_bathrooms.fillna(1),
          l.comp_300m, l.am_pool, l.am_elevator if 'am_elevator' in l else 0, l.am_grill,
          l.number_of_bedrooms, l.micro_zone)
# quality controls used only in training, so the sale-side score is a
# "professionally operated" counterfactual rather than an average-host outcome
Xtr['prof']=l.is_professional; Xtr['star']=l.star; Xtr['pics']=np.log1p(l.picture_count)
Xtr['logrev_host']=l.log_reviews
y=l.log_rev.values
gb=GradientBoostingRegressor(n_estimators=600,max_depth=3,learning_rate=0.04,subsample=0.8,random_state=1)
pred=cross_val_pred=cross_val_predict(gb,Xtr,y,cv=KFold(5,shuffle=True,random_state=0))
print('revenue model CV R2 = %.3f | median abs %% error = %.1f%%'%(
      1-((y-pred)**2).sum()/((y-y.mean())**2).sum(), 100*np.median(np.abs(np.expm1(pred-y)))))
gb.fit(Xtr,y)

zbath=l.groupby('bed_bucket').number_of_bathrooms.median()
zcomp=l.groupby('micro_zone').comp_300m.median()
Xte=build(s, s.guests_est, s.dist_beach_km, s.bed_bucket.map(zbath).fillna(1),
          s.micro_zone.map(zcomp).fillna(l.comp_300m.median()), s.am_pool,
          s.am_elevator, s.am_grill, s.bedrooms, s.micro_zone)
Xte['prof']=1; Xte['star']=l.star.quantile(.75); Xte['pics']=np.log1p(30)
Xte['logrev_host']=l.log_reviews.quantile(.75)
Xte=Xte[Xtr.columns]
resid_var=np.var(y-gb.predict(Xtr))
s['rev_pred']=np.exp(gb.predict(Xte)+resid_var/2)

# ---- 4. full investment economics per listing -----------------------------
price=s.sale_price*(1-P['negotiation_disc'])
s['capex']=price*(1+P['closing_costs'])+s.usable_area*P['furnish_per_m2']
condo=s.monthly_condo_fee.fillna(s.groupby(['micro_zone','bed_bucket']).monthly_condo_fee.transform('median')).fillna(450)*12
iptu=s.yearly_iptu.fillna(price*P['iptu_pct_fallback'])
# occupancy implied by the demand model for that zone/size cell
occ=l.groupby(['micro_zone','bed_bucket']).occ.median()
s['occ']=pd.MultiIndex.from_frame(s[['micro_zone','bed_bucket']]).map(occ)
s['occ']=s.occ.fillna(l.occ.median())*P['booked_share']
s['opex']=(s.rev_pred*P['mgmt_fee']+condo+iptu+s.occ*365*P['util_per_night']
           +12*P['fixed_monthly']+price*P['maint_pct_value'])
s['noi']=s.rev_pred-s.opex
s['gross_yield']=s.rev_pred/s.capex
s['net_yield']=s.noi/s.capex
s['payback_yrs']=s.capex/s.noi
s['condo_annual']=condo
# comparability confidence: how much Airbnb evidence backs this cell
cell_n=l.groupby(['micro_zone','bed_bucket']).size()
s['n_comps']=pd.MultiIndex.from_frame(s[['micro_zone','bed_bucket']]).map(cell_n).fillna(0)
s.to_csv(OUT+'sale_scored.csv',index=False)

print('\n=== net yield distribution by zone x bedrooms (ready-to-use stock only) ===')
r=s[(s.is_offplan==0)&(s.n_comps>=10)]
tab=r.groupby(['micro_zone','bed_bucket']).agg(n=('net_yield','size'),price=('sale_price','median'),
    rev=('rev_pred','median'),ny_med=('net_yield','median'),ny_p90=('net_yield',lambda x:x.quantile(.9)),
    pay=('payback_yrs','median')).sort_values('ny_med',ascending=False)
print(tab[tab.n>=15].round({'price':0,'rev':0,'ny_med':4,'ny_p90':4,'pay':1}).to_string())

print('\n=== TOP 25 individual buy candidates (ready stock, credible comps) ===')
top=r[(r.sale_price.between(300_000,3_000_000))].nlargest(25,'net_yield')
cols=['listing_id','micro_zone','bedrooms','usable_area','sale_price','monthly_condo_fee',
      'rev_pred','noi','net_yield','payback_yrs','advertiser_name']
print(top[cols].round({'rev_pred':0,'noi':0,'net_yield':4,'payback_yrs':1}).to_string(index=False))
