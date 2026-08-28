"""05 - What explains revenue, and does the Centro + compact hypothesis survive?"""
import numpy as np, pandas as pd, json, re
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import KFold, cross_val_score
from sklearn.linear_model import RidgeCV
OUT='/home/claude/proj/output/'; D='/home/claude/data/data/'
rng=np.random.default_rng(7)

l=pd.read_csv(OUT+'listing_investable.csv')
det=pd.read_csv(D+'Details_Itapema.csv', low_memory=False)[['airbnb_listing_id','amenities','ad_description','space','owner_id']]
hosts=pd.read_csv(D+'Hosts_ids_Itapema.csv', low_memory=False).drop_duplicates('owner_id')
l=l.merge(det,on='airbnb_listing_id',how='left').merge(
    hosts[['owner_id','is_superhost','years_host','number_of_reviews_host','response_rate_shown']],
    on='owner_id',how='left')
AM={'am_pool':'Piscina','am_ac':'Ar-condicionado','am_wifi':'Wi-Fi','am_grill':'Churrasqueira',
    'am_parking':'Estacionamento','am_elevator':'Elevador','am_seaview':'Vista para o mar',
    'am_beachfront':'Acesso à praia','am_washer':'Máquina de [Ll]avar','am_gym':'Academia',
    'am_hottub':'Banheira de hidromassagem|Jacuzzi','am_crib':'Berço','am_workspace':'Espaço de trabalho'}
for k,v in AM.items(): l[k]=l.amenities.fillna('').str.contains(v,regex=True).astype(int)
l['n_amenities']=l.amenities.fillna('[]').str.count('","')+1
l['desc_len']=l.ad_description.fillna('').str.len()
l['is_superhost']=(l.is_superhost.astype(str)=='True').astype(int)
l['is_professional']=(l.is_professional.astype(str)=='True').astype(int)
l['is_guest_favorite']=(l.is_guest_favorite.astype(str)=='True').astype(int)
l['instant']=(l.can_instant_book.astype(str)=='true').astype(int)
l['has_rating']=(l.star_rating>0).astype(int)
l['star']=l.star_rating.where(l.star_rating>0)
l['star']=l.star.fillna(l.star.median())
l['log_rev']=np.log(l.rev_annual_gross)
l['log_reviews']=np.log1p(l.number_of_reviews)
l['is_centro']=(l.suburb=='Centro').astype(int)
l['compact']=(l.number_of_bedrooms<=1).astype(int)

feats=['number_of_bedrooms','number_of_guests','number_of_bathrooms','dist_beach_km','comp_300m',
       'star','has_rating','log_reviews','is_superhost','is_professional','is_guest_favorite',
       'instant','picture_count','min_nights','n_amenities','desc_len','years_host','cleaning_fee']+list(AM)
zon=pd.get_dummies(l.micro_zone,prefix='z')
X=pd.concat([l[feats].astype(float).fillna(0), zon.astype(float)],axis=1)
y=l.log_rev.values

gb=GradientBoostingRegressor(n_estimators=500,max_depth=3,learning_rate=0.05,subsample=0.8,random_state=0)
cv=cross_val_score(gb,X,y,cv=KFold(5,shuffle=True,random_state=0),scoring='r2')
print('GBM CV R2 on log annual revenue: %.3f (+/- %.3f)'%(cv.mean(),cv.std()))
gb.fit(X,y)
imp=pd.Series(gb.feature_importances_,index=X.columns).sort_values(ascending=False)
print('\nTop revenue drivers (GBM importance):'); print(imp.head(18).round(3).to_string())

# permutation-style partial effects on the natural scale
base=gb.predict(X)
print('\nPartial effect of key features (median % change in revenue when moved p25 -> p75):')
for f in ['number_of_guests','dist_beach_km','star','log_reviews','is_superhost','is_professional',
          'am_pool','am_seaview','picture_count','comp_300m','number_of_bedrooms']:
    lo,hi=X[f].quantile(.25),X[f].quantile(.75)
    if lo==hi: lo,hi=X[f].min(),X[f].max()
    Xa=X.copy(); Xa[f]=lo; Xb=X.copy(); Xb[f]=hi
    print(f'  {f:22s} {lo:8.2f} -> {hi:8.2f} : {100*(np.exp(gb.predict(Xb).mean()-gb.predict(Xa).mean())-1):+6.1f}%')

