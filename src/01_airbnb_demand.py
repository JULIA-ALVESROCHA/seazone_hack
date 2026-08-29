"""
01 - Airbnb demand model for Itapema.

Turns Price_AV (a scraped availability calendar) into per-listing occupancy,
ADR and revenue over the observed window, correcting for booking lead time.

Key insight: Price_AV contains ONE ROW PER (listing, stay-date) ONLY WHEN THE
NIGHT IS AVAILABLE. A missing (listing, stay-date) inside a capture window is
therefore an *unavailable* night (booked or blocked). Availability observed far
ahead of the stay date overstates final availability, so we estimate a booking
curve h(lead) and project every listing to lead = 0.

Model:  logit P(available | listing i, stay-date d, lead L) = a_i + f_d + h(L)
Final occupancy for (i,d):  1 - sigmoid(a_i + f_d + h(0))
"""
import numpy as np, pandas as pd
from scipy import sparse
from sklearn.linear_model import LogisticRegression, Ridge
import json, os
import _paths
RAW, OUT = _paths.setup()
_paths.tee('log_01_airbnb_demand.txt')

price = pd.read_csv(RAW/'Price_AV_Itapema.csv', low_memory=False)
price['date'] = pd.to_datetime(price['date'])
price['cap']  = pd.to_datetime(price['aquisition_date']).dt.normalize()
price = price.drop_duplicates(['airbnb_listing_id','date','cap'])

# ---- 1. build the (listing, date, capture) availability panel -------------
caps = sorted(price.cap.unique())
frames = []
for c in caps:
    g = price[price.cap == c]
    wmax = g.date.max()                      # scrape horizon for this capture
    dates = pd.date_range(c, wmax)
    ids = np.sort(g.airbnb_listing_id.unique())   # listings observed in this capture
    idx = pd.MultiIndex.from_product([ids, dates], names=['airbnb_listing_id','date'])
    f = pd.DataFrame(index=idx).reset_index()
    f['cap'] = c
    f = f.merge(g[['airbnb_listing_id','date','price']], on=['airbnb_listing_id','date'], how='left')
    f['avail'] = f.price.notna().astype(int)
    frames.append(f)
panel = pd.concat(frames, ignore_index=True)
panel['lead'] = (panel.date - panel.cap).dt.days
print('panel rows', len(panel), 'listings', panel.airbnb_listing_id.nunique(),
      'avail rate', panel.avail.mean().round(3))

# ---- 2. logistic FE model for availability --------------------------------
lst = pd.Categorical(panel.airbnb_listing_id)
dat = pd.Categorical(panel.date)
led = pd.Categorical(panel.lead)
nL, nD, nH = len(lst.categories), len(dat.categories), len(led.categories)
rows = np.arange(len(panel))
X = sparse.hstack([
    sparse.csr_matrix((np.ones(len(panel)), (rows, lst.codes)), shape=(len(panel), nL)),
    sparse.csr_matrix((np.ones(len(panel)), (rows, dat.codes)), shape=(len(panel), nD)),
    sparse.csr_matrix((np.ones(len(panel)), (rows, led.codes)), shape=(len(panel), nH)),
]).tocsr()
clf = LogisticRegression(penalty='l2', C=50.0, solver='lbfgs', max_iter=800, fit_intercept=False)
clf.fit(X, panel.avail.values)
b = clf.coef_[0]
a_i = pd.Series(b[:nL], index=lst.categories)
f_d = pd.Series(b[nL:nL+nD], index=dat.categories)
h_L = pd.Series(b[nL+nD:], index=led.categories)
print('booking curve h(L) at L=0,7,30,60,90:',
      [round(float(h_L.reindex([l]).iloc[0]),3) if l in h_L.index else None for l in [0,7,30,60,90]])
h0 = float(h_L.loc[0])

# ---- 3. price model: log price ~ listing FE + date FE ---------------------
obs = panel[panel.avail == 1].copy()
lst2 = pd.Categorical(obs.airbnb_listing_id, categories=lst.categories)
dat2 = pd.Categorical(obs.date, categories=dat.categories)
r2 = np.arange(len(obs))
Xp = sparse.hstack([
    sparse.csr_matrix((np.ones(len(obs)), (r2, lst2.codes)), shape=(len(obs), nL)),
    sparse.csr_matrix((np.ones(len(obs)), (r2, dat2.codes)), shape=(len(obs), nD)),
]).tocsr()
rg = Ridge(alpha=1.0, fit_intercept=False, solver='sparse_cg')
rg.fit(Xp, np.log(obs.price.values))
p_i = pd.Series(rg.coef_[:nL], index=lst.categories)
p_d = pd.Series(rg.coef_[nL:], index=dat.categories)
resid = np.log(obs.price.values) - Xp @ rg.coef_
sig2 = resid.var()
print('price model R2', 1 - sig2/np.log(obs.price.values).var())

# ---- 4. project every listing over the full observed window ---------------
all_dates = pd.DatetimeIndex(dat.categories)
grid = pd.MultiIndex.from_product([lst.categories, all_dates],
                                  names=['airbnb_listing_id','date']).to_frame(index=False)
grid['lin'] = grid.airbnb_listing_id.map(a_i) + grid.date.map(f_d) + h0
grid['p_avail_final'] = 1/(1+np.exp(-grid.lin))
grid['occ'] = 1 - grid.p_avail_final
grid['price_hat'] = np.exp(grid.airbnb_listing_id.map(p_i) + grid.date.map(p_d) + sig2/2)
grid['exp_rev'] = grid.occ * grid.price_hat
grid.to_csv(OUT/'listing_date_grid.csv.gz', index=False)

lst_sum = grid.groupby('airbnb_listing_id').agg(
    nights=('date','size'), occ=('occ','mean'),
    adr=('price_hat','mean'), revpan=('exp_rev','mean'),
    rev_window=('exp_rev','sum')).reset_index()
# ADR weighted by occupancy = what a booked night actually earns
w = grid.groupby('airbnb_listing_id').apply(
        lambda g: np.average(g.price_hat, weights=g.occ), include_groups=False)
lst_sum['adr_booked'] = lst_sum.airbnb_listing_id.map(w)
lst_sum.to_csv(OUT/'listing_demand.csv', index=False)
print(lst_sum[['occ','adr','adr_booked','revpan','rev_window']].describe().round(1).to_string())

# weekly revenue-per-available-night series for the demand slide (model-projected,
# lead-3, so the seasonal shape is comparable across the whole window)
MES = {1: 'jan', 2: 'fev', 3: 'mar', 4: 'abr', 5: 'mai', 6: 'jun',
       7: 'jul', 8: 'ago', 9: 'set', 10: 'out', 11: 'nov', 12: 'dez'}
week = (grid.groupby(grid.date.dt.to_period('W').dt.start_time)
            .exp_rev.mean().reset_index().rename(columns={'date': 'week_start'}))
week['label'] = week.week_start.dt.day.astype(str) + ' ' + \
    week.week_start.dt.month.map(MES)
week.to_csv(OUT/'weekly_revpan.csv', index=False)
print('weekly model RevPAN (label, revpan):')
print(week[['label', 'exp_rev']].round(0).to_string(index=False))

json.dump({'h_lead': {str(k): float(v) for k, v in h_L.items()},
           'window_start': str(all_dates.min().date()),
           'window_end': str(all_dates.max().date()),
           'n_nights': int(len(all_dates))}, open(OUT/'booking_curve.json','w'), indent=1)
