#!/usr/bin/env python3
import os, requests, pandas as pd
BASE = os.path.dirname(__file__)
RAW = os.path.join(BASE, 'raw')
GEO = os.path.join(BASE, 'geo')
os.makedirs(RAW, exist_ok=True)
os.makedirs(GEO, exist_ok=True)

print('This script downloads pre-compiled Census CSV and district GeoJSON from known open repos.')
CENSUS_URL = 'https://raw.githubusercontent.com/nishusharma1608/India-Census-2011-Analysis/master/india-districts-census-2011.csv'
GEO_URL = 'https://raw.githubusercontent.com/datameet/maps/master/State/India_districts.geojson'
WIKI_URL = 'https://en.wikipedia.org/wiki/List_of_states_and_union_territories_of_India_by_unemployment_rate'

try:
    r = requests.get(CENSUS_URL, timeout=60)
    r.raise_for_status()
    with open(os.path.join(RAW, 'census_full_districts_2011_source.csv'), 'wb') as f:
        f.write(r.content)
    print('Census CSV saved.')
except Exception as e:
    print('Census download failed:', e)

try:
    r = requests.get(GEO_URL, timeout=60)
    r.raise_for_status()
    with open(os.path.join(GEO, 'india_districts.geojson'), 'wb') as f:
        f.write(r.content)
    print('GeoJSON saved.')
except Exception as e:
    print('GeoJSON download failed:', e)

# parse wiki for unemployment
try:
    tables = pd.read_html(WIKI_URL)
    # pick first sensible table
    tbl = tables[0]
    tbl.to_csv(os.path.join(RAW, 'plfs_unemployment_states.csv'), index=False)
    print('PLFS/state unemployment saved.')
except Exception as e:
    print('PLFS download failed:', e)

print('Done. If any download failed, please run this script again on a machine with internet access or provide local files.')
