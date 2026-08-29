"""03 - Spatial features for Airbnb listings: data-derived coastline, distance to
beach, local competition density (KD-tree), and micro-zone assignment that lines
up with the finer VivaReal neighbourhood taxonomy."""
import numpy as np, pandas as pd
from scipy.spatial import cKDTree
import _paths
RAW, OUT = _paths.setup()
_paths.tee('log_03_spatial.txt')
mesh=pd.read_csv(RAW/'Mesh_Ids_Data_Itapema.csv')
det=pd.read_csv(RAW/'Details_Itapema.csv', low_memory=False)

# --- coastline estimated as the eastern envelope of the listing point cloud
mm=mesh.copy()
mm['latbin']=(mm.latitude*400).round()/400
env=mm.groupby('latbin').longitude.quantile(0.97)
env=env[env.index.to_series().between(-27.152,-27.052)].sort_index()
env=env.rolling(3,center=True,min_periods=1).median()
coast=np.column_stack([env.index.values, env.values])
# densify the polyline
fine_lat=np.arange(coast[:,0].min(), coast[:,0].max(), 0.0002)
fine_lon=np.interp(fine_lat, coast[:,0], coast[:,1])
CO=np.column_stack([fine_lat*111.32, fine_lon*111.32*np.cos(np.radians(27.1))])  # km

XY=np.column_stack([mesh.latitude.values*111.32,
                    mesh.longitude.values*111.32*np.cos(np.radians(27.1))])
tree_c=cKDTree(CO)
mesh['dist_beach_km']=tree_c.query(XY)[0]
# competition density: listings within 300 m / 1 km (KD-tree, O(n log n))
tree_l=cKDTree(XY)
mesh['comp_300m']=[len(x)-1 for x in tree_l.query_ball_point(XY, 0.3)]
mesh['comp_1km'] =[len(x)-1 for x in tree_l.query_ball_point(XY, 1.0)]

def micro(r):
    if r.suburb!='Meia Praia': return r.suburb
    return 'Meia Praia (beach band)' if r.dist_beach_km<=0.35 else 'Meia Praia (inland)'
mesh['micro_zone']=mesh.apply(micro, axis=1)
mesh.to_csv(OUT/'geo_features.csv', index=False)
print(mesh.groupby('suburb').dist_beach_km.describe()[['count','25%','50%','75%']].round(2).to_string())
print('\nmicro zone counts:'); print(mesh.micro_zone.value_counts().head(8).to_string())
print('\ndist_beach deciles vs comp_300m:')
mesh['db']=pd.qcut(mesh.dist_beach_km,10,duplicates='drop')
print(mesh.groupby('db',observed=True).agg(n=('comp_300m','size'),comp=('comp_300m','mean')).round(1).to_string())
