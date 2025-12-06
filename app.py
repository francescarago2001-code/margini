import streamlit as st
import streamlit.components.v1 as components

# Configura la pagina Streamlit
st.set_page_config(layout="wide", page_title="KPI Dashboard Pro")

# --- CODICE HTML/JS/CSS COMPLETO ---
codice_html_app = """
<!doctype html>
<html lang="it">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>KPI Dashboard Pro</title>

  <script src="https://cdn.tailwindcss.com"></script>

  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">

  <script src="https://cdn.jsdelivr.net/npm/papaparse@5.4.1/papaparse.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/xlsx@0.19.3/dist/xlsx.full.min.js"></script>

  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>

  <style>
    html, body { font-family: Inter, sans-serif; }
    .btn { @apply inline-flex items-center justify-center gap-2 rounded-xl px-4 py-2 text-sm font-semibold transition cursor-pointer; }
    .btn-primary { @apply btn bg-slate-900 text-white hover:bg-slate-800; }
    .btn-ghost { @apply btn bg-white text-slate-700 hover:bg-slate-50 border border-slate-200; }
    .pill { @apply inline-flex items-center gap-2 rounded-full px-3 py-1 text-xs font-semibold; }
    .pill-ok { @apply pill bg-emerald-50 text-emerald-700 border border-emerald-100; }
    .pill-warn { @apply pill bg-amber-50 text-amber-700 border border-amber-100; }
    .card { @apply rounded-2xl bg-white border border-slate-200 p-5 shadow-sm; }
    .input { @apply w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-slate-200; }
    .select { @apply input; }
    
    /* Navigazione */
    .tab-active { @apply bg-slate-900 text-white border-slate-900; }
    .tab-inactive { @apply bg-white text-slate-700 border-slate-200 hover:bg-slate-50; }
  </style>
</head>

<body class="min-h-screen bg-slate-50 text-slate-900 pb-10">

  <div id="app" class="max-w-7xl mx-auto px-4 py-6">
    
    <header class="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between mb-6">
      <div class="flex items-center gap-3">
        <div class="h-10 w-10 rounded-xl bg-slate-900 text-white grid place-items-center font-bold">KM</div>
        <div>
          <div class="text-xl font-bold">KPI Manager</div>
          <div class="text-xs text-slate-500">Dashboard Finanziaria (Excel & CSV)</div>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <span id="planBadge" class="pill-ok">Piano Basic</span>
        <button id="btnResetDemo" class="btn-ghost text-xs">Reset Dati</button>
      </div>
    </header>

    <div class="grid grid-cols-1 lg:grid-cols-[260px_1fr] gap-6">
      
      <aside class="h-fit space-y-4">
        <div class="card">
          <div class="text-xs font-bold text-slate-500 uppercase tracking-wider mb-3">Menu</div>
          
          <div class="mb-3">
            <label class="text-xs text-slate-500">Azienda</label>
            <input id="companyName" class="input mt-1" placeholder="Es. Mario Rossi Srl" />
          </div>

          <div class="h-px bg-slate-100 my-4"></div>

          <nav class="space-y-2">
            <button data-nav="import" class="nav-btn w-full btn-ghost justify-start">📥 Import Dati</button>
            <button data-nav="doctor" class="nav-btn w-full btn-ghost justify-start">🩺 Controllo Qualità</button>
            <button data-nav="kpi" class="nav-btn w-full btn-ghost justify-start">📊 Dashboard KPI</button>
            <button data-nav="margins" class="nav-btn w-full btn-ghost justify-start">💰 Analisi Margini</button>
            <button data-nav="billing" class="nav-btn w-full btn-ghost justify-start">💳 Abbonamento</button>
          </nav>
        </div>

        <div class="card bg-slate-50 border-slate-100">
          <div class="text-xs font-bold text-slate-700">Formati Reali Supportati</div>
          <ul class="mt-2 text-xs text-slate-600 space-y-1">
            <li>✅ Excel (.xlsx, .xls)</li>
            <li>✅ CSV (.csv)</li>
          </ul>
        </div>
      </aside>

      <main class="space-y-6">

        <div class="card flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h2 id="workspaceTitle" class="font-bold text-lg">Benvenuto</h2>
            <p id="workspaceSubtitle" class="text-xs text-slate-500">Carica un file Excel o CSV per vedere i tuoi numeri.</p>
          </div>
          <div class="flex items-center gap-2">
            <span id="dataStatus" class="pill-warn">Nessun dato</span>
          </div>
        </div>

        <section id="view-import" class="view hidden space-y-6">
          <div class="card">
            <h3 class="text-lg font-bold mb-1">Passo 1: Caricamento File</h3>
            <p class="text-xs text-slate-500 mb-4">Trascina qui il tuo file Excel o CSV.</p>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="border-2 border-dashed border-slate-300 rounded-xl p-8 text-center hover:bg-slate-50 transition relative">
                <input id="fileInput" type="file" accept=".csv,.xlsx,.xls" class="absolute inset-0 w-full h-full opacity-0 cursor-pointer" />
                <div class="pointer-events-none">
                  <div class="text-4xl mb-2">📊</div>
                  <div class="font-bold text-slate-700">Clicca o Trascina qui</div>
                  <div class="text-xs text-slate-400 mt-2">Solo file .xlsx, .xls o .csv</div>
                  <div id="fileNameDisplay" class="mt-4 text-sm font-bold text-emerald-600"></div>
                </div>
              </div>

              <div class="bg-slate-50 rounded-xl p-5 border border-slate-100 flex flex-col justify-center">
                <div class="text-sm font-semibold mb-2">Non hai un file pronto?</div>
                <button id="btnQuickSample" class="btn-ghost w-full text-xs">Carica Dati Demo (Automatico)</button>
              </div>
            </div>
            
            <button id="btnParseFile" class="btn-primary w-full mt-6 text-lg py-4">Analizza File</button>
          </div>

          <div id="mappingArea" class="card hidden">
            <h3 class="text-lg font-bold mb-1">Passo 2: Verifica Colonne</h3>
            <p class="text-xs text-slate-500 mb-4">Abbiamo letto il file. Conferma a cosa corrispondono le colonne.</p>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div><label class="text-xs font-bold text-slate-600">Data *</label><select id="mapDate" class="select mt-1"></select></div>
              <div><label class="text-xs font-bold text-slate-600">Prodotto/Servizio *</label><select id="mapProduct" class="select mt-1"></select></div>
              <div><label class="text-xs font-bold text-slate-600">Ricavi *</label><select id="mapRevenue" class="select mt-1"></select></div>
              <div><label class="text-xs font-bold text-slate-600">Costi *</label><select id="mapCost" class="select mt-1"></select></div>
              <div><label class="text-xs font-bold text-slate-600">Cliente</label><select id="mapCustomer" class="select mt-1"></select></div>
            </div>

            <div class="mt-6 flex justify-end gap-2">
              <button id="btnApplyMapping" class="btn-primary">Salva e Elabora</button>
            </div>
          </div>
        </section>

        <section id="view-doctor" class="view hidden space-y-6">
          <div class="card">
            <h3 class="text-lg font-bold">Controllo Qualità Dati</h3>
            <p class="text-xs text-slate-500">Ecco cosa abbiamo trovato nel tuo file.</p>
          </div>
          <div id="doctorStats" class="grid grid-cols-2 lg:grid-cols-4 gap-4"></div>
          <div class="card">
            <h4 class="font-bold text-sm mb-3">Anteprima Dati (Primi 10 - Ordinati per Data)</h4>
            <div class="overflow-x-auto">
              <table class="w-full text-left text-xs">
                <thead class="bg-slate-50 border-b">
                  <tr><th class="p-2">Data</th><th class="p-2">Prodotto</th><th class="p-2">Ricavo</th><th class="p-2">Costo</th><th class="p-2">Margine</th></tr>
                </thead>
                <tbody id="doctorTableBody"></tbody>
              </table>
            </div>
          </div>
        </section>

        <section id="view-kpi" class="view hidden space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4" id="kpiCards"></div>
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div class="card">
              <h4 class="font-bold text-sm mb-4">Andamento Ricavi</h4>
              <canvas id="chartRevenue"></canvas>
            </div>
            <div class="card">
              <h4 class="font-bold text-sm mb-4">Andamento Margini</h4>
              <canvas id="chartMargin"></canvas>
            </div>
          </div>
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div class="card">
              <h4 class="font-bold text-sm mb-4">Top 5 Prodotti</h4>
              <div id="listTopProducts" class="space-y-2"></div>
            </div>
            <div class="card">
              <h4 class="font-bold text-sm mb-4">Top 5 Clienti</h4>
              <div id="listTopCustomers" class="space-y-2"></div>
            </div>
          </div>
        </section>

        <section id="view-margins" class="view hidden space-y-6">
          <div id="paywall" class="card bg-slate-900 text-white text-center py-10 hidden">
            <div class="text-2xl font-bold mb-2">Funzionalità PRO</div>
            <p class="text-slate-300 mb-4">L'analisi avanzata dei margini richiede il piano Pro.</p>
            <button onclick="showView('billing')" class="bg-white text-slate-900 px-6 py-2 rounded-full font-bold hover:bg-slate-100">Vedi Piani</button>
          </div>
          <div id="marginsContent">
             <div class="card border-l-4 border-l-rose-500">
               <h3 class="font-bold text-rose-700">Analisi Criticità</h3>
               <p class="text-xs text-slate-600 mb-4">Prodotti o servizi che ti stanno facendo perdere soldi.</p>
               <div id="marginAlerts" class="space-y-2"></div>
             </div>
             <div class="card mt-6">
               <h3 class="font-bold mb-4">Classifica Margini (Tutti i prodotti)</h3>
               <div id="marginRanking" class="space-y-1"></div>
             </div>
          </div>
        </section>

        <section id="view-billing" class="view hidden space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="card border-2 border-transparent">
              <h3 class="text-xl font-bold">Basic</h3>
              <div class="text-3xl font-bold mt-2">€79<span class="text-sm font-normal text-slate-500">/mese</span></div>
              <ul class="mt-4 space-y-2 text-sm text-slate-600">
                <li>✅ Import Excel/CSV</li>
                <li>✅ Dashboard KPI</li>
                <li>❌ Scanner Margini</li>
              </ul>
              <button id="btnPlanBasic" class="btn-ghost w-full mt-6">Attiva Basic</button>
            </div>
            <div class="card border-2 border-slate-900 relative overflow-hidden">
              <div class="absolute top-0 right-0 bg-slate-900 text-white text-[10px] px-2 py-1 font-bold">CONSIGLIATO</div>
              <h3 class="text-xl font-bold">Pro</h3>
              <div class="text-3xl font-bold mt-2">€199<span class="text-sm font-normal text-slate-500">/mese</span></div>
              <ul class="mt-4 space-y-2 text-sm text-slate-600">
                <li>✅ Tutto il Basic</li>
                <li>✅ Scanner Margini & Alert</li>
                <li>✅ Analisi Clienti</li>
              </ul>
              <button id="btnPlanPro" class="btn-primary w-full mt-6">Attiva Pro</button>
            </div>
          </div>
        </section>

      </main>
    </div>
  </div>

  <script>
    // --- STATO ---
    const state = {
      rawRows: [],
      normRows: [],
      headers: [],
      company: localStorage.getItem("km_company") || "",
      plan: localStorage.getItem("km_plan") || "basic",
      charts: {}
    };

    // --- UTILS ---
    const $ = id => document.getElementById(id);
    const formatMoney = n => new Intl.NumberFormat('it-IT', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 }).format(n);
    
    // --- GESTIONE VISTE ---
    function showView(viewId) {
      document.querySelectorAll('.view').forEach(el => el.classList.add('hidden'));
      document.getElementById('view-' + viewId).classList.remove('hidden');
      
      document.querySelectorAll('.nav-btn').forEach(btn => {
        if(btn.dataset.nav === viewId) {
          btn.classList.remove('btn-ghost');
          btn.classList.add('bg-slate-900', 'text-white', 'rounded-xl'); 
        } else {
          btn.classList.add('btn-ghost');
          btn.classList.remove('bg-slate-900', 'text-white');
        }
      });

      if(viewId === 'doctor') renderDoctor();
      if(viewId === 'kpi') renderKPI();
      if(viewId === 'margins') renderMargins();
    }

    // --- INIT ---
    function init() {
      if(state.company) $('companyName').value = state.company;
      updateUI();
      
      document.querySelectorAll('.nav-btn').forEach(btn => btn.addEventListener('click', () => showView(btn.dataset.nav)));
      $('companyName').addEventListener('input', e => { state.company = e.target.value; localStorage.setItem("km_company", state.company); updateUI(); });
      $('btnPlanBasic').onclick = () => setPlan('basic');
      $('btnPlanPro').onclick = () => setPlan('pro');
      $('btnResetDemo').onclick = () => { localStorage.clear(); location.reload(); };

      // Display Nome File
      $('fileInput').addEventListener('change', (e) => {
        const name = e.target.files[0]?.name;
        if(name) $('fileNameDisplay').textContent = name;
      });

      showView('import');
    }

    function updateUI() {
      $('workspaceTitle').textContent = state.company || "Dashboard Finanziaria";
      $('dataStatus').className = state.normRows.length ? "pill-ok" : "pill-warn";
      $('dataStatus').textContent = state.normRows.length ? `${state.normRows.length} Righe` : "Nessun Dato";
      $('planBadge').textContent = state.plan === 'pro' ? "Piano PRO" : "Piano BASIC";
    }

    function setPlan(plan) {
      state.plan = plan; localStorage.setItem("km_plan", plan);
      updateUI(); alert("Piano " + plan.toUpperCase() + " attivato!");
      if(plan === 'pro') showView('margins');
    }

    // --- MOTORE DI CARICAMENTO REALE ---
    
    // 1. Dati Demo di fallback
    const DEMO_DATA = [
        {date: "2024-01-10", product: "Consulenza Strategica", revenue: 1500, cost: 200, customer: "Alpha Srl"},
        {date: "2024-01-15", product: "Sviluppo Web", revenue: 2500, cost: 500, customer: "Beta Group"},
        {date: "2024-02-05", product: "Campagna Ads (ERR)", revenue: 300, cost: 400, customer: "Gamma SpA"},
        {date: "2024-02-20", product: "Manutenzione", revenue: 1200, cost: 100, customer: "Alpha Srl"},
        {date: "2024-03-01", product: "Licenza Software", revenue: 800, cost: 50, customer: "Delta Co."},
        {date: "2024-03-15", product: "Design Logo", revenue: 600, cost: 50, customer: "Gamma SpA"},
        {date: "2024-04-01", product: "Stampa Brochure", revenue: 200, cost: 250, customer: "Delta Co."},
        {date: "2024-05-01", product: "Video Making", revenue: 3000, cost: 1200, customer: "Beta Group"}
    ];

    $('btnQuickSample').onclick = () => {
        processRawData(DEMO_DATA);
        // Pre-fill mapping per demo
        $('mapDate').value = 'date'; $('mapProduct').value = 'product'; 
        $('mapRevenue').value = 'revenue'; $('mapCost').value = 'cost'; $('mapCustomer').value = 'customer';
    };

    $('btnParseFile').onclick = () => {
      const file = $('fileInput').files[0];
      if(!file) return alert("Seleziona un file Excel o CSV.");

      const ext = file.name.split('.').pop().toLowerCase();
      const reader = new FileReader();

      if(ext === 'csv') {
          reader.onload = (e) => {
              Papa.parse(e.target.result, {
                  header: true, skipEmptyLines: true,
                  complete: (res) => processRawData(res.data)
              });
          };
          reader.readAsText(file);
      } else if(ext === 'xlsx' || ext === 'xls') {
          reader.onload = (e) => {
              const data = new Uint8Array(e.target.result);
              const workbook = XLSX.read(data, {type: 'array'});
              const firstSheet = workbook.SheetNames[0];
              const jsonData = XLSX.utils.sheet_to_json(workbook.Sheets[firstSheet], {defval:""});
              processRawData(jsonData);
          };
          reader.readAsArrayBuffer(file);
      } else {
          alert("Formato non supportato. Usa solo Excel o CSV.");
      }
    };

    function processRawData(data) {
      if(!data || data.length === 0) return alert("File vuoto o illeggibile.");
      state.rawRows = data;
      state.headers = Object.keys(data[0] || {});
      
      const selects = ['mapDate', 'mapProduct', 'mapRevenue', 'mapCost', 'mapCustomer'];
      selects.forEach(id => {
        const el = $(id);
        el.innerHTML = '<option value="">-- Seleziona --</option>';
        state.headers.forEach(h => el.innerHTML += `<option value="${h}">${h}</option>`);
      });

      // Auto-selezione base
      state.headers.forEach(h => {
        const lower = h.toLowerCase();
        if(lower.includes('dat')) $('mapDate').value = h;
        if(lower.includes('prod') || lower.includes('serv') || lower.includes('desc')) $('mapProduct').value = h;
        if(lower.includes('ric') || lower.includes('fatt') || lower.includes('entrat') || lower.includes('rev')) $('mapRevenue').value = h;
        if(lower.includes('cos') || lower.includes('usc')) $('mapCost').value = h;
        if(lower.includes('cli') || lower.includes('rag')) $('mapCustomer').value = h;
      });

      $('mappingArea').classList.remove('hidden');
    }

    $('btnApplyMapping').onclick = applyMapping;

    function applyMapping() {
      const m = {
        date: $('mapDate').value,
        product: $('mapProduct').value,
        revenue: $('mapRevenue').value,
        cost: $('mapCost').value,
        customer: $('mapCustomer').value
      };

      if(!m.date || !m.product || !m.revenue || !m.cost) return alert("Mappa i campi obbligatori (*)");

      // Normalizzazione e Calcoli
      state.normRows = state.rawRows.map(r => ({
        date: normalizeDate(r[m.date]),
        product: r[m.product] || "N/A",
        revenue: parseFloat(r[m.revenue]) || 0,
        cost: parseFloat(r[m.cost]) || 0,
        customer: m.customer ? (r[m.customer] || "Anonimo") : "Anonimo",
        margin: (parseFloat(r[m.revenue]) || 0) - (parseFloat(r[m.cost]) || 0)
      })).filter(r => r.date).sort((a, b) => a.date.localeCompare(b.date));

      updateUI();
      showView('doctor');
    }

    function normalizeDate(val) {
      if(!val) return null;
      if(val instanceof Date) return val.toISOString().split('T')[0];
      const v = String(val).trim();
      // Excel serial date check
      if(!isNaN(v) && v.length > 4 && v.length < 6) { 
         const d = new Date((v - (25567 + 2))*86400*1000); 
         return d.toISOString().split('T')[0]; 
      }
      let d = new Date(v);
      if(!isNaN(d)) return d.toISOString().split('T')[0];
      const parts = v.split(/[\/\-\.]/);
      if(parts.length === 3) return `${parts[2]}-${parts[1].padStart(2,'0')}-${parts[0].padStart(2,'0')}`;
      return null;
    }

    // --- RENDER FUNCTIONS ---
    function renderDoctor() {
      const rows = state.normRows;
      const totalRev = rows.reduce((acc, r) => acc + r.revenue, 0);
      const totalCost = rows.reduce((acc, r) => acc + r.cost, 0);
      
      $('doctorStats').innerHTML = `
        <div class="card bg-slate-50 border-slate-200"><div class="text-xs text-slate-500">Righe Totali</div><div class="text-xl font-bold">${rows.length}</div></div>
        <div class="card bg-emerald-50 border-emerald-100"><div class="text-xs text-emerald-700">Fatturato</div><div class="text-xl font-bold text-emerald-800">${formatMoney(totalRev)}</div></div>
        <div class="card bg-rose-50 border-rose-100"><div class="text-xs text-rose-700">Costi</div><div class="text-xl font-bold text-rose-800">${formatMoney(totalCost)}</div></div>
        <div class="card bg-blue-50 border-blue-100"><div class="text-xs text-blue-700">Periodo</div><div class="text-sm font-bold text-blue-800">${rows.length ? rows[0].date + ' -> ' + rows[rows.length-1].date : '-'}</div></div>
      `;
      $('doctorTableBody').innerHTML = rows.slice(0, 10).map(r => `
        <tr class="border-b hover:bg-slate-50"><td class="p-2">${r.date}</td><td class="p-2 font-medium">${r.product}</td><td class="p-2 text-emerald-600">${formatMoney(r.revenue)}</td><td class="p-2 text-rose-600">${formatMoney(r.cost)}</td><td class="p-2 font-bold">${formatMoney(r.margin)}</td></tr>
      `).join('');
    }

    function renderKPI() {
      if(!state.normRows.length) return;
      const months = {};
      state.normRows.forEach(r => {
        const m = r.date.substring(0, 7);
        if(!months[m]) months[m] = { rev: 0, cost: 0, margin: 0 };
        months[m].rev += r.revenue;
        months[m].cost += r.cost;
        months[m].margin += r.margin;
      });

      const labels = Object.keys(months).sort();
      const dataRev = labels.map(m => months[m].rev);
      const dataMar = labels.map(m => months[m].margin);

      if(state.charts.rev) state.charts.rev.destroy();
      state.charts.rev = new Chart($('chartRevenue'), { type: 'line', data: { labels, datasets: [{ label: 'Fatturato', data: dataRev, borderColor: '#10b981', tension: 0.3 }] } });

      if(state.charts.mar) state.charts.mar.destroy();
      state.charts.mar = new Chart($('chartMargin'), { type: 'bar', data: { labels, datasets: [{ label: 'Margine', data: dataMar, backgroundColor: '#3b82f6' }] } });

      const prodMap = {}; const custMap = {};
      state.normRows.forEach(r => {
        prodMap[r.product] = (prodMap[r.product] || 0) + r.revenue;
        custMap[r.customer] = (custMap[r.customer] || 0) + r.revenue;
      });

      const topProd = Object.entries(prodMap).sort((a,b) => b[1] - a[1]).slice(0, 5);
      const topCust = Object.entries(custMap).sort((a,b) => b[1] - a[1]).slice(0, 5);

      $('listTopProducts').innerHTML = topProd.map((p, i) => `<div class="flex justify-between items-center text-sm border-b pb-1"><span><b>${i+1}.</b> ${p[0]}</span><span class="font-mono">${formatMoney(p[1])}</span></div>`).join('');
      $('listTopCustomers').innerHTML = topCust.map((c, i) => `<div class="flex justify-between items-center text-sm border-b pb-1"><span><b>${i+1}.</b> ${c[0]}</span><span class="font-mono">${formatMoney(c[1])}</span></div>`).join('');
    }

    function renderMargins() {
      if(state.plan !== 'pro') { $('paywall').classList.remove('hidden'); $('marginsContent').classList.add('hidden'); return; }
      $('paywall').classList.add('hidden'); $('marginsContent').classList.remove('hidden');

      const pStats = {};
      state.normRows.forEach(r => {
        if(!pStats[r.product]) pStats[r.product] = { rev: 0, cost: 0, margin: 0 };
        pStats[r.product].rev += r.revenue; pStats[r.product].cost += r.cost; pStats[r.product].margin += r.margin;
      });

      const pArray = Object.entries(pStats).map(([name, s]) => ({ name, ...s, marginPct: s.rev > 0 ? (s.margin / s.rev) : 0 })).sort((a, b) => a.margin - b.margin);
      const alerts = pArray.filter(p => p.margin < 0 || p.marginPct < 0.10);
      
      $('marginAlerts').innerHTML = alerts.length ? alerts.map(p => `
          <div class="flex justify-between items-center bg-rose-50 p-2 rounded border border-rose-100">
            <div><div class="font-bold text-sm text-rose-800">${p.name}</div><div class="text-xs text-rose-600">${p.margin < 0 ? 'IN PERDITA' : 'MARGINE BASSO'} (${(p.marginPct*100).toFixed(1)}%)</div></div>
            <div class="font-bold text-rose-700">${formatMoney(p.margin)}</div>
          </div>`).join('') : '<div class="text-sm text-emerald-600">✅ Nessun prodotto in perdita rilevato.</div>';

      pArray.sort((a, b) => b.margin - a.margin);
      $('marginRanking').innerHTML = pArray.map((p, i) => `
        <div class="flex justify-between items-center p-2 hover:bg-slate-50 rounded text-sm">
           <div class="flex items-center gap-2"><span class="text-slate-400 font-mono text-xs w-4">${i+1}</span><span class="font-medium">${p.name}</span></div>
           <div class="flex gap-4"><span class="text-slate-500 text-xs mt-1">Rev: ${formatMoney(p.rev)}</span><span class="font-bold ${p.margin < 0 ? 'text-rose-600' : 'text-emerald-600'}">${formatMoney(p.margin)}</span></div>
        </div>`).join('');
    }

    init();
  </script>
</body>
</html>
"""

components.html(codice_html_app, height=1200, scrolling=True)
