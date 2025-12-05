<!doctype html>
<html lang="it">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>KPI → Margini | MVP</title>

  <!-- Tailwind (CDN for MVP demo) -->
  <script src="https://cdn.tailwindcss.com"></script>

  <!-- Icons -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">

  <!-- CSV Parser -->
  <script src="https://cdn.jsdelivr.net/npm/papaparse@5.4.1/papaparse.min.js"></script>

  <!-- XLSX Parser (SheetJS) -->
  <script src="https://cdn.jsdelivr.net/npm/xlsx@0.19.3/dist/xlsx.full.min.js"></script>

  <!-- Charts -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>

  <style>
    html, body { font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, sans-serif; }
    .glass {
      background: rgba(255,255,255,0.7);
      backdrop-filter: blur(10px);
    }
    .shadow-soft { box-shadow: 0 10px 30px rgba(0,0,0,0.08); }
    .btn {
      @apply inline-flex items-center justify-center gap-2 rounded-xl px-4 py-2 text-sm font-semibold transition;
    }
    .btn-primary {
      @apply btn bg-slate-900 text-white hover:bg-slate-800;
    }
    .btn-ghost {
      @apply btn bg-white text-slate-700 hover:bg-slate-50 border border-slate-200;
    }
    .pill {
      @apply inline-flex items-center gap-2 rounded-full px-3 py-1 text-xs font-semibold;
    }
    .pill-ok { @apply pill bg-emerald-50 text-emerald-700 border border-emerald-100; }
    .pill-warn { @apply pill bg-amber-50 text-amber-700 border border-amber-100; }
    .pill-bad { @apply pill bg-rose-50 text-rose-700 border border-rose-100; }
    .tab-active {
      @apply bg-slate-900 text-white border-slate-900;
    }
    .tab-inactive {
      @apply bg-white text-slate-700 border-slate-200 hover:bg-slate-50;
    }
    .card {
      @apply rounded-2xl bg-white border border-slate-200 p-5 shadow-soft;
    }
    .small-muted { @apply text-xs text-slate-500; }
    .input {
      @apply w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-slate-200;
    }
    .select {
      @apply input;
    }
    .divider {
      height: 1px; background: linear-gradient(to right, transparent, rgba(0,0,0,0.08), transparent);
    }
  </style>
</head>

