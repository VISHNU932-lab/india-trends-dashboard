import os, pandas as pd, geopandas as gpd, json

BASE = os.path.dirname(os.path.dirname(__file__))
DATA = os.path.join(BASE, 'data')
GEO = os.path.join(BASE, 'geo')
RAW = os.path.join(BASE, 'raw')

def load_csv_try(paths):
    for p in paths:
        full = os.path.join(RAW, p)
        if os.path.exists(full):
            try:
                return pd.read_csv(full)
            except Exception:
                pass
    # fallback to sample in data/
    for p in paths:
        full = os.path.join(DATA, p.replace('census_','sample_') )
        if os.path.exists(full):
            return pd.read_csv(full)
    raise FileNotFoundError('No CSV found for '+str(paths))

def load_all_data():
    data = {}
    data['population'] = load_csv_try(['census_population_districts.csv','census_full_districts_2011_source.csv','sample_population.csv'])
    data['housing'] = load_csv_try(['census_housing_districts.csv','sample_housing.csv'])
    data['employment_states'] = load_csv_try(['plfs_unemployment_states.csv','sample_employment.csv'])
    # mapping
    mapping_file = os.path.join(RAW, 'district_state_mapping.csv')
    if os.path.exists(mapping_file):
        mapping = pd.read_csv(mapping_file)
    else:
        mapping = pd.read_csv(os.path.join(DATA, 'district_state_mapping.csv'))
    return data, mapping

def ensure_geo_loaded():
    geo_full = os.path.join(GEO, 'india_districts.geojson')
    sample = os.path.join(GEO, 'sample_districts.geojson')
    if os.path.exists(geo_full):
        return gpd.read_file(geo_full)
    else:
        return gpd.read_file(sample)