# ---- interpretable linear benchmark with zone fixed effects ---------------
lin=['np.log guests','dist_beach_km','star','log_reviews','is_superhost','is_professional','picture_count']
Xl=pd.concat([pd.DataFrame({'log_guests':np.log(l.number_of_guests),'dist_beach':l.dist_beach_km,
    'star':l.star,'log_reviews':l.log_reviews,'superhost':l.is_superhost,'prof':l.is_professional,
    'pics':np.log1p(l.picture_count),'baths':l.number_of_bathrooms.fillna(1),
    'comp':np.log1p(l.comp_300m)}), zon.astype(float)],axis=1).fillna(0)
r=RidgeCV(alphas=np.logspace(-3,3,25)).fit(Xl,y)
print('\nLinear (log-log) elasticities, zone fixed effects, R2=%.3f:'%r.score(Xl,y))
print(pd.Series(r.coef_,index=Xl.columns).round(3).head(9).to_string())

# =================== HYPOTHESIS TEST ======================================
print('\n'+'='*78)
print('H0 test: "compact (studio/1BR) units in Centro are the most efficient investment"')
print('='*78)
seg=pd.read_csv(OUT+'segments_micro_zone.csv')
sale=pd.read_csv(OUT+'sale_clean.csv',low_memory=False)

print('\n[1] Does the product exist on the acquisition market?')
ap=sale.groupby(sale.bedrooms.clip(0,4)).size()
print('   apartments for sale by bedrooms:', ap.to_dict())
print('   studios (0 BR) for sale:', int((sale.bedrooms==0).sum()))
print('   1BR for sale in Centro:', int(((sale.bedrooms==1)&(sale.macro_zone=="Centro")).sum()),
      '| 1BR city-wide:', int((sale.bedrooms==1).sum()),
      f'({100*(sale.bedrooms==1).mean():.1f}% of listed apartments)')

print('\n[2] Raw revenue and occupancy, Centro vs rest, by bedroom count:')
t=l.groupby(['is_centro','bed_bucket']).agg(n=('log_rev','size'),occ=('occ','median'),
      adr=('adr','median'),rev=('rev_annual_gross','median')).round(2)
print(t.to_string())

print('\n[3] Centro effect controlling for size, quality, distance and competition:')
Xc=Xl.copy()
Xc=Xc.drop(columns=[c for c in Xc.columns if c.startswith('z_')])
Xc['centro']=l.is_centro.values
Xc['compact']=l.compact.values
Xc['centro_x_compact']=(l.is_centro*l.compact).values
rc=RidgeCV(alphas=np.logspace(-3,3,25)).fit(Xc,y)
co=pd.Series(rc.coef_,index=Xc.columns)
def boot(Xc,y,n=400):
    out=[]
    for _ in range(n):
        i=rng.integers(0,len(y),len(y))
        m=RidgeCV(alphas=np.logspace(-3,3,15)).fit(Xc.iloc[i],y[i])
        out.append(pd.Series(m.coef_,index=Xc.columns))
    return pd.DataFrame(out)
B=boot(Xc,y)
for k in ['centro','compact','centro_x_compact','dist_beach']:
    ci=B[k].quantile([.025,.975])
    print(f'   {k:20s} coef {co[k]:+.3f}  (bootstrap 95% CI {ci.iloc[0]:+.3f}, {ci.iloc[1]:+.3f})'
          f'  => {100*(np.exp(co[k])-1):+.1f}% revenue')

print('\n[4] Efficiency (gross revenue / acquisition price) by segment, ranked:')
seg['rev_to_price']=seg.rev_med/(seg.price*(1-0.07))
sel=seg[(seg.n_ab>=8)&(seg.n_sale>=15)][['zone','bed_bucket','n_ab','n_sale','rev_med','price','rev_to_price','net_yield','payback_yrs']]
print(sel.sort_values('rev_to_price',ascending=False).round({'rev_med':0,'price':0,'rev_to_price':4,'net_yield':4,'payback_yrs':1}).to_string(index=False))
l.to_csv(OUT+'listing_modelfeatures.csv',index=False)
