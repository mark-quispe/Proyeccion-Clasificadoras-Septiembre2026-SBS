import json
import os

def generate_dashboard():
    # Load JSON data
    with open('Data/dashboard_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    data_js_str = json.dumps(data, ensure_ascii=False)
    
    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>SBS - Clasificaciones e Informes Semestrales Proyectados (Tema Nord)</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    :root {{
      /* Nord Color Palette Theme */
      --nord0: #2e3440; /* polar night main background */
      --nord1: #3b4252; /* polar night card background */
      --nord2: #434c5e; /* polar night elevated */
      --nord3: #4c566a; /* polar night borders / muted text */
      
      --nord4: #d8dee9; /* snow storm default text */
      --nord5: #e5e9f0; /* snow storm lighter text */
      --nord6: #eceff4; /* snow storm brightest */
      
      --nord7: #8fbcbb; /* frost teal */
      --nord8: #88c0d0; /* frost ice blue */
      --nord9: #81a1c1; /* frost medium blue */
      --nord10: #5e81ac; /* frost deep blue */
      
      --nord11: #bf616a; /* aurora red */
      --nord12: #d08770; /* aurora orange */
      --nord13: #ebcb8b; /* aurora yellow */
      --nord14: #a3be8c; /* aurora green */
      --nord15: #b48ead; /* aurora purple */
    }}
    body {{
      background-color: var(--nord0);
      color: var(--nord4);
    }}
    /* Custom scrollbar for Nord theme */
    ::-webkit-scrollbar {{
      width: 8px;
      height: 8px;
    }}
    ::-webkit-scrollbar-track {{
      background: var(--nord0);
    }}
    ::-webkit-scrollbar-thumb {{
      background: var(--nord2);
      border-radius: 4px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
      background: var(--nord3);
    }}
    
    /* Highlight Badges and Column Backgrounds */
    .nord-badge-green {{
      color: var(--nord14) !important;
      background-color: rgba(163, 190, 140, 0.18) !important;
      font-weight: bold;
      padding: 0.15rem 0.4rem;
      border-radius: 0.25rem;
      border: 1px solid rgba(163, 190, 140, 0.35) !important;
    }}
    .nord-badge-red {{
      color: var(--nord11) !important;
      background-color: rgba(191, 97, 106, 0.18) !important;
      font-weight: bold;
      padding: 0.15rem 0.4rem;
      border-radius: 0.25rem;
      border: 1px solid rgba(191, 97, 106, 0.35) !important;
    }}
    .score-green {{
      background-color: rgba(163, 190, 140, 0.12) !important;
      color: var(--nord14) !important;
      font-weight: bold;
      border-left: 1px solid var(--nord2) !important;
    }}
    .score-red {{
      background-color: rgba(191, 97, 106, 0.12) !important;
      color: var(--nord11) !important;
      font-weight: bold;
      border-left: 1px solid var(--nord2) !important;
    }}
  </style>
</head>
<body class="font-sans antialiased min-h-screen">

  <!-- Header -->
  <header class="bg-[var(--nord1)] border-b border-[var(--nord2)] shadow-lg py-4 px-6">
    <div class="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-4">
      <div class="flex items-center gap-4">
        <!-- Mock SBS Logo adapted to Nord Theme -->
        <div class="border-l-4 border-[var(--nord8)] pl-3">
          <div class="text-[10px] font-bold text-[var(--nord4)] tracking-wider">SUPERINTENDENCIA</div>
          <div class="text-sm font-black text-[var(--nord8)] tracking-tight">DE BANCA, SEGUROS Y AFP</div>
          <div class="text-[9px] text-[var(--nord9)]">República del Perú</div>
        </div>
      </div>
      <div class="text-right">
        <h1 class="text-xl font-bold text-[var(--nord6)]">Proyección de Clasificaciones de Riesgo</h1>
        <p class="text-xs text-[var(--nord4)]">Análisis y Estimación para el Cierre Semestral: Septiembre 2026</p>
      </div>
    </div>
  </header>

  <main class="max-w-7xl mx-auto p-4 md:p-6 space-y-6">

    <!-- KPI Metrics Dashboard -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
      <div class="bg-[var(--nord1)] p-4 rounded-xl border border-[var(--nord2)] shadow-md">
        <div class="text-[10px] text-[var(--nord9)] font-bold uppercase tracking-wider">Entidades Supervisadas</div>
        <div class="text-2xl font-bold text-[var(--nord6)] mt-1" id="kpi-total">79</div>
        <div class="text-[11px] text-[var(--nord4)]/70 mt-1">100% de cobertura de datos SBS</div>
      </div>
      <div class="bg-[var(--nord1)] p-4 rounded-xl border border-[var(--nord2)] shadow-md">
        <div class="text-[10px] text-[var(--nord9)] font-bold uppercase tracking-wider">Riesgo Mínimo (A+)</div>
        <div class="text-2xl font-bold text-[var(--nord14)] mt-1" id="kpi-minimo">12</div>
        <div class="text-[11px] text-[var(--nord14)] mt-1 font-medium">Estable a nivel de segmento</div>
      </div>
      <div class="bg-[var(--nord1)] p-4 rounded-xl border border-[var(--nord2)] shadow-md">
        <div class="text-[10px] text-[var(--nord9)] font-bold uppercase tracking-wider">Impulso de Mejora (↑)</div>
        <div class="text-2xl font-bold text-[var(--nord7)] mt-1" id="kpi-upgrades">6</div>
        <div class="text-[11px] text-[var(--nord7)] mt-1 font-medium">Bancos y Cajas con tendencia al alza</div>
      </div>
      <div class="bg-[var(--nord1)] p-4 rounded-xl border border-[var(--nord2)] shadow-md col-span-1">
        <div class="text-[10px] text-[var(--nord9)] font-bold uppercase tracking-wider">Estrés Crítico (D)</div>
        <div class="text-2xl font-bold text-[var(--nord11)] mt-1" id="kpi-critical">1</div>
        <div class="text-[11px] text-[var(--nord11)] mt-1 font-medium">1 Caja Rural bajo vigilancia intensiva</div>
      </div>
    </div>

    <!-- Filters Section (Nord Theme) -->
    <div class="bg-[var(--nord1)] p-6 rounded-xl border border-[var(--nord2)] shadow-md">
      <h2 class="text-[var(--nord8)] font-bold text-xs mb-4 tracking-wide uppercase">Criterios de Búsqueda</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        
        <div>
          <label class="block text-xs font-semibold text-[var(--nord4)] mb-1">Periodo Semestral</label>
          <select id="select-period" class="w-full bg-[var(--nord0)] border border-[var(--nord2)] rounded-lg py-2 px-3 text-sm focus:outline-none focus:border-[var(--nord8)] font-semibold text-[var(--nord5)]">
            <option value="ProjSep2026" selected>2026 - SEPTIEMBRE (Proyectado)</option>
            <option value="Mar2026">2026 - MARZO (Histórico SBS)</option>
            <option value="Sep2025">2025 - SEPTIEMBRE (Histórico SBS)</option>
          </select>
        </div>

        <div>
          <label class="block text-xs font-semibold text-[var(--nord4)] mb-1">Tipo de Entidad</label>
          <select id="select-tipo" class="w-full bg-[var(--nord0)] border border-[var(--nord2)] rounded-lg py-2 px-3 text-sm focus:outline-none focus:border-[var(--nord8)] text-[var(--nord5)]">
            <option value="TODOS">-- TODOS --</option>
            <option value="Banco">Banco</option>
            <option value="Seguros">Seguros</option>
            <option value="Caja Municipal de Ahorro y Crédito">Caja Municipal (CMAC)</option>
            <option value="Caja Rural de Ahorro y Crédito">Caja Rural (CRAC)</option>
            <option value="Financiera">Financiera</option>
            <option value="Cooperativa">Cooperativas</option>
          </select>
        </div>

        <div class="flex items-end">
          <div class="flex gap-2 w-full">
            <input type="text" id="search-entity" placeholder="Buscar entidad..." class="w-full bg-[var(--nord0)] border border-[var(--nord2)] rounded-lg py-2 px-3 text-sm focus:outline-none focus:border-[var(--nord8)] text-[var(--nord5)] placeholder-[var(--nord3)]">
            <button id="btn-clear" class="bg-[var(--nord2)] hover:bg-[var(--nord3)] text-[var(--nord6)] rounded-lg px-4 text-xs font-bold transition">Limpiar</button>
          </div>
        </div>

      </div>
    </div>

    <!-- Table Grid (Nord style) -->
    <div class="bg-[var(--nord1)] rounded-xl border border-[var(--nord2)] shadow-md overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="bg-[var(--nord0)] border-b border-[var(--nord2)] text-[var(--nord5)] text-[11px] uppercase tracking-wider font-bold">
              <th class="py-3.5 px-4 text-[var(--nord8)]">Tipo de Entidad</th>
              <th class="py-3.5 px-4 text-[var(--nord8)]">Entidad</th>
              <th class="py-3.5 px-4 text-center">Apoyo y Asociados</th>
              <th class="py-3.5 px-4 text-center">Class y Asociados</th>
              <th class="py-3.5 px-4 text-center">JCR Latino America</th>
              <th class="py-3.5 px-4 text-center">Microrate</th>
              <th class="py-3.5 px-4 text-center">Moodys Local PE</th>
              <th class="py-3.5 px-4 text-center">PCR (Pacific)</th>
              <th class="py-3.5 px-4 text-center bg-[var(--nord0)] border-l border-[var(--nord2)]">Score Consenso</th>
            </tr>
          </thead>
          <tbody id="table-body" class="divide-y divide-[var(--nord2)] text-xs">
            <!-- Dynamically populated -->
          </tbody>
        </table>
      </div>
      <div class="p-4 bg-[var(--nord0)] border-t border-[var(--nord2)] flex justify-between items-center text-xs text-[var(--nord4)]">
        <div id="table-info">Mostrando 79 de 79 registros</div>
        <div class="flex items-center gap-4">
          <div class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-[var(--nord14)] inline-block"></span> Mejorando (↑)</div>
          <div class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-[var(--nord11)] inline-block"></span> Deterioro (↓)</div>
        </div>
      </div>
    </div>

    <!-- Footer / Autores -->
    <footer class="bg-[var(--nord1)] p-5 rounded-xl border border-[var(--nord2)] shadow-md text-center text-xs">
      <div class="font-bold text-[var(--nord8)] uppercase tracking-wider mb-3">Integrantes del Proyecto</div>
      <div class="flex flex-col md:flex-row justify-center items-center gap-2 md:gap-8 text-[var(--nord5)] font-semibold">
        <span>Mark Quispe Gonzales</span>
        <span class="hidden md:inline text-[var(--nord3)]">|</span>
        <span>Yoshiro Vilchez Cardich</span>
        <span class="hidden md:inline text-[var(--nord3)]">|</span>
        <span>Yunior Yanac Minaya</span>
      </div>
    </footer>

  </main>

  <script>
    const data = {data_js_str};

    const tableBody = document.getElementById('table-body');
    const selectPeriod = document.getElementById('select-period');
    const selectTipo = document.getElementById('select-tipo');
    const searchEntity = document.getElementById('search-entity');
    const btnClear = document.getElementById('btn-clear');
    const tableInfo = document.getElementById('table-info');

    function getTrendColor(val) {{
      if (val.includes('↑')) return 'nord-badge-green';
      if (val.includes('↓')) return 'nord-badge-red';
      return 'text-[var(--nord4)]';
    }}

    function renderTable() {{
      const period = selectPeriod.value;
      const tipoFilter = selectTipo.value;
      const search = searchEntity.value.toLowerCase().trim();

      tableBody.innerHTML = '';
      let visibleCount = 0;

      data.forEach(item => {{
        // Filter by Tipo
        if (tipoFilter !== 'TODOS') {{
          if (tipoFilter === 'Cooperativa') {{
            if (!item.Tipo.includes('Cooperativa')) return;
          }} else if (item.Tipo !== tipoFilter) {{
            return;
          }}
        }}

        // Filter by name
        if (search && !item.Entidad.toLowerCase().includes(search)) return;

        visibleCount++;

        // Get ratings for the chosen period
        let ratings = {{}};
        let score = '';
        let scoreClass = 'bg-[var(--nord0)] font-bold text-[var(--nord5)] border-l border-[var(--nord2)]';

        if (period === 'ProjSep2026') {{
          ratings = item.ProjSep2026;
          score = item.Summary.Score_Proj_Sep2026 ? item.Summary.Score_Proj_Sep2026.toFixed(2) + ' (' + item.Summary.Rating_Consenso_Proj_Sep2026 + ')' : '-';
          if (item.Summary.Tendencia_Proyectada === 'Positiva (Mejora)') {{
            scoreClass = 'score-green';
          }} else if (item.Summary.Tendencia_Proyectada === 'Negativa (Deterioro)') {{
            scoreClass = 'score-red';
          }}
        }} else if (period === 'Mar2026') {{
          ratings = item.Mar2026;
          score = item.Summary.Score_Mar2026 ? item.Summary.Score_Mar2026.toFixed(2) + ' (' + item.Summary.Rating_Consenso_Mar2026 + ')' : '-';
        }} else {{
          ratings = item.Sep2025;
          score = item.Summary.Score_Sep2025 ? item.Summary.Score_Sep2025.toFixed(2) + ' (' + item.Summary.Rating_Consenso_Mar2026 + ')' : '-';
        }}

        const row = document.createElement('tr');
        row.className = 'hover:bg-[var(--nord2)]/30 transition-colors border-b border-[var(--nord2)]';
        
        const agNames = [
          'Apoyo y Asociados Internacionales',
          'Class y Asociados S.A.',
          'JCR Latino America',
          'Microrate',
          'Moodys Local PE Clasificadora de Riesgo',
          'PCR (Pacific Credit Rating)'
        ];

        let cellsHtml = `
          <td class="py-3 px-4 font-semibold text-[var(--nord9)] text-[10px]">${{item.Tipo}}</td>
          <td class="py-3 px-4 font-bold text-[var(--nord5)]">${{item.Entidad}}</td>
        `;

        agNames.forEach(ag => {{
          let val = ratings[ag] || '';
          let change = ratings[ag + '_cambio'] || '';
          
          let disp = val;
          if (period !== 'ProjSep2026' && change) {{
            disp = val + ' ' + change;
          }}

          cellsHtml += `
            <td class="py-3 px-4 text-center">
              <span class="${{getTrendColor(disp)}}">${{disp || '-'}}</span>
            </td>
          `;
        }});

        cellsHtml += `
          <td class="py-3 px-4 text-center ${{scoreClass}}">${{score}}</td>
        `;

        row.innerHTML = cellsHtml;
        tableBody.appendChild(row);
      }});

      tableInfo.textContent = `Mostrando ${{visibleCount}} de ${{data.length}} registros`;
    }}

    // Event listeners
    selectPeriod.addEventListener('change', renderTable);
    selectTipo.addEventListener('change', renderTable);
    searchEntity.addEventListener('input', renderTable);
    btnClear.addEventListener('click', () => {{
      selectTipo.value = 'TODOS';
      searchEntity.value = '';
      selectPeriod.value = 'ProjSep2026';
      renderTable();
    }});

    // Initial render
    renderTable();
  </script>
</body>
</html>
"""
    
    output_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'index.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Dashboard HTML generated successfully at: {output_path}")

if __name__ == '__main__':
    generate_dashboard()
