import os, pandas as pd
from fpdf import FPDF

BASE = os.path.dirname(os.path.dirname(__file__))
EXPORT = os.path.join(BASE, 'export')
os.makedirs(EXPORT, exist_ok=True)

def generate_state_report(state_name, data, gdf, year):
    # Very simple PDF summary: state name, year, top metrics
    pop = data['population']
    df = pop[(pop['state_name'].str.lower()==state_name.lower()) & (pop['year']==int(year))]
    if df.empty:
        summary = [['State', state_name], ['Year', year], ['Note', 'No data found']]
    else:
        row = df.mean(numeric_only=True)
        summary = [['State', state_name], ['Year', year],
                   ['Population (avg)', int(row.get('population_total',0))],
                   ['Population density (avg)', int(row.get('population_density',0))]]
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, f'State Report: {state_name} - {year}', ln=True)
    pdf.ln(4)
    pdf.set_font('Arial', '', 12)
    for k,v in summary:
        pdf.cell(0,8,f'{k}: {v}', ln=True)
    out = os.path.join(EXPORT, f'report_{state_name.replace(" ","_")}_{year}.pdf')
    pdf.output(out)
    return out
