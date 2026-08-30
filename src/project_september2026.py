import os
import sys
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

# Agency columns
AGENCIES = [
    'Apoyo y Asociados Internacionales',
    'Class y Asociados S.A.',
    'JCR Latino America',
    'Microrate',
    'Moodys Local PE Clasificadora de Riesgo',
    'PCR (Pacific Credit Rating)'
]

# Rating scale numerical mapping
RATING_MAP = {
    'A+': 12,
    'A': 11,
    'A-': 10,
    'B+': 9,
    'B': 8,
    'B-': 7,
    'C+': 6,
    'C': 5,
    'C-': 4,
    'D+': 3,
    'D': 2,
    'E': 1,
    'RET': 0
}

INV_RATING_MAP = {v: k for k, v in RATING_MAP.items()}

def num_to_rating(score):
    if pd.isna(score) or score is None:
        return ''
    rounded = int(round(score))
    rounded = max(0, min(12, rounded))
    return INV_RATING_MAP.get(rounded, '')

def get_risk_level(score):
    if pd.isna(score) or score is None:
        return 'Sin Clasificación'
    if score >= 11.5:
        return 'Riesgo Mínimo (A+)'
    elif score >= 9.5:
        return 'Bajo Riesgo (A / A-)'
    elif score >= 7.5:
        return 'Riesgo Moderado (B+ / B)'
    elif score >= 5.5:
        return 'Riesgo Medio-Alto (B- / C+)'
    elif score >= 3.5:
        return 'Alto Riesgo (C / C-)'
    else:
        return 'Riesgo Crítico / Estrés (D / RET)'

def parse_sbs_file(filepath):
    """
    Parses SBS HTML table format (.xls export).
    Returns DataFrame with columns: Tipo, Entidad, and per-agency rating / cambio indicator.
    """
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    table = soup.find('table', class_='gridStyle')
    if not table:
        raise ValueError(f"No gridStyle table found in {filepath}")
        
    headers = [th.get_text(strip=True) for th in table.find_all('th')]
    
    rows = []
    for tr in table.find_all('tr', class_='data'):
        tds = tr.find_all('td', recursive=False)
        if len(tds) < 8:
            continue
        tipo = tds[0].get_text(strip=True)
        entidad = tds[1].get_text(strip=True)
        
        row = {'Tipo': tipo, 'Entidad': entidad}
        
        for idx, agency in enumerate(AGENCIES, start=2):
            td = tds[idx]
            inner = td.find('table', class_='tblInnerResumen')
            if inner:
                cat_el = inner.find('td', class_='categoria')
                cat = cat_el.get_text(strip=True) if cat_el else ''
                
                cambio_el = inner.find('td', class_='cambio')
                cambio = cambio_el.get_text(strip=True) if cambio_el else ''
                
                row[agency] = cat
                row[agency + '_cambio'] = cambio
            else:
                row[agency] = ''
                row[agency + '_cambio'] = ''
        rows.append(row)
        
    return pd.DataFrame(rows)

