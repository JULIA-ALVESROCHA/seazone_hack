"""02 - VivaReal sale market: cleaning, geography normalisation, price surfaces."""
import numpy as np, pandas as pd, re
import _paths
RAW, OUT = _paths.setup()
_paths.tee('log_02_sale_market.txt')
v=pd.read_csv(RAW/'VivaReal_Itapema.csv', low_memory=False)
print('raw', v.shape)
v=v.drop_duplicates('listing_id')
# de-duplicate near-identical relistings (same advertiser, price, area, bedrooms)
v['dupkey']=v.advertiser_name.astype(str)+'|'+v.sale_price.astype(str)+'|'+v.usable_area.astype(str)+'|'+v.bedrooms.astype(str)+'|'+v.suburb.astype(str)
print('near-dup groups removed:', v.duplicated('dupkey').sum())
v=v.drop_duplicates('dupkey')

# ---- geography: VivaReal suburb is finer than the Airbnb mesh taxonomy ----
def norm(s):
    if pd.isna(s): return np.nan
    s=s.strip().lower()
    s=(s.replace('ã','a').replace('á','a').replace('â','a').replace('é','e')
         .replace('ê','e').replace('í','i').replace('ó','o').replace('ô','o').replace('ú','u').replace('ç','c'))
    return re.sub(r'\s+',' ',s)
v['sub_raw']=v.suburb.map(norm)
# micro-zone kept for within-region detail; macro-zone matches the Airbnb mesh
MACRO={'meia praia':'Meia Praia','andorinha':'Meia Praia','castelo branco':'Meia Praia',
       'jardim praia mar':'Jardim Praia Mar','centro':'Centro','canto da praia':'Canto da Praia',
       'morretes':'Morretes','tabuleiro dos oliveiras':'Tabuleiro dos Oliveiras','tabuleiro':'Tabuleiro dos Oliveiras',
       'casa branca':'Casa Branca','alto sao bento':'Alto Sao Bento','ilhota':'Ilhota','varzea':'Varzea',
       'sertao do trombudo':'Sertao do Trombudo','sertaozinho':'Sertaozinho','areal':'Areal',
       'leopoldo zarling':'Leopoldo Zarling','lameiro':'Lameiro','estreito':'Centro','itapema':np.nan}
MICRO={'meia praia':'Meia Praia (beach band)','andorinha':'Andorinha (inland Meia Praia)',
       'castelo branco':'Castelo Branco (inland Meia Praia)','jardim praia mar':'Jardim Praia Mar'}
v['macro_zone']=v.sub_raw.map(MACRO)
v['micro_zone']=v.sub_raw.map(lambda s: MICRO.get(s, MACRO.get(s, np.nan)))

# ---- validity filters -----------------------------------------------------
v['sale_price']=pd.to_numeric(v.sale_price, errors='coerce')
v['usable_area']=pd.to_numeric(v.usable_area, errors='coerce')
v['monthly_condo_fee']=pd.to_numeric(v.monthly_condo_fee, errors='coerce').replace(0,np.nan)
v['yearly_iptu']=pd.to_numeric(v.yearly_iptu, errors='coerce').replace(0,np.nan)
v['ppsm']=v.sale_price/v.usable_area
flags={}
flags['price<50k or >20M']=((v.sale_price<50_000)|(v.sale_price>20_000_000)).sum()
flags['area<20 or >800 m2']=((v.usable_area<20)|(v.usable_area>800)).sum()
flags['ppsm<2k or >40k']=((v.ppsm<2000)|(v.ppsm>40000)).sum()
flags['condo fee > 5% of price/yr']=(v.monthly_condo_fee*12 > 0.05*v.sale_price).sum()
print('\nquality flags:', flags)
clean=v[(v.listing_type=='apartamento')&v.sale_price.between(50_000,20_000_000)
        &v.usable_area.between(20,800)&v.ppsm.between(2000,40000)].copy()
clean.loc[clean.monthly_condo_fee*12 > 0.05*clean.sale_price,'monthly_condo_fee']=np.nan
clean.loc[clean.yearly_iptu > 0.03*clean.sale_price,'yearly_iptu']=np.nan
print('clean apartments', len(clean), 'of', (v.listing_type=='apartamento').sum())

# ---- amenity flags --------------------------------------------------------
for a,c in [('POOL','am_pool'),('ELEVATOR','am_elevator'),('GYM','am_gym'),
            ('BARBECUE_GRILL','am_grill'),('PARTY_HALL','am_partyhall'),
            ('PLAYGROUND','am_playground'),('SAUNA','am_sauna'),('FURNISHED','am_furnished')]:
    clean[c]=clean.amenities.fillna('').str.contains(a).astype(int)
clean['is_beachfront_title']=clean.listing_title.str.lower().str.contains('frente mar|frente ao mar|beira mar').astype(int)
clean.to_csv(OUT/'sale_clean.csv', index=False)

print('\n-- median asking price / m2 by macro zone x bedrooms (n>=15) --')
t=clean.groupby(['macro_zone','bedrooms']).agg(n=('sale_price','size'),price=('sale_price','median'),
        area=('usable_area','median'),ppsm=('ppsm','median'),condo=('monthly_condo_fee','median'))
print(t[t.n>=15].round(0).to_string())
print('\n-- micro zone (Meia Praia split) --')
t2=clean[clean.macro_zone=='Meia Praia'].groupby(['micro_zone','bedrooms']).agg(
    n=('sale_price','size'),price=('sale_price','median'),area=('usable_area','median'),ppsm=('ppsm','median'))
print(t2[t2.n>=10].round(0).to_string())
