import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
import json, os
from utils.data_loader import load_all_data, ensure_geo_loaded
from utils.pdf_export import generate_state_report

st.set_page_config(layout="wide", page_title="India Trends Dashboard", initial_sidebar_state="expanded")
st.title("India — Population, Housing & Employment Explorer (Dark mode)")

# Sidebar controls
data, mapping = load_all_data()  # returns dicts/dataframes
gdf = ensure_geo_loaded()

st.sidebar.header("Controls")
level = st.sidebar.selectbox("Level", ["district","state"])
metric = st.sidebar.selectbox("Metric", list(data['population'].columns.drop(['district_name','state_name','year'])) if 'population' in data else ["population_total"])
year = st.sidebar.selectbox("Year", sorted(data['population']['year'].unique().tolist()))

# Filter population df for year
pop_df = data['population'][data['population']['year']==int(year)].copy()

if level == "district":
    merged = gdf.merge(pop_df, left_on="district_name", right_on="district_name", how="left")
    title = f"District-level: {metric} ({year})"
else:
    # aggregate to state using mapping
    agg = pop_df.groupby('state_name').mean(numeric_only=True).reset_index()
    gstate = gdf.dissolve(by="state_name", aggfunc='first').reset_index()
    merged = gstate.merge(agg, on="state_name", how="left")
    title = f"State-level: {metric} ({year})"

fig = px.choropleth_mapbox(merged, geojson=json.loads(merged.to_json()), locations=merged.index,
                           color=metric, mapbox_style="open-street-map",
                           center={"lat":23.0,"lon":80.0}, zoom=3, opacity=0.6,
                           hover_name=merged.get("district_name", merged.get("state_name")),
                           hover_data={metric:True})
fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0}, title=title)
st.plotly_chart(fig, use_container_width=True)

# State-level charts
if level=="state":
    st.header("State-level trends")
    # line chart for population over years for selected metric
    st.subheader("Population trend (states)")
    df_ts = data['population'].groupby(['state_name','year'])[metric].mean().reset_index()
    st.line_chart(df_ts.pivot(index='year', columns='state_name', values=metric))

# PDF export
st.sidebar.markdown("### Export")
state_choice = st.sidebar.text_input("State name (for report)", value="Example State A")
if st.sidebar.button("Generate State Report"):
    out = generate_state_report(state_choice, data, gdf, year)
    st.sidebar.success(f"Report saved to {out}")