<body class="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-100 text-slate-900">
  <!-- ===================== App Shell ===================== -->
  <div id="app" class="max-w-7xl mx-auto px-4 py-6 lg:px-8">
    <!-- Header -->
    <header class="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
      <div class="flex items-center gap-3">
        <div class="h-10 w-10 rounded-2xl bg-slate-900 text-white grid place-items-center font-extrabold">KM</div>
        <div>
          <div class="text-lg font-extrabold tracking-tight">KPI → Margini</div>
          <div class="text-xs text-slate-500">MVP demo client-side • pronto da deploy statico</div>
        </div>
      </div>

      <div class="flex items-center gap-2">
        <span id="planBadge" class="pill-ok">Piano Basic</span>
        <button id="btnResetDemo" class="btn-ghost">Reset demo</button>
      </div>
    </header>

    <!-- Main layout -->
    <div class="mt-6 grid grid-cols-1 lg:grid-cols-[260px_1fr] gap-6">
      <!-- Sidebar -->
      <aside class="card h-fit sticky top-6">
        <div class="text-xs font-bold text-slate-500 uppercase tracking-wider">Workspace</div>

        <div class="mt-3">
          <label class="small-muted">Azienda</label>
          <input id="companyName" class="input mt-1" placeholder="Es. Rossi Srl" />
        </div>

        <div class="mt-3">
          <label class="small-muted">Settore</label>
          <select id="sectorSelect" class="select mt-1">
            <option value="generic">Generico</option>
            <option value="services">Servizi / Consulenza</option>
            <option value="retail">Retail</option>
            <option value="ecommerce">E-commerce</option>
          </select>
        </div>

        <div class="mt-4 divider"></div>

        <div class="mt-4 space-y-2">
          <button data-nav="import" class="nav-btn w-full btn-ghost justify-start">
            <span>📥</span><span>Import dati</span>
          </button>
          <button data-nav="doctor" class="nav-btn w-full btn-ghost justify-start">
            <span>🩺</span><span>Data Doctor</span>
          </button>
          <button data-nav="kpi" class="nav-btn w-full btn-ghost justify-start">
            <span>📊</span><span>Dashboard KPI</span>
          </button>
          <button data-nav="margins" class="nav-btn w-full btn-ghost justify-start">
            <span>💰</span><span>Margin Scanner</span>
          </button>
          <button data-nav="billing" class="nav-btn w-full btn-ghost justify-start">
            <span>🧾</span><span>Billing</span>
          </button>
        </div>

        <div class="mt-6 rounded-xl bg-slate-50 border border-slate-200 p-3">
          <div class="text-xs font-semibold text-slate-700">Formato dati consigliato</div>
          <ul class="mt-2 text-xs text-slate-600 space-y-1">
            <li>• <b>date</b> (YYYY-MM-DD)</li>
            <li>• <b>product</b> o service</li>
            <li>• <b>revenue</b></li>
            <li>• <b>cost</b></li>
            <li>• <b>customer</b (opzionale)</li>
            <li>• <b>channel</b (opzionale)</li>
          </ul>
        </div>
      </aside>

      <!-- Content -->
      <main class="space-y-6">
        <!-- Top status bar -->
        <div class="card">
          <div class="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
            <div>
              <div id="workspaceTitle" class="text-base font-bold">Nessun workspace impostato</div>
              <div id="workspaceSubtitle" class="small-muted">Imposta azienda e settore per iniziare.</div>
            </div>
            <div class="flex items-center gap-2">
              <span id="dataStatus" class="pill-warn">Nessun dataset</span>
              <button id="btnQuickSample" class="btn-ghost">Carica dataset demo</button>
            </div>
          </div>
        </div>

        <!-- ============ VIEW: IMPORT ============ -->
        <section id="view-import" class="view card hidden">
          <div class="flex items-center justify-between">
            <div>
              <div class="text-lg font-extrabold">Import dati</div>
              <div class="small-muted">Carica CSV o Excel. Poi mappa le colonne principali.</div>
            </div>
            <span class="pill-ok">Step 1</span>
          </div>

          <div class="mt-5 grid grid-cols-1 lg:grid-cols-2 gap-4">
            <div class="rounded-2xl border border-dashed border-slate-300 p-5">
              <div class="text-sm font-semibold">Upload file</div>
              <div class="small-muted mt-1">Supporta .csv, .xlsx, .xls</div>
              <input id="fileInput" type="file" accept=".csv,.xlsx,.xls" class="mt-3 block w-full text-sm" />
              <button id="btnParseFile" class="btn-primary mt-3">Analizza file</button>
            </div>

            <div class="rounded-2xl bg-slate-50 border border-slate-200 p-5">
              <div class="text-sm font-semibold">Oppure usa un esempio rapido</div>
              <div class="small-muted mt-1">Utile per demo commerciale.</div>
              <button id="btnLoadSample2" class="btn-ghost mt-3">Importa CSV di esempio</button>

              <div class="mt-4 text-xs text-slate-600">
                Il dataset demo contiene: date, product, revenue, cost, customer, channel.
              </div>
            </div>
          </div>

          <div id="importPreviewWrap" class="mt-6 hidden">
            <div class="divider my-6"></div>
            <div class="flex items-center justify-between">
              <div>
                <div class="text-base font-bold">Anteprima intestazioni & mapping</div>
                <div class="small-muted">Seleziona le colonne corrette.</div>
              </div>
              <span class="pill-warn">Step 2</span>
            </div>

            <div class="mt-4 grid grid-cols-1 lg:grid-cols-3 gap-4">
              <div>
                <label class="small-muted">Colonna data</label>
                <select id="mapDate" class="select mt-1"></select>
              </div>
              <div>
                <label class="small-muted">Colonna prodotto/servizio</label>
                <select id="mapProduct" class="select mt-1"></select>
              </div>
              <div>
                <label class="small-muted">Colonna ricavi</label>
                <select id="mapRevenue" class="select mt-1"></select>
              </div>
              <div>
                <label class="small-muted">Colonna costi</label>
                <select id="mapCost" class="select mt-1"></select>
              </div>
              <div>
                <label class="small-muted">Colonna cliente (opzionale)</label>
                <select id="mapCustomer" class="select mt-1"></select>
              </div>
              <div>
                <label class="small-muted">Colonna canale (opzionale)</label>
                <select id="mapChannel" class="select mt-1"></select>
              </div>
            </div>

            <div class="mt-5 flex flex-wrap gap-2">
              <button id="btnApplyMapping" class="btn-primary">Conferma e salva dataset</button>
              <button id="btnClearImport" class="btn-ghost">Annulla</button>
            </div>

            <div id="importTinyTable" class="mt-5 overflow-auto rounded-xl border border-slate-200"></div>
          </div>
        </section>

        <!-- ============ VIEW: DOCTOR ============ -->
        <section id="view-doctor" class="view card hidden">
          <div class="flex items-center justify-between">
            <div>
              <div class="text-lg font-extrabold">Data Doctor</div>
              <div class="small-muted">Controllo qualità automatico su duplicati, mancanti, date e outlier.</div>
            </div>
            <span class="pill-ok">MVP</span>
          </div>

          <div id="doctorEmpty" class="mt-6 rounded-2xl bg-slate-50 border border-slate-200 p-6">
            <div class="text-sm font-semibold">Nessun dataset caricato</div>
            <div class="small-muted mt-1">Vai su “Import dati” per iniziare.</div>
          </div>

          <div id="doctorContent" class="mt-6 hidden">
            <div class="grid grid-cols-1 lg:grid-cols-4 gap-4">
              <div class="card">
                <div class="small-muted">Righe totali</div>
                <div id="statRows" class="text-2xl font-extrabold mt-1">-</div>
              </div>
              <div class="card">
                <div class="small-muted">Duplicati potenziali</div>
                <div id="statDup" class="text-2xl font-extrabold mt-1">-</div>
              </div>
              <div class="card">
                <div class="small-muted">Valori mancanti (critici)</div>
                <div id="statMissing" class="text-2xl font-extrabold mt-1">-</div>
              </div>
              <div class="card">
                <div class="small-muted">Outlier ricavi/costi</div>
                <div id="statOutliers" class="text-2xl font-extrabold mt-1">-</div>
              </div>
            </div>

            <div class="divider my-6"></div>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div class="card">
                <div class="text-sm font-bold">Problemi trovati</div>
                <ul id="doctorIssues" class="mt-3 text-sm text-slate-700 space-y-2"></ul>
              </div>

              <div class="card">
                <div class="text-sm font-bold">Azioni rapide (demo)</div>
                <div class="small-muted mt-1">In questa versione MVP demo le correzioni sono simulate.</div>
                <div class="mt-3 flex flex-wrap gap-2">
                  <button id="btnSimFixMissing" class="btn-ghost">Simula fix mancanti</button>
                  <button id="btnSimRemoveDup" class="btn-ghost">Simula rimozione duplicati</button>
                  <button id="btnSimClampOutliers" class="btn-ghost">Simula normalizzazione outlier</button>
                </div>
                <div id="doctorActionMsg" class="mt-3 text-xs text-slate-600"></div>
              </div>
            </div>

            <div class="mt-6 card">
              <div class="text-sm font-bold">Anteprima dataset normalizzato</div>
              <div class="small-muted mt-1">Visualizza le prime 20 righe dopo mapping.</div>
              <div id="doctorTable" class="mt-3 overflow-auto rounded-xl border border-slate-200"></div>
            </div>
          </div>
        </section>

        <!-- ============ VIEW: KPI ============ -->
        <section id="view-kpi" class="view card hidden">
          <div class="flex items-center justify-between">
            <div>
              <div class="text-lg font-extrabold">Dashboard KPI</div>
              <div class="small-muted">Template automatici per settore + indicatori chiave.</div>
            </div>
            <span class="pill-ok">Piano Basic</span>
          </div>

          <div id="kpiEmpty" class="mt-6 rounded-2xl bg-slate-50 border border-slate-200 p-6">
            <div class="text-sm font-semibold">Nessun dataset caricato</div>
            <div class="small-muted mt-1">Importa un file per vedere i KPI.</div>
          </div>

          <div id="kpiContent" class="mt-6 hidden">
            <div class="grid grid-cols-1 lg:grid-cols-4 gap-4">
              <div class="card">
                <div class="small-muted">Fatturato totale</div>
                <div id="kpiRevenue" class="text-2xl font-extrabold mt-1">-</div>
              </div>
              <div class="card">
                <div class="small-muted">Costi totali</div>
                <div id="kpiCost" class="text-2xl font-extrabold mt-1">-</div>
              </div>
              <div class="card">
                <div class="small-muted">Margine lordo</div>
                <div id="kpiGross" class="text-2xl font-extrabold mt-1">-</div>
              </div>
              <div class="card">
                <div class="small-muted">Margine %</div>
                <div id="kpiGrossPct" class="text-2xl font-extrabold mt-1">-</div>
              </div>
            </div>

            <div class="divider my-6"></div>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div class="card">
                <div class="text-sm font-bold">Trend ricavi mensili</div>
                <canvas id="chartRevenue" height="140"></canvas>
              </div>
              <div class="card">
                <div class="text-sm font-bold">Trend margine mensile</div>
                <canvas id="chartMargin" height="140"></canvas>
              </div>
            </div>

            <div class="mt-6 grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div class="card">
                <div class="text-sm font-bold">Top prodotti/servizi per ricavi</div>
                <div id="topProducts" class="mt-3"></div>
              </div>
              <div class="card">
                <div class="text-sm font-bold">Top clienti (se presenti)</div>
                <div id="topCustomers" class="mt-3"></div>
              </div>
            </div>
          </div>
        </section>

        <!-- ============ VIEW: MARGINS ============ -->
        <section id="view-margins" class="view card hidden">
          <div class="flex items-center justify-between">
            <div>
              <div class="text-lg font-extrabold">Margin Scanner</div>
              <div class="small-muted">Analisi margini per prodotto/cliente + alert “buchi di profitto”.</div>
            </div>
            <span id="marginsPlanPill" class="pill-warn">Richiede Pro</span>
          </div>

          <div id="marginsEmpty" class="mt-6 rounded-2xl bg-slate-50 border border-slate-200 p-6">
            <div class="text-sm font-semibold">Nessun dataset caricato</div>
            <div class="small-muted mt-1">Importa un file per analizzare i margini.</div>
          </div>

          <!-- Paywall -->
          <div id="marginsPaywall" class="mt-6 hidden">
            <div class="rounded-2xl border border-slate-200 bg-gradient-to-br from-white to-slate-50 p-6">
              <div class="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
                <div>
                  <div class="text-base font-extrabold">Sblocca Margin Scanner</div>
                  <div class="small-muted mt-1">
                    Questa demo mostra il paywall. Vai su Billing e attiva Pro per vedere l’analisi.
                  </div>
                </div>
                <button id="btnGoBillingFromPaywall" class="btn-primary">Vai a Billing</button>
              </div>
            </div>
          </div>

          <div id="marginsContent" class="mt-6 hidden">
            <div class="grid grid-cols-1 lg:grid-cols-4 gap-4">
              <div class="card">
                <div class="small-muted">Prodotti analizzati</div>
                <div id="mStatProducts" class="text-2xl font-extrabold mt-1">-</div>
              </div>
              <div class="card">
                <div class="small-muted">Margine totale</div>
                <div id="mStatGross" class="text-2xl font-extrabold mt-1">-</div>
              </div>
              <div class="card">
                <div class="small-muted">Peggiori 10 per margine</div>
                <div id="mStatWorst" class="text-2xl font-extrabold mt-1">-</div>
              </div>
              <div class="card">
                <div class="small-muted">Alert attivi</div>
                <div id="mStatAlerts" class="text-2xl font-extrabold mt-1">-</div>
              </div>
            </div>

            <div class="divider my-6"></div>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div class="card">
                <div class="text-sm font-bold">Top 10 prodotti per margine €</div>
                <div id="mTopProducts" class="mt-3"></div>
              </div>

              <div class="card">
                <div class="text-sm font-bold">Bottom 10 “buchi di margine”</div>
                <div id="mWorstProducts" class="mt-3"></div>
              </div>
            </div>

            <div class="mt-6 card">
              <div class="text-sm font-bold">Alert diagnostici</div>
              <div id="mAlertsList" class="mt-3 text-sm text-slate-700 space-y-2"></div>
            </div>
          </div>
        </section>

        <!-- ============ VIEW: BILLING ============ -->
        <section id="view-billing" class="view card hidden">
          <div class="flex items-center justify-between">
            <div>
              <div class="text-lg font-extrabold">Billing (demo)</div>
              <div class="small-muted">Toggle semplice piano Basic/Pro per simulare l’abbonamento.</div>
            </div>
            <span class="pill-ok">Demo commerciale</span>
          </div>

          <div class="mt-6 grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div class="card">
              <div class="text-base font-extrabold">Piano Basic</div>
              <div class="small-muted mt-1">KPI automatici + report base</div>
              <ul class="mt-3 text-sm text-slate-700 space-y-1">
                <li>• Import CSV/XLSX</li>
                <li>• Mapping guidato</li>
                <li>• Data Doctor base</li>
                <li>• Dashboard KPI</li>
              </ul>
              <div class="mt-4 flex items-center justify-between">
                <div class="text-2xl font-extrabold">€ 79<span class="text-sm font-semibold text-slate-500">/mese</span></div>
                <button id="btnSetBasic" class="btn-ghost">Attiva Basic</button>
              </div>
            </div>

            <div class="card border-slate-900">
              <div class="flex items-center gap-2">
                <div class="text-base font-extrabold">Piano Pro</div>
                <span class="pill-ok">Consigliato</span>
              </div>
              <div class="small-muted mt-1">Tutto il Basic + Margin Scanner</div>
              <ul class="mt-3 text-sm text-slate-700 space-y-1">
                <li>• Margine per prodotto/cliente</li>
                <li>• Top/Bottom margini</li>
                <li>• Alert “buchi di profitto”</li>
                <li>• Trend margini</li>
              </ul>
              <div class="mt-4 flex items-center justify-between">
                <div class="text-2xl font-extrabold">€ 199<span class="text-sm font-semibold text-slate-500">/mese</span></div>
                <button id="btnSetPro" class="btn-primary">Attiva Pro</button>
              </div>
            </div>
          </div>

          <div class="mt-6 rounded-2xl bg-slate-50 border border-slate-200 p-5">
            <div class="text-sm font-semibold">Nota</div>
            <div class="small-muted mt-1">
              In versione SaaS reale qui collegheremo Stripe Subscription + gestione utenti.
            </div>
          </div>
        </section>

      </main>
    </div>
  </div>

  <!-- ===================== Logic ===================== -->
  <script>
    /***********************
     * Simple State (LocalStorage)
     ***********************/
    const LS = {
      company: "km_company",
      sector: "km_sector",
      plan: "km_plan",
      datasetRaw: "km_dataset_raw",
      mapping: "km_mapping",
      datasetNorm: "km_dataset_norm"
    };

    const state = {
      company: localStorage.getItem(LS.company) || "",
      sector: localStorage.getItem(LS.sector) || "generic",
      plan: localStorage.getItem(LS.plan) || "basic", // basic | pro
      rawRows: loadJSON(LS.datasetRaw, []),
      mapping: loadJSON(LS.mapping, null),
      normRows: loadJSON(LS.datasetNorm, []),
      lastImportHeaders: [],
      charts: {}
    };

    function loadJSON(key, fallback) {
      try {
        const v = localStorage.getItem(key);
        return v ? JSON.parse(v) : fallback;
      } catch {
        return fallback;
      }
    }
    function saveJSON(key, value) {
      localStorage.setItem(key, JSON.stringify(value));
    }

    /***********************
     * DOM Helpers
     ***********************/
    const $ = (id) => document.getElementById(id);

    const views = ["import", "doctor", "kpi", "margins", "billing"];
    function showView(name) {
      views.forEach(v => {
        const el = $("view-" + v);
        if (!el) return;
        el.classList.toggle("hidden", v !== name);
      });
      document.querySelectorAll(".nav-btn").forEach(btn => {
        const active = btn.dataset.nav === name;
        btn.classList.remove("tab-active","tab-inactive");
        btn.classList.add(active ? "tab-active" : "tab-inactive");
      });

      // refresh view-specific UI
      if (name === "doctor") renderDoctor();
      if (name === "kpi") renderKPI();
      if (name === "margins") renderMargins();
      if (name === "billing") renderPlanBadge();
      if (name === "import") renderImportPreviewTable();
    }

    function money(n) {
      if (!isFinite(n)) return "-";
      return new Intl.NumberFormat("it-IT", { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n);
    }
    function pct(n) {
      if (!isFinite(n)) return "-";
      return new Intl.NumberFormat("it-IT", { style: "percent", maximumFractionDigits: 1 }).format(n);
    }

    /***********************
     * Workspace UI
     ***********************/
    function syncWorkspaceUI() {
      $("companyName").value = state.company;
      $("sectorSelect").value = state.sector;
      $("workspaceTitle").textContent = state.company ? `${state.company}` : "Nessun workspace impostato";
      const sectorLabel = {
        generic: "Generico",
        services: "Servizi / Consulenza",
        retail: "Retail",
        ecommerce: "E-commerce"
      }[state.sector] || "Generico";
      $("workspaceSubtitle").textContent = state.company
        ? `Settore: ${sectorLabel} • Piano: ${state.plan.toUpperCase()}`
        : "Imposta azienda e settore per iniziare.";

      $("dataStatus").className = state.normRows?.length ? "pill-ok" : "pill-warn";
      $("dataStatus").textContent = state.normRows?.length ? `Dataset attivo (${state.normRows.length} righe)` : "Nessun dataset";
      renderPlanBadge();
    }

    function renderPlanBadge() {
      const badge = $("planBadge");
      if (state.plan === "pro") {
        badge.className = "pill-ok";
        badge.textContent = "Piano Pro";
      } else {
        badge.className = "pill-ok";
        badge.textContent = "Piano Basic";
      }
    }

    $("companyName").addEventListener("input", (e) => {
      state.company = e.target.value.trim();
      localStorage.setItem(LS.company, state.company);
      syncWorkspaceUI();
    });
    $("sectorSelect").addEventListener("change", (e) => {
      state.sector = e.target.value;
      localStorage.setItem(LS.sector, state.sector);
      syncWorkspaceUI();
      // refresh KPI with template hints
      renderKPI();
    });

    $("btnResetDemo").addEventListener("click", () => {
      Object.values(LS).forEach(k => localStorage.removeItem(k));
      location.reload();
    });

    /***********************
     * Navigation
     ***********************/
    document.querySelectorAll(".nav-btn").forEach(btn => {
      btn.classList.add("tab-inactive");
      btn.addEventListener("click", () => showView(btn.dataset.nav));
    });

    /***********************
     * Sample Dataset
     ***********************/
    const SAMPLE_CSV = `date,product,revenue,cost,customer,channel
2025-01-03,Prodotto A,1200,700,Cliente 1,Online
2025-01-10,Prodotto A,1100,680,Cliente 2,Online
2025-01-15,Prodotto B,900,950,Cliente 3,Retail
2025-01-20,Prodotto C,1500,600,Cliente 1,Online
2025-02-05,Prodotto A,1300,720,Cliente 4,Retail
2025-02-11,Prodotto B,800,840,Cliente 5,Online
2025-02-18,Prodotto D,500,200,Cliente 6,Retail
2025-03-02,Prodotto C,1600,650,Cliente 2,Online
2025-03-10,Prodotto E,400,500,Cliente 7,Online
2025-03-18,Prodotto A,1250,710,Cliente 8,Retail
2025-03-22,Prodotto D,520,210,Cliente 6,Retail
2025-04-05,Prodotto C,1700,660,Cliente 9,Online
2025-04-12,Prodotto B,950,980,Cliente 3,Retail
2025-04-20,Prodotto F,300,100,Cliente 10,Online
2025-04-25,Prodotto A,1400,740,Cliente 1,Online
2025-05-02,Prodotto C,1800,690,Cliente 2,Online
2025-05-10,Prodotto E,380,520,Cliente 7,Online
2025-05-18,Prodotto G,2200,1200,Cliente 11,Retail
2025-05-22,Prodotto H,250,260,Cliente 12,Online
2025-06-01,Prodotto A,1500,760,Cliente 13,Retail`;

    $("btnQuickSample").addEventListener("click", () => {
      loadSampleCSV();
      showView("doctor");
    });
    $("btnLoadSample2").addEventListener("click", () => {
      loadSampleCSV();
      renderImportPreviewTable();
    });

    function loadSampleCSV() {
      const parsed = Papa.parse(SAMPLE_CSV, { header: true, skipEmptyLines: true });
      state.rawRows = parsed.data;
      state.lastImportHeaders = parsed.meta.fields || Object.keys(state.rawRows[0] || {});
      saveJSON(LS.datasetRaw, state.rawRows);
      // auto mapping for sample
      state.mapping = {
        date: "date",
        product: "product",
        revenue: "revenue",
        cost: "cost",
        customer: "customer",
        channel: "channel"
      };
      saveJSON(LS.mapping, state.mapping);
      normalizeDataset();
      syncWorkspaceUI();
      prepareMappingSelects();
      $("importPreviewWrap").classList.remove("hidden");
      renderImportPreviewTable();
    }

    /***********************
     * File Parsing
     ***********************/
    $("btnParseFile").addEventListener("click", async () => {
      const file = $("fileInput").files?.[0];
      if (!file) {
        alert("Seleziona un file CSV o Excel.");
        return;
      }
      const ext = file.name.split(".").pop().toLowerCase();

      try {
        if (ext === "csv") {
          const text = await file.text();
          const parsed = Papa.parse(text, { header: true, skipEmptyLines: true });
          state.rawRows = parsed.data;
          state.lastImportHeaders = parsed.meta.fields || Object.keys(state.rawRows[0] || {});
        } else if (ext === "xlsx" || ext === "xls") {
          const data = await file.arrayBuffer();
          const wb = XLSX.read(data, { type: "array" });
          const wsName = wb.SheetNames[0];
          const ws = wb.Sheets[wsName];
          const json = XLSX.utils.sheet_to_json(ws, { defval: "" });
          state.rawRows = json;
          state.lastImportHeaders = Object.keys(json[0] || {});
        } else {
          alert("Formato non supportato.");
          return;
        }

        saveJSON(LS.datasetRaw, state.rawRows);
        prepareMappingSelects();
        $("importPreviewWrap").classList.remove("hidden");
        renderImportPreviewTable();
        syncWorkspaceUI();
      } catch (err) {
        console.error(err);
        alert("Errore nella lettura del file.");
      }
    });

    $("btnClearImport").addEventListener("click", () => {
      $("importPreviewWrap").classList.add("hidden");
      state.lastImportHeaders = [];
      renderImportPreviewTable();
    });

    function prepareMappingSelects() {
      const headers = state.lastImportHeaders.length
        ? state.lastImportHeaders
        : Object.keys(state.rawRows[0] || {});

      const selects = [
        $("mapDate"), $("mapProduct"), $("mapRevenue"),
        $("mapCost"), $("mapCustomer"), $("mapChannel")
      ];
      selects.forEach(sel => {
        sel.innerHTML = "";
        const optEmpty = document.createElement("option");
        optEmpty.value = "";
        optEmpty.textContent = "— seleziona —";
        sel.appendChild(optEmpty);

        headers.forEach(h => {
          const o = document.createElement("option");
          o.value = h; o.textContent = h;
          sel.appendChild(o);
        });
      });

      // naive auto-suggest
      const lowerMap = headers.reduce((acc, h) => (acc[h.toLowerCase()] = h, acc), {});
      const guess = (keys) => keys.find(k => lowerMap[k]) ? lowerMap[keys.find(k => lowerMap[k])] : "";

      $("mapDate").value = guess(["date","data","giorno"]);
      $("mapProduct").value = guess(["product","prodotto","service","servizio","sku","item"]);
      $("mapRevenue").value = guess(["revenue","ricavi","fatturato","sales"]);
      $("mapCost").value = guess(["cost","costi","costo"]);
      $("mapCustomer").value = guess(["customer","cliente","client"]);
      $("mapChannel").value = guess(["channel","canale"]);
    }

    $("btnApplyMapping").addEventListener("click", () => {
      const m = {
        date: $("mapDate").value,
        product: $("mapProduct").value,
        revenue: $("mapRevenue").value,
        cost: $("mapCost").value,
        customer: $("mapCustomer").value,
        channel: $("mapChannel").value
      };

      if (!m.date || !m.product || !m.revenue || !m.cost) {
        alert("Mappa almeno: data, prodotto/servizio, ricavi, costi.");
        return;
      }
      state.mapping = m;
      saveJSON(LS.mapping, m);
      normalizeDataset();
      syncWorkspaceUI();
      alert("Dataset salvato e normalizzato.");
      showView("doctor");
    });

    function normalizeDataset() {
      const m = state.mapping;
      if (!m || !state.rawRows?.length) {
        state.normRows = [];
        saveJSON(LS.datasetNorm, state.normRows);
        return;
      }

      const norm = state.rawRows.map((r, idx) => {
        const dateRaw = r[m.date];
        const date = normalizeDate(dateRaw);
        const revenue = toNumber(r[m.revenue]);
        const cost = toNumber(r[m.cost]);
        const product = (r[m.product] ?? "").toString().trim();
        const customer = m.customer ? (r[m.customer] ?? "").toString().trim() : "";
        const channel = m.channel ? (r[m.channel] ?? "").toString().trim() : "";

        return {
          _row: idx + 1,
          date,
          product,
          revenue,
          cost,
          customer,
          channel,
          gross: isFinite(revenue) && isFinite(cost) ? (revenue - cost) : NaN
        };
      });

      state.normRows = norm;
      saveJSON(LS.datasetNorm, norm);
    }

    function normalizeDate(v) {
      if (v instanceof Date && !isNaN(v)) return v.toISOString().slice(0,10);
      const s = (v ?? "").toString().trim();
      if (!s) return "";
      // Try ISO first
      const d1 = new Date(s);
      if (!isNaN(d1)) return d1.toISOString().slice(0,10);

      // Try DD/MM/YYYY
      const m = s.match(/^(\d{1,2})[\/\-\.](\d{1,2})[\/\-\.](\d{2,4})$/);
      if (m) {
        let dd = parseInt(m[1],10), mm = parseInt(m[2],10), yy = parseInt(m[3],10);
        if (yy < 100) yy += 2000;
        const d = new Date(Date.UTC(yy, mm-1, dd));
        if (!isNaN(d)) return d.toISOString().slice(0,10);
      }
      return "";
    }

    function toNumber(v) {
      if (typeof v === "number") return v;
      const s = (v ?? "").toString().replace(/\s/g,"").replace(/\./g,"").replace(",",".");
      const n = parseFloat(s);
      return isFinite(n) ? n : NaN;
    }

    /***********************
     * Import Preview Small Table
     ***********************/
    function renderImportPreviewTable() {
      const wrap = $("importTinyTable");
      if (!wrap) return;
      const rows = state.rawRows?.slice(0, 8) || [];
      if (!rows.length) {
        wrap.innerHTML = "<div class='p-3 text-xs text-slate-500'>Nessuna anteprima disponibile.</div>";
        return;
      }
      const headers = Object.keys(rows[0] || {});
      wrap.innerHTML = buildTableHTML(headers, rows);
    }

    function buildTableHTML(headers, rows) {
      const head = headers.map(h => `<th class="text-left px-3 py-2 text-xs font-semibold text-slate-600 border-b">${escapeHTML(h)}</th>`).join("");
      const body = rows.map(r => {
        const tds = headers.map(h => `<td class="px-3 py-2 text-xs text-slate-700 border-b">${escapeHTML(r[h] ?? "")}</td>`).join("");
        return `<tr>${tds}</tr>`;
      }).join("");

      return `
        <table class="min-w-full bg-white">
          <thead><tr>${head}</tr></thead>
          <tbody>${body}</tbody>
        </table>
      `;
    }

    function escapeHTML(s) {
      return (s ?? "").toString()
        .replace(/&/g,"&amp;")
        .replace(/</g,"&lt;")
        .replace(/>/g,"&gt;")
        .replace(/"/g,"&quot;")
        .replace(/'/g,"&#039;");
    }

    /***********************
     * Data Doctor
     ***********************/
    function renderDoctor() {
      const hasData = state.normRows?.length > 0;
      $("doctorEmpty").classList.toggle("hidden", hasData);
      $("doctorContent").classList.toggle("hidden", !hasData);

      if (!hasData) return;

      const rows = state.normRows;
      $("statRows").textContent = rows.length;

      // duplicates by key date+product+revenue+cost
      const keyCount = new Map();
      rows.forEach(r => {
        const key = [r.date, r.product, r.revenue, r.cost].join("||");
        keyCount.set(key, (keyCount.get(key) || 0) + 1);
      });
      let dup = 0;
      keyCount.forEach(c => { if (c > 1) dup += (c - 1); });
      $("statDup").textContent = dup;

      // missing critical
      const missing = rows.filter(r => !r.date || !r.product || !isFinite(r.revenue) || !isFinite(r.cost)).length;
      $("statMissing").textContent = missing;

      // outliers simple z-score-ish using median absolute deviation on revenue+cost separately
      const outRevenue = detectOutliers(rows.map(r => r.revenue));
      const outCost = detectOutliers(rows.map(r => r.cost));
      const outCount = Math.max(outRevenue.size, outCost.size);
      $("statOutliers").textContent = outCount;

      // issues list
      const issues = [];
      if (missing) issues.push({ type: "warn", text: `${missing} righe con campi critici mancanti o non numerici.` });
      if (dup) issues.push({ type: "warn", text: `${dup} duplicati potenziali basati su data+prodotto+ricavo+costo.` });
      if (outCount) issues.push({ type: "warn", text: `Possibili outlier su ricavi/costi. Controllo consigliato.` });
      if (!missing && !dup && !outCount) issues.push({ type: "ok", text: "Dataset pulito secondo i controlli base dell’MVP." });

      $("doctorIssues").innerHTML = issues.map(i => `
        <li class="flex items-start gap-2">
          <span class="${i.type === "ok" ? "pill-ok" : "pill-warn"}">${i.type === "ok" ? "OK" : "ATTENZIONE"}</span>
          <span>${escapeHTML(i.text)}</span>
        </li>
      `).join("");

      // table preview
      $("doctorTable").innerHTML = buildNormPreviewTable(rows);

      // action buttons (demo)
      $("doctorActionMsg").textContent = "";
      $("btnSimFixMissing").onclick = () => $("doctorActionMsg").textContent =
        "Simulazione: valori mancanti riempiti dove possibile. (Nella versione SaaS reale applicheremo regole di imputazione.)";
      $("btnSimRemoveDup").onclick = () => $("doctorActionMsg").textContent =
        "Simulazione: duplicati consolidati. (Nella versione SaaS reale potrai approvare la rimozione.)";
      $("btnSimClampOutliers").onclick = () => $("doctorActionMsg").textContent =
        "Simulazione: outlier normalizzati. (Nella versione SaaS reale useremo soglie configurabili.)";
    }

    function buildNormPreviewTable(rows) {
      const slice = rows.slice(0, 20);
      const headers = ["_row","date","product","revenue","cost","gross","customer","channel"];
      const head = headers.map(h => `<th class="text-left px-3 py-2 text-xs font-semibold text-slate-600 border-b">${escapeHTML(h)}</th>`).join("");
      const body = slice.map(r => {
        const cells = headers.map(h => {
          let val = r[h] ?? "";
          if (h === "revenue" || h === "cost" || h === "gross") {
            val = isFinite(val) ? Math.round(val) : "";
          }
          return `<td class="px-3 py-2 text-xs text-slate-700 border-b">${escapeHTML(val)}</td>`;
        }).join("");
        return `<tr>${cells}</tr>`;
      }).join("");

      return `
        <table class="min-w-full bg-white">
          <thead><tr>${head}</tr></thead>
          <tbody>${body}</tbody>
        </table>
      `;
    }

    function detectOutliers(values) {
      const nums = values.filter(v => isFinite(v));
      if (nums.length < 8) return new Set();
      const sorted = [...nums].sort((a,b)=>a-b);
      const median = sorted[Math.floor(sorted.length/2)];
      const absDevs = sorted.map(v => Math.abs(v - median)).sort((a,b)=>a-b);
      const mad = absDevs[Math.floor(absDevs.length/2)] || 0;
      const threshold = mad === 0 ? 0 : 3 * mad; // simple robust rule

      const idxs = new Set();
      values.forEach((v, i) => {
        if (!isFinite(v)) return;
        if (threshold > 0 && Math.abs(v - median) > threshold) idxs.add(i);
      });
      return idxs;
    }

    /***********************
     * KPI Dashboard
     ***********************/
    function renderKPI() {
      const hasData = state.normRows?.length > 0;
      $("kpiEmpty").classList.toggle("hidden", hasData);
      $("kpiContent").classList.toggle("hidden", !hasData);
      if (!hasData) return;

      const rows = state.normRows;
      const revenueTotal = sum(rows, r => r.revenue);
      const costTotal = sum(rows, r => r.cost);
      const grossTotal = revenueTotal - costTotal;
      const grossPct = revenueTotal > 0 ? grossTotal / revenueTotal : NaN;

      $("kpiRevenue").textContent = money(revenueTotal);
      $("kpiCost").textContent = money(costTotal);
      $("kpiGross").textContent = money(grossTotal);
      $("kpiGrossPct").textContent = pct(grossPct);

      // group by month
      const byMonth = groupBy(rows.filter(r=>r.date), r => r.date.slice(0,7));
      const months = Object.keys(byMonth).sort();
      const revSeries = months.map(m => sum(byMonth[m], r=>r.revenue));
      const grossSeries = months.map(m => sum(byMonth[m], r=>(r.revenue - r.cost)));

      // charts
      renderLineChart("chartRevenue", months, revSeries, "Ricavi");
      renderLineChart("chartMargin", months, grossSeries, "Margine");

      // top products
      const byProd = groupBy(rows, r=>r.product || "—");
      const prodRows = Object.entries(byProd).map(([k, arr]) => ({
        key: k,
        revenue: sum(arr, r=>r.revenue),
        gross: sum(arr, r=>(r.revenue - r.cost))
      })).sort((a,b)=>b.revenue - a.revenue).slice(0, 10);

      $("topProducts").innerHTML = buildRankList(prodRows, "revenue", "gross");

      // top customers (if any)
      const hasCustomer = rows.some(r => r.customer);
      if (!hasCustomer) {
        $("topCustomers").innerHTML = `<div class="text-xs text-slate-500">Nessuna colonna cliente mappata o dati vuoti.</div>`;
      } else {
        const byCust = groupBy(rows.filter(r => r.customer), r=>r.customer);
        const custRows = Object.entries(byCust).map(([k, arr]) => ({
          key: k,
          revenue: sum(arr, r=>r.revenue),
          gross: sum(arr, r=>(r.revenue - r.cost))
        })).sort((a,b)=>b.revenue - a.revenue).slice(0, 10);
        $("topCustomers").innerHTML = buildRankList(custRows, "revenue", "gross");
      }
    }

    function renderLineChart(canvasId, labels, data, label) {
      const ctx = $(canvasId);
      if (!ctx) return;
      if (state.charts[canvasId]) {
        state.charts[canvasId].destroy();
      }
      state.charts[canvasId] = new Chart(ctx, {
        type: 'line',
        data: {
          labels,
          datasets: [{
            label,
            data,
            tension: 0.25,
            fill: false
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: { display: false },
            tooltip: { mode: 'index', intersect: false }
          },
          scales: {
            y: {
              ticks: {
                callback: (v) => new Intl.NumberFormat("it-IT").format(v)
              }
            }
          }
        }
      });
    }

    function buildRankList(items, fieldMain, fieldSecondary) {
      if (!items.length) return `<div class="text-xs text-slate-500">Nessun dato sufficiente.</div>`;
      return `
        <div class="space-y-2">
          ${items.map((it, i) => `
            <div class="flex items-center justify-between rounded-xl border border-slate-200 bg-white px-3 py-2">
              <div class="flex items-center gap-3">
                <div class="h-7 w-7 rounded-lg bg-slate-900 text-white text-xs font-bold grid place-items-center">${i+1}</div>
                <div>
                  <div class="text-sm font-semibold">${escapeHTML(it.key)}</div>
                  <div class="small-muted">Margine: ${money(it[fieldSecondary] ?? 0)}</div>
                </div>
              </div>
              <div class="text-sm font-bold">${money(it[fieldMain] ?? 0)}</div>
            </div>
          `).join("")}
        </div>
      `;
    }

    /***********************
     * Margins
     ***********************/
    $("btnGoBillingFromPaywall").addEventListener("click", () => showView("billing"));

    function renderMargins() {
      const hasData = state.normRows?.length > 0;
      $("marginsEmpty").classList.toggle("hidden", hasData);

      const isPro = state.plan === "pro";
      $("marginsPlanPill").className = isPro ? "pill-ok" : "pill-warn";
      $("marginsPlanPill").textContent = isPro ? "Piano Pro attivo" : "Richiede Pro";

      $("marginsPaywall").classList.toggle("hidden", !hasData || isPro);
      $("marginsContent").classList.toggle("hidden", !hasData || !isPro);

      if (!hasData || !isPro) return;

      const rows = state.normRows;
      const byProd = groupBy(rows, r=>r.product || "—");
      const prodAgg = Object.entries(byProd).map(([k, arr]) => {
        const rev = sum(arr, r=>r.revenue);
        const cost = sum(arr, r=>r.cost);
        const gross = rev - cost;
        const pct = rev > 0 ? gross / rev : NaN;
        return { key: k, revenue: rev, cost, gross, pct, count: arr.length };
      });

      prodAgg.sort((a,b)=>b.gross - a.gross);

      $("mStatProducts").textContent = prodAgg.length;
      $("mStatGross").textContent = money(sum(prodAgg, p=>p.gross));
      const worst10 = [...prodAgg].sort((a,b)=>a.gross - b.gross).slice(0,10);
      $("mStatWorst").textContent = worst10.length;

      const alerts = buildMarginAlerts(prodAgg);
      $("mStatAlerts").textContent = alerts.length;

      $("mTopProducts").innerHTML = buildMarginsList(prodAgg.slice(0,10));
      $("mWorstProducts").innerHTML = buildMarginsList(worst10, true);
      $("mAlertsList").innerHTML = alerts.length
        ? alerts.map(a => `<div class="rounded-xl border border-amber-200 bg-amber-50 px-3 py-2">
            <b>${escapeHTML(a.title)}</b> — ${escapeHTML(a.text)}
          </div>`).join("")
        : `<div class="text-xs text-slate-500">Nessun alert critico rilevato con le regole base.</div>`;
    }

    function buildMarginsList(items, emphasizeBad=false) {
      if (!items.length) return `<div class="text-xs text-slate-500">Nessun dato sufficiente.</div>`;
      return `
        <div class="space-y-2">
          ${items.map((it, i) => {
            const badgeClass = emphasizeBad
              ? (it.gross < 0 ? "pill-bad" : "pill-warn")
              : (it.gross >= 0 ? "pill-ok" : "pill-bad");
            const badgeText = isFinite(it.pct) ? pct(it.pct) : "—";
            return `
              <div class="flex items-center justify-between rounded-xl border border-slate-200 bg-white px-3 py-2">
                <div class="flex items-center gap-3">
                  <div class="h-7 w-7 rounded-lg ${emphasizeBad ? "bg-rose-600" : "bg-slate-900"} text-white text-xs font-bold grid place-items-center">${i+1}</div>
                  <div>
                    <div class="text-sm font-semibold">${escapeHTML(it.key)}</div>
                    <div class="small-muted">Ricavi: ${money(it.revenue)} • Costi: ${money(it.cost)}</div>
                  </div>
                </div>
                <div class="text-right">
                  <div class="text-sm font-extrabold">${money(it.gross)}</div>
                  <span class="${badgeClass}">${badgeText}</span>
                </div>
              </div>
            `;
          }).join("")}
        </div>
      `;
    }

    function buildMarginAlerts(prodAgg) {
      const alerts = [];
      // Rule 1: negative gross
      const neg = prodAgg.filter(p => p.gross < 0);
      if (neg.length) {
        alerts.push({
          title: "Prodotti in perdita",
          text: `${neg.length} prodotti/servizi hanno margine negativo. Priorità alta.`
        });
      }

      // Rule 2: low margin pct under 5% with meaningful revenue
      const low = prodAgg.filter(p => isFinite(p.pct) && p.pct < 0.05 && p.revenue > 500);
      if (low.length) {
        alerts.push({
          title: "Margini troppo bassi",
          text: `${low.length} prodotti con margine <5% e ricavi significativi. Valuta prezzo o costo fornitore.`
        });
      }

      // Rule 3: small revenue but high handling count
      const noisy = prodAgg.filter(p => p.revenue < 300 && p.count >= 3);
      if (noisy.length) {
        alerts.push({
          title: "Bassa resa operativa",
          text: `${noisy.length} prodotti con ricavi bassi ma presenza ricorrente. Potrebbero creare attrito operativo.`
        });
      }

      return alerts;
    }

    /***********************
     * Billing (demo)
     ***********************/
    $("btnSetBasic").addEventListener("click", () => setPlan("basic"));
    $("btnSetPro").addEventListener("click", () => setPlan("pro"));

    function setPlan(plan) {
      state.plan = plan;
      localStorage.setItem(LS.plan, plan);
      syncWorkspaceUI();
      renderMargins();
      showView("margins");
    }

    /***********************
     * Utilities
     ***********************/
    function sum(arr, fn) {
      let s = 0;
      arr.forEach(x => {
        const v = fn(x);
        if (isFinite(v)) s += v;
      });
      return s;
    }
    function groupBy(arr, fnKey) {
      const m = {};
      for (const x of arr) {
        const k = fnKey(x) ?? "—";
        (m[k] ||= []).push(x);
      }
      return m;
    }

    /***********************
     * Boot
     ***********************/
    function boot() {
      // default company name for nicer demo
      if (!state.company) {
        state.company = "Demo PMI Srl";
        localStorage.setItem(LS.company, state.company);
      }

      syncWorkspaceUI();

      // If mapping exists but norm missing, rebuild
      if (state.mapping && state.rawRows?.length && (!state.normRows || !state.normRows.length)) {
        normalizeDataset();
      }

      // highlight initial nav
      showView("import");

      // if we already have raw headers, prep mapping selects
      if (state.rawRows?.length) {
        state.lastImportHeaders = Object.keys(state.rawRows[0] || {});
        prepareMappingSelects();
        $("importPreviewWrap").classList.remove("hidden");
      }
    }

    boot();
  </script>
</body>
</html>