def build_projection():
    file_sep25 = os.path.join('Data', 'septiembre2025.xls')
    file_mar26 = os.path.join('Data', 'marzo2026.xls')
    
    print(f"Reading {file_sep25}...")
    df_sep25 = parse_sbs_file(file_sep25)
    print(f"Reading {file_mar26}...")
    df_mar26 = parse_sbs_file(file_mar26)
    
    # Merge entities
    merged = pd.merge(
        df_mar26[['Tipo', 'Entidad'] + AGENCIES + [a + '_cambio' for a in AGENCIES]],
        df_sep25[['Tipo', 'Entidad'] + AGENCIES + [a + '_cambio' for a in AGENCIES]],
        on=['Tipo', 'Entidad'],
        suffixes=('_mar26', '_sep25'),
        how='left'
    )
    
    # Projection results structures
    df_proj_sbs = df_mar26[['Tipo', 'Entidad']].copy()
    
    entity_summary = []
    
    # Detail transition tracker
    transition_list = []

    for idx, row in merged.iterrows():
        tipo = row['Tipo']
        entidad = row['Entidad']
        
        scores_sep25 = []
        scores_mar26 = []
        scores_proj26 = []
        
        upgrades_count = 0
        downgrades_count = 0
        
        for ag in AGENCIES:
            r_sep25 = row.get(ag + '_sep25', '')
            r_mar26 = row.get(ag + '_mar26', '')
            c_mar26 = row.get(ag + '_cambio_mar26', '')
            
            val_sep25 = RATING_MAP.get(r_sep25, np.nan) if pd.notna(r_sep25) and r_sep25 != '' else np.nan
            val_mar26 = RATING_MAP.get(r_mar26, np.nan) if pd.notna(r_mar26) and r_mar26 != '' else np.nan
            
            if pd.notna(val_sep25):
                scores_sep25.append(val_sep25)
            if pd.notna(val_mar26):
                scores_mar26.append(val_mar26)
                
            # Projection logic for agency rating
            r_proj = r_mar26
            proj_indicator = ''
            
            if pd.notna(val_mar26):
                # Check momentum
                if c_mar26 == '↑' or (pd.notna(val_sep25) and val_mar26 > val_sep25):
                    # Positive momentum
                    upgrades_count += 1
                    # Projection: consolidate or 1 notch higher if strong momentum
                    val_proj = min(12, val_mar26 + 0.5)
                    r_proj = num_to_rating(val_proj)
                    proj_indicator = '↑'
                elif c_mar26 == '↓' or (pd.notna(val_sep25) and val_mar26 < val_sep25):
                    # Negative momentum
                    downgrades_count += 1
                    val_proj = max(0, val_mar26 - 0.5)
                    r_proj = num_to_rating(val_proj)
                    proj_indicator = '↓'
                else:
                    # Stable
                    val_proj = val_mar26
                    r_proj = r_mar26
                    proj_indicator = ''
                
                scores_proj26.append(val_proj)
                
                transition_list.append({
                    'Tipo': tipo,
                    'Entidad': entidad,
                    'Agencia': ag,
                    'Sep2025': r_sep25,
                    'Mar2026': r_mar26,
                    'Indicator_Mar26': c_mar26,
                    'Proj_Sep2026': r_proj,
                    'Indicator_Sep26': proj_indicator
                })
            
            # Format SBS output string
            if r_proj != '':
                df_proj_sbs.loc[idx, ag] = f"{r_proj} ({proj_indicator})" if proj_indicator else r_proj
            else:
                df_proj_sbs.loc[idx, ag] = ''

        # Summary for entity
        avg_sep25 = np.mean(scores_sep25) if len(scores_sep25) > 0 else np.nan
        avg_mar26 = np.mean(scores_mar26) if len(scores_mar26) > 0 else np.nan
        avg_proj26 = np.mean(scores_proj26) if len(scores_proj26) > 0 else np.nan
        
        diff_proj_mar = (avg_proj26 - avg_mar26) if (pd.notna(avg_proj26) and pd.notna(avg_mar26)) else 0
        
        if diff_proj_mar > 0.1:
            tendencia = 'Positiva (Mejora)'
        elif diff_proj_mar < -0.1:
            tendencia = 'Negativa (Deterioro)'
        else:
            tendencia = 'Estable'
            
        entity_summary.append({
            'Tipo': tipo,
            'Entidad': entidad,
            'Agencias_Evaluadoras': len(scores_mar26),
            'Score_Sep2025': round(avg_sep25, 2) if pd.notna(avg_sep25) else None,
            'Score_Mar2026': round(avg_mar26, 2) if pd.notna(avg_mar26) else None,
            'Score_Proj_Sep2026': round(avg_proj26, 2) if pd.notna(avg_proj26) else None,
            'Rating_Consenso_Mar2026': num_to_rating(avg_mar26),
            'Rating_Consenso_Proj_Sep2026': num_to_rating(avg_proj26),
            'Categoria_Riesgo_Mar2026': get_risk_level(avg_mar26),
            'Categoria_Riesgo_Proj_Sep2026': get_risk_level(avg_proj26),
            'Tendencia_Proyectada': tendencia,
            'Upgrades_Mar2026': upgrades_count,
            'Downgrades_Mar2026': downgrades_count
        })

    df_summary = pd.DataFrame(entity_summary)
    df_transitions = pd.DataFrame(transition_list)
    
    # Save files
    path_excel = os.path.join('Data', 'septiembre2026_proyeccion.xlsx')
    path_csv_sbs = os.path.join('Data', 'septiembre2026_proyeccion.csv')
    path_csv_summary = os.path.join('Data', 'resumen_entidades_riesgo.csv')
    path_csv_trans = os.path.join('Data', 'transiciones_detalladas.csv')
    
    # Write Excel with multiple sheets
    with pd.ExcelWriter(path_excel, engine='openpyxl') as writer:
        df_proj_sbs.to_excel(writer, sheet_name='Proyeccion_SBS_Sep2026', index=False)
        df_summary.to_excel(writer, sheet_name='Resumen_Riesgo_Entidades', index=False)
        df_transitions.to_excel(writer, sheet_name='Transiciones_Agencias', index=False)
        
    df_proj_sbs.to_csv(path_csv_sbs, index=False, encoding='utf-8-sig')
    df_summary.to_csv(path_csv_summary, index=False, encoding='utf-8-sig')
    df_transitions.to_csv(path_csv_trans, index=False, encoding='utf-8-sig')
    
    print(f"SUCCESS: Saved projection Excel to {path_excel}")
    print(f"SUCCESS: Saved SBS table CSV to {path_csv_sbs}")
    print(f"SUCCESS: Saved entity summary CSV to {path_csv_summary}")
    print(f"SUCCESS: Saved transitions CSV to {path_csv_trans}")
    
    return df_proj_sbs, df_summary, df_transitions

if __name__ == '__main__':
    build_projection()
