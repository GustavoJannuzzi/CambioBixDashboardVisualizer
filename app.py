import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import io
import warnings

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CambioBix · Análise de Migração CRM",
    page_icon="💱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .stApp { background: linear-gradient(135deg, #0d1117 0%, #161b26 60%, #0d1117 100%); }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #161b26 0%, #0d1117 100%);
        border-right: 1px solid #30363d;
    }
    [data-testid="stSidebar"] * { color: #e6edf3 !important; }

    .metric-card {
        background: linear-gradient(135deg, #1c2333 0%, #21262d 100%);
        border: 1px solid #30363d;
        border-radius: 16px;
        padding: 20px 24px;
        text-align: center;
        transition: transform .2s, box-shadow .2s;
        position: relative;
        overflow: hidden;
    }
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(56,139,253,.25);
    }
    .metric-card::before {
        content: "";
        position: absolute; top: 0; left: 0; right: 0;
        height: 3px; border-radius: 16px 16px 0 0;
    }
    .metric-card.blue::before   { background: linear-gradient(90deg, #388bfd, #58a6ff); }
    .metric-card.green::before  { background: linear-gradient(90deg, #3fb950, #56d364); }
    .metric-card.orange::before { background: linear-gradient(90deg, #f0883e, #ffa657); }
    .metric-card.purple::before { background: linear-gradient(90deg, #bc8cff, #d2a8ff); }
    .metric-card.red::before    { background: linear-gradient(90deg, #f85149, #ff7b72); }
    .metric-card.teal::before   { background: linear-gradient(90deg, #39d353, #2ea043); }
    .metric-card.cyan::before   { background: linear-gradient(90deg, #79c0ff, #388bfd); }

    .metric-value { font-size: 2.2rem; font-weight: 800; color: #e6edf3; line-height: 1; margin-bottom: 6px; }
    .metric-label { font-size: .75rem; font-weight: 500; color: #8b949e; text-transform: uppercase; letter-spacing: .08em; }
    .metric-icon  { font-size: 1.5rem; margin-bottom: 8px; }

    .section-header {
        font-size: 1.1rem; font-weight: 700; color: #e6edf3;
        border-left: 4px solid #388bfd;
        padding-left: 12px; margin: 24px 0 14px;
    }
    .section-header.history { border-color: #bc8cff; }

    .stat-row {
        display: flex; justify-content: space-between; align-items: center;
        padding: 10px 14px; border-radius: 8px; margin-bottom: 6px;
        background: #1c2333; border: 1px solid #30363d; transition: background .15s;
    }
    .stat-row:hover { background: #21262d; }
    .stat-col-name { font-size: .85rem; font-weight: 600; color: #c9d1d9; }
    .stat-col-type { font-size: .72rem; color: #6e7681; font-style: italic; }
    .stat-null-badge { font-size: .75rem; font-weight: 700; padding: 3px 10px; border-radius: 20px; }
    .high-null   { background: rgba(248,81,73,.2);  color: #ff7b72; }
    .medium-null { background: rgba(240,136,62,.2); color: #ffa657; }
    .low-null    { background: rgba(56,139,253,.2); color: #58a6ff; }
    .zero-null   { background: rgba(63,185,80,.2);  color: #56d364; }

    .null-bar { height: 6px; border-radius: 3px; background: linear-gradient(90deg, #388bfd, #58a6ff); margin-top: 4px; }

    /* mode badge */
    .mode-badge {
        display: inline-block; padding: 4px 14px; border-radius: 20px;
        font-size: .78rem; font-weight: 700; letter-spacing: .05em;
        margin-bottom: 12px;
    }
    .mode-badge.ops      { background: rgba(56,139,253,.2); color: #58a6ff; border: 1px solid rgba(56,139,253,.4); }
    .mode-badge.history  { background: rgba(188,140,255,.2); color: #d2a8ff; border: 1px solid rgba(188,140,255,.4); }
    .mode-badge.combined { background: rgba(63,185,80,.2);  color: #56d364; border: 1px solid rgba(63,185,80,.4); }

    /* combined mode — op card */
    .op-card-combined {
        background: linear-gradient(145deg,#1c2333,#21262d);
        border: 1px solid #30363d;
        border-left: 4px solid #388bfd;
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 14px;
    }
    /* status badges */
    .sbadge { display:inline-block; padding:2px 10px; border-radius:20px; font-size:.75rem; font-weight:600; }
    .sbadge-resolved  { background:rgba(63,185,80,.15);  color:#56d364; border:1px solid rgba(63,185,80,.3); }
    .sbadge-pending   { background:rgba(240,136,62,.15); color:#ffa657; border:1px solid rgba(240,136,62,.3); }
    .sbadge-analysis  { background:rgba(56,139,253,.15); color:#58a6ff; border:1px solid rgba(56,139,253,.3); }
    .sbadge-cancelled { background:rgba(248,81,73,.15);  color:#ff7b72; border:1px solid rgba(248,81,73,.3); }
    .sbadge-default   { background:rgba(139,148,158,.15);color:#8b949e; border:1px solid rgba(139,148,158,.3); }

    .stTabs [data-baseweb="tab-list"] { background: #161b26; border-radius: 10px; gap: 4px; }
    .stTabs [data-baseweb="tab"]      { background: transparent; color: #8b949e; border-radius: 8px; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] { background: #21262d; color: #e6edf3; }

    [data-testid="stFileUploadDropzone"] {
        background: #161b26 !important; border: 2px dashed #30363d !important; border-radius: 12px !important;
    }
    h1, h2, h3 { color: #e6edf3 !important; }
    p, li, span { color: #c9d1d9; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#c9d1d9"),
    margin=dict(l=20, r=20, t=40, b=20),
)
LEGEND_STYLE = dict(bgcolor="rgba(0,0,0,0)", bordercolor="#30363d")

COLOR_PALETTE = [
    "#388bfd", "#3fb950", "#f0883e", "#bc8cff",
    "#f85149", "#39d353", "#ffa657", "#d2a8ff",
    "#ff7b72", "#58a6ff",
]
STATUS_COLOR_MAP = {
    "Novo": "#388bfd", "Análise": "#bc8cff",
    "Pendente Complemento": "#f0883e", "Pendente Analise PLD": "#ffa657",
    "Pendente Documentação": "#ffd700", "Documentação": "#d2a8ff",
    "PLD Aprovado": "#3fb950", "Liquidação": "#39d353",
    "Encerrado": "#8b949e", "Cancelado": "#f85149",
    "Bacen": "#58a6ff", "PLD Rejeitado": "#ff7b72",
    "Legitimação": "#e3b341", "Anulado": "#6e7681",
}
TASK_COLOR_MAP = {
    "CheckSLADeadline": "#f0883e",
    "ExecuteSLA":      "#388bfd",
    "CheckSLAGoal":    "#3fb950",
}

DB_MODES = {
    "📋  Registros de Operações": "ops",
    "🕐  Histórico de Operações": "history",
    "🔗  Operações + Histórico Vinculado": "combined",
}

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_excel(file_bytes: bytes, filename: str) -> dict:
    buf = io.BytesIO(file_bytes)
    xl = pd.ExcelFile(buf)
    return {sheet: xl.parse(sheet) for sheet in xl.sheet_names}


def null_badge(pct: float) -> str:
    if pct == 0:       cls = "zero-null"
    elif pct < 20:     cls = "low-null"
    elif pct < 50:     cls = "medium-null"
    else:              cls = "high-null"
    return f'<span class="stat-null-badge {cls}">{pct:.1f}%</span>'


def metric_card(icon: str, value, label: str, color: str = "blue") -> str:
    return f"""
    <div class="metric-card {color}">
        <div class="metric-icon">{icon}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
    </div>"""


def render_quality_table(df: pd.DataFrame, total_rows: int):
    """Render the per-column quality HTML list."""
    null_series     = df.isnull().sum()
    null_pct_series = (null_series / total_rows * 100).round(2)
    html = ""
    for col in df.columns:
        n_null = int(null_series[col])
        pct    = float(null_pct_series[col])
        dtype  = str(df[col].dtype)
        n_uniq = int(df[col].nunique(dropna=True))
        bar    = f'<div class="null-bar" style="width:{min(pct,100):.1f}%;"></div>'
        html  += f"""
        <div class="stat-row">
            <div>
                <div class="stat-col-name">{col}</div>
                <div class="stat-col-type">{dtype} · {n_uniq} únicos</div>
                {bar}
            </div>
            <div style="text-align:right; min-width:120px;">
                {null_badge(pct)}
                <div style="font-size:.7rem; color:#6e7681; margin-top:4px;">
                    {n_null} / {total_rows} nulos
                </div>
            </div>
        </div>"""
    st.markdown(html, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
        <div style="text-align:center; padding: 20px 0 10px;">
            <div style="font-size:2.5rem;">💱</div>
            <div style="font-size:1.3rem; font-weight:800; color:#e6edf3;">CambioBix</div>
            <div style="font-size:.75rem; color:#6e7681; margin-top:4px;">Análise de Migração · CRM</div>
        </div>
        <hr style="border-color:#30363d; margin: 10px 0 16px;">
        """,
        unsafe_allow_html=True,
    )

    # ── Database type selector
    db_mode_label = st.selectbox(
        "🗄️  Tipo de base de dados",
        list(DB_MODES.keys()),
        index=0,
        help=(
            "Registros de Operações: arquivo ControleDiario... com dados das operações de câmbio.\n\n"
            "Histórico de Operações: arquivo pxGetWorkHistory... com o log de eventos por operação."
        ),
    )
    db_mode = DB_MODES[db_mode_label]

    st.markdown("<div style='margin-top:8px;'></div>", unsafe_allow_html=True)

    # ── File uploader(s)
    if db_mode == "combined":
        st.markdown("**📋 Arquivo de Operações (ControleDiario):**")
        uploaded_cd = st.file_uploader(
            "Operações", type=["xlsx", "xls"],
            help="Arquivo ControleDiario com as operações de câmbio.",
            key="up_cd",
        )
        if uploaded_cd:
            st.success(f"✅ {uploaded_cd.name}")
            st.caption(f"{uploaded_cd.size / 1024:.1f} KB")

        st.markdown("**📜 Arquivo de Histórico (pxGetWorkHistory):**")
        uploaded_hist = st.file_uploader(
            "Histórico", type=["xlsx", "xls"],
            help="Arquivo pxGetWorkHistory com o log de eventos.",
            key="up_hist",
        )
        if uploaded_hist:
            st.success(f"✅ {uploaded_hist.name}")
            st.caption(f"{uploaded_hist.size / 1024:.1f} KB")

        uploaded_file = None  # não usado no modo combined
    else:
        uploaded_cd   = None
        uploaded_hist = None
        uploaded_file = st.file_uploader(
            "📂 Carregar arquivo Excel",
            type=["xlsx", "xls"],
            help="Faça upload do relatório exportado do CRM.",
        )
        if uploaded_file:
            st.success(f"✅ **{uploaded_file.name}**")
            st.caption(f"Tamanho: {uploaded_file.size / 1024:.1f} KB")

    st.markdown("<hr style='border-color:#30363d; margin:16px 0 8px;'>", unsafe_allow_html=True)
    st.markdown(
        "<div style='font-size:.7rem; color:#6e7681; text-align:center;'>Versão 1.0 · 2026</div>",
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────────────────────────────────────
# PAGE HEADER
# ─────────────────────────────────────────────────────────────────────────────
if db_mode == "ops":
    mode_label_html = '<span class="mode-badge ops">📋 Registros de Operações</span>'
elif db_mode == "history":
    mode_label_html = '<span class="mode-badge history">🕐 Histórico de Operações</span>'
else:
    mode_label_html = '<span class="mode-badge combined">🔗 Operações + Histórico Vinculado</span>'
st.markdown(
    f"""
    <h1 style="font-size:2rem; font-weight:800; margin-bottom:4px;">
        💱 Dashboard · Operações de Câmbio
    </h1>
    {mode_label_html}
    <p style="color:#8b949e; margin-bottom:20px;">
        Análise pré-migração de CRM · Visualize, filtre e diagnostique seus dados
    </p>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# UPLOAD GATE
# ─────────────────────────────────────────────────────────────────────────────
# ── Upload gate
if db_mode == "combined":
    missing = []
    if not uploaded_cd:   missing.append("Operações (ControleDiario)")
    if not uploaded_hist: missing.append("Histórico (pxGetWorkHistory)")
    if missing:
        st.markdown(
            f"""
            <div style="background:linear-gradient(135deg,#1c2333,#161b26);border:1px dashed #30363d;
                        border-radius:16px;padding:60px 40px;text-align:center;margin-top:40px;">
                <div style="font-size:3rem;margin-bottom:16px;">🔗</div>
                <h2 style="color:#e6edf3;font-size:1.4rem;margin-bottom:8px;">
                    Carregue os dois arquivos para começar
                </h2>
                <p style="color:#6e7681;max-width:500px;margin:0 auto;">
                    Faltando: <b style='color:#f0883e'>{'</b> e <b style="color:#f0883e">'.join(missing)}</b>
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.stop()
elif not uploaded_file:
    st.markdown(
        """
        <div style="background:linear-gradient(135deg,#1c2333,#161b26);border:1px dashed #30363d;
                    border-radius:16px;padding:60px 40px;text-align:center;margin-top:40px;">
            <div style="font-size:3rem;margin-bottom:16px;">📊</div>
            <h2 style="color:#e6edf3;font-size:1.4rem;margin-bottom:8px;">
                Faça upload do seu Excel para começar
            </h2>
            <p style="color:#6e7681;max-width:500px;margin:0 auto;">
                Use o painel lateral para selecionar o tipo de base de dados e depois
                carregar o arquivo exportado do CRM.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────────────────────────────────────
if db_mode == "combined":
    # ── Carregar os dois arquivos separados
    @st.cache_data(show_spinner=False)
    def load_combined(cd_bytes, hist_bytes):
        df_cd   = pd.read_excel(io.BytesIO(cd_bytes))
        df_hist = pd.read_excel(io.BytesIO(hist_bytes))
        # Constantes de chave
        col_chave_cd   = "Chave de manipulação de instâncias"
        col_chave_hist = "Histórico de"
        # Normalizar chaves
        df_cd[col_chave_cd]     = df_cd[col_chave_cd].astype(str).str.strip()
        df_hist[col_chave_hist] = df_hist[col_chave_hist].astype(str).str.strip()
        # Contagem de histórico por operação
        hist_count = (
            df_hist.groupby(col_chave_hist)
            .size()
            .reset_index(name="Qtd Histórico")
        )
        df_cd = df_cd.merge(
            hist_count,
            left_on=col_chave_cd,
            right_on=col_chave_hist,
            how="left",
            suffixes=("", "_h"),
        )
        df_cd["Qtd Histórico"] = df_cd["Qtd Histórico"].fillna(0).astype(int)
        if col_chave_hist in df_cd.columns and col_chave_hist != col_chave_cd:
            df_cd.drop(columns=[col_chave_hist], inplace=True)
        return df_cd, df_hist, col_chave_cd, col_chave_hist

    with st.spinner("Carregando e cruzando os dados…"):
        df_cd, df_hist_raw, COL_CD, COL_HIST = load_combined(
            uploaded_cd.getvalue(), uploaded_hist.getvalue()
        )

else:
    with st.spinner("Carregando e processando dados..."):
        sheets = load_excel(uploaded_file.getvalue(), uploaded_file.name)

    main_sheet = max(sheets.items(), key=lambda kv: len(kv[1]))[0]
    df_raw = sheets[main_sheet].copy()

    # Sidebar sheet selector (only for ops mode)
    if db_mode == "ops":
        with st.sidebar:
            if len(sheets) > 1:
                st.markdown("**📋 Planilhas disponíveis**")
                main_sheet = st.selectbox(
                    "Selecione a planilha principal:",
                    list(sheets.keys()),
                    index=list(sheets.keys()).index(main_sheet),
                )
                df_raw = sheets[main_sheet].copy()


# ══════════════════════════════════════════════════════════════════════════════
#  MODE C — OPERAÇÕES + HISTÓRICO VINCULADO
# ══════════════════════════════════════════════════════════════════════════════
if db_mode == "combined":

    # ── helpers internos ──────────────────────────────────────────────────────
    def _fmt_val(val):
        try:
            if pd.isna(val): return "—"
            return f"{float(val):,.2f}".replace(",","X").replace(".","," ).replace("X",".")
        except Exception: return str(val)

    def _fmt_date(val):
        try:
            if pd.isna(val): return "—"
            if isinstance(val, str): return val[:10]
            return pd.Timestamp(val).strftime("%d/%m/%Y")
        except Exception: return str(val)

    def _badge(status: str) -> str:
        s = str(status).lower()
        if any(k in s for k in ["resolv","concluíd","finaliz"]): cls = "sbadge-resolved"
        elif any(k in s for k in ["pendent","aguard"]):          cls = "sbadge-pending"
        elif any(k in s for k in ["análise","analise"]):         cls = "sbadge-analysis"
        elif "cancel" in s:                                       cls = "sbadge-cancelled"
        else:                                                     cls = "sbadge-default"
        return f'<span class="sbadge {cls}">{status}</span>'

    # ── KPIs ──────────────────────────────────────────────────────────────────
    total_ops  = len(df_cd)
    total_hist = len(df_hist_raw)
    ops_c_hist = (df_cd["Qtd Histórico"] > 0).sum()
    pct_ch     = ops_c_hist / total_ops * 100 if total_ops else 0
    vol_me     = df_cd["Valor ME"].sum() if "Valor ME" in df_cd.columns else 0
    n_moedas   = df_cd["Código ME"].nunique() if "Código ME" in df_cd.columns else 0

    k1,k2,k3,k4,k5 = st.columns(5)
    for col_k, icon, val, label, color in [
        (k1,"📋",f"{total_ops:,}","Operações","blue"),
        (k2,"📜",f"{total_hist:,}","Registros de Histórico","purple"),
        (k3,"💰",_fmt_val(vol_me),"Volume Total ME","green"),
        (k4,"💱",n_moedas,"Moedas Distintas","orange"),
        (k5,"📊",f"{pct_ch:.0f}%",f"Com Histórico ({ops_c_hist}/{total_ops})","teal"),
    ]:
        col_k.markdown(metric_card(icon, val, label, color), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Abas ──────────────────────────────────────────────────────────────────
    tab_drill, tab_charts, tab_table = st.tabs([
        "📋 Operações + Histórico",
        "📊 Análises Visuais",
        "🔗 Tabela Combinada",
    ])

    # ── Filtros (sidebar) ─────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("---")
        st.markdown("**🔍 Filtros**")
        statuses = sorted(df_cd["Status de caso"].dropna().unique()) if "Status de caso" in df_cd.columns else []
        sel_st   = st.multiselect("Status", statuses, default=statuses, key="c_st")
        moedas_l = sorted(df_cd["Código ME"].dropna().unique()) if "Código ME" in df_cd.columns else []
        sel_me   = st.multiselect("Moeda ME", moedas_l, default=moedas_l, key="c_me")
        tipos_l  = sorted(df_cd["Tipo Operação"].dropna().unique()) if "Tipo Operação" in df_cd.columns else []
        sel_tp   = st.multiselect("Tipo Operação", tipos_l, default=tipos_l, key="c_tp")
        srch     = st.text_input("🔎 Buscar ID / Razão Social", "", key="c_srch")

    df_view = df_cd.copy()
    if sel_st: df_view = df_view[df_view["Status de caso"].isin(sel_st)]
    if sel_me: df_view = df_view[df_view["Código ME"].isin(sel_me)]
    if sel_tp: df_view = df_view[df_view["Tipo Operação"].isin(sel_tp)]
    if srch.strip():
        t = srch.strip().lower()
        mask = pd.Series(False, index=df_view.index)
        for c in ["ID do Caso","Razão Social","Nome Fantasia", COL_CD, "Operador"]:
            if c in df_view.columns:
                mask |= df_view[c].astype(str).str.lower().str.contains(t, na=False)
        df_view = df_view[mask]

    # ── TAB 1 · Drill-down ───────────────────────────────────────────────────
    with tab_drill:
        col_left, col_right = st.columns([1.3, 1.7], gap="medium")

        with col_left:
            st.markdown('<div class="section-header">📋 Operações de Câmbio</div>', unsafe_allow_html=True)

            ids_list = df_view["ID do Caso"].dropna().astype(str).tolist() if "ID do Caso" in df_view.columns else df_view[COL_CD].tolist()
            if not ids_list:
                st.warning("Nenhuma operação com os filtros aplicados.")
                st.stop()

            sel_id = st.selectbox("Selecione uma Operação:", ids_list, key="c_sel_id")

            resumo_cols = [c for c in ["ID do Caso","Status de caso","Nome Fantasia","Código ME","Valor ME","Data Criação","Qtd Histórico"] if c in df_view.columns]
            df_res = df_view[resumo_cols].copy()
            if "Valor ME"    in df_res.columns: df_res["Valor ME"]    = df_res["Valor ME"].apply(_fmt_val)
            if "Data Criação" in df_res.columns: df_res["Data Criação"] = df_res["Data Criação"].apply(_fmt_date)
            st.dataframe(df_res.reset_index(drop=True), use_container_width=True, height=420, hide_index=True)

        with col_right:
            st.markdown('<div class="section-header">📜 Histórico da Operação</div>', unsafe_allow_html=True)

            if "ID do Caso" in df_view.columns:
                op_row = df_view[df_view["ID do Caso"].astype(str) == str(sel_id)]
            else:
                op_row = df_view[df_view[COL_CD].astype(str) == str(sel_id)]

            if op_row.empty:
                st.info("Operação não encontrada.")
            else:
                op     = op_row.iloc[0]
                chave  = str(op.get(COL_CD,"")).strip()
                status = str(op.get("Status de caso",""))
                me_cod = str(op.get("Código ME",""))
                val_me = op.get("Valor ME", None)
                taxa   = op.get("Taxa", None)
                emp    = str(op.get("Nome Fantasia", op.get("Razão Social","")))
                oper   = str(op.get("Operador",""))
                dcri   = _fmt_date(op.get("Data Criação", None))
                tipo   = str(op.get("Tipo Operação",""))
                qtdh   = int(op.get("Qtd Histórico", 0))

                st.markdown(f"""
                <div class="op-card-combined">
                    <div style="font-weight:700;font-size:1rem;color:#79c0ff;margin-bottom:6px">📌 {sel_id} &nbsp;·&nbsp; {emp}</div>
                    <div style="font-size:.82rem;color:#8b949e">
                        {_badge(status)} &nbsp;
                        <b style="color:#e3b341">{me_cod}</b> &nbsp;
                        Valor: <b style="color:#56d364">{_fmt_val(val_me)} {me_cod}</b> &nbsp;
                        Taxa: <b style="color:#79c0ff">{_fmt_val(taxa)}</b>
                    </div>
                    <div style="font-size:.82rem;color:#8b949e;margin-top:6px">
                        📅 {dcri} &nbsp;·&nbsp; ⚙️ {tipo} &nbsp;·&nbsp; 👤 {oper} &nbsp;·&nbsp; 📜 <b>{qtdh}</b> reg. histórico
                    </div>
                    <div style="font-size:.73rem;color:#484f58;margin-top:4px">🔑 {chave}</div>
                </div>
                """, unsafe_allow_html=True)

                with st.expander("📂 Todos os campos da Operação"):
                    disp_cols = [c for c in ["ID do Caso", COL_CD, "Data Criação","Status de caso","Nome Fantasia","Razão Social","Valor ME","Código ME","Taxa","Taxa Nivelamento","Tipo Operação","Modalidade","Tipo","Valor MN","VET","Ptax","Operador","Qtd Histórico"] if c in op_row.columns]
                    det = op_row[disp_cols].T.reset_index()
                    det.columns = ["Campo","Valor"]
                    det["Valor"] = det["Valor"].astype(str)
                    st.dataframe(det, use_container_width=True, hide_index=True, height=280)

                st.markdown("---")

                # Histórico filtrado
                df_h_op = df_hist_raw[df_hist_raw[COL_HIST].astype(str).str.strip() == chave].copy()

                if df_h_op.empty:
                    st.markdown("""
                    <div style="background:rgba(56,139,253,.08);border:1px solid rgba(56,139,253,.2);border-radius:10px;padding:12px 16px;color:#79c0ff;font-size:.88rem">
                        ⚠️ Nenhum registro de histórico encontrado para esta operação.
                    </div>""", unsafe_allow_html=True)
                else:
                    if "Criar hora" in df_h_op.columns:
                        df_h_op = df_h_op.sort_values("Criar hora", ascending=True)

                    st.markdown(f'<p style="color:#8b949e;font-size:.85rem;margin-bottom:10px">🔗 {len(df_h_op)} registro(s) vinculados</p>', unsafe_allow_html=True)

                    col_task = "Nome da Tarefa"       if "Nome da Tarefa"       in df_h_op.columns else None
                    col_hora = "Criar hora"            if "Criar hora"            in df_h_op.columns else None
                    col_exec = "Executante"            if "Executante"            in df_h_op.columns else None
                    col_tipo = "Tipo de Caso/Suporte" if "Tipo de Caso/Suporte" in df_h_op.columns else None
                    col_ident= "Identificador"        if "Identificador"        in df_h_op.columns else None

                    n_h = len(df_h_op)
                    for i, (_, row_h) in enumerate(df_h_op.iterrows()):
                        tarefa  = str(row_h[col_task])  if col_task  else "—"
                        hora    = _fmt_date(row_h[col_hora]) if col_hora else "—"
                        exec_   = str(row_h[col_exec])  if col_exec  else "—"
                        tipo_h  = str(row_h[col_tipo])  if col_tipo  else ""
                        ident   = str(row_h[col_ident]) if col_ident else ""
                        for v in [tarefa, exec_, tipo_h, ident]:
                            pass
                        if tarefa  == "nan": tarefa  = "—"
                        if exec_   == "nan": exec_   = "—"
                        if tipo_h  == "nan": tipo_h  = ""
                        if ident   == "nan": ident   = ""

                        dot_c = "#56d364" if i==0 else ("#f85149" if i==n_h-1 else "#388bfd")
                        dot_g = "rgba(63,185,80,.5)" if i==0 else ("rgba(248,81,73,.5)" if i==n_h-1 else "rgba(56,139,253,.5)")
                        sep   = "<div style='width:2px;background:#30363d;height:16px;margin:2px auto 0 auto'></div>" if i < n_h-1 else ""
                        mb    = "8px" if i < n_h-1 else "0px"
                        id_tag= f"<span style='font-size:.73rem;color:#8b949e;background:#21262d;padding:1px 8px;border-radius:10px;margin-left:6px'>{ident}</span>" if ident else ""
                        td    = tipo_h if tipo_h else "N/A"

                        card = (
                            f"<div style='display:flex;gap:12px;align-items:flex-start;margin-bottom:0'>"
                            f"<div style='display:flex;flex-direction:column;align-items:center;flex-shrink:0;width:14px;padding-top:4px'>"
                            f"<div style='width:12px;height:12px;border-radius:50%;background:{dot_c};box-shadow:0 0 7px {dot_g};flex-shrink:0'></div>"
                            f"{sep}</div>"
                            f"<div style='background:linear-gradient(145deg,#1c2333,#21262d);border:1px solid #30363d;border-radius:10px;padding:10px 14px;flex:1;margin-bottom:{mb}'>"
                            f"<div style='font-weight:600;font-size:.88rem;color:#e6edf3'>{tarefa} {id_tag}</div>"
                            f"<div style='font-size:.78rem;color:#8b949e;margin-top:4px'>📅 {hora} &nbsp;|&nbsp; {td}</div>"
                            f"<div style='font-size:.78rem;color:#79c0ff;margin-top:2px;font-weight:500'>👤 {exec_}</div>"
                            f"</div></div>"
                        )
                        st.markdown(card, unsafe_allow_html=True)

                    with st.expander("📑 Ver tabela do histórico"):
                        hist_disp = [c for c in ["Identificador", COL_HIST,"Nome da Tarefa","Criar hora","Executante","Tipo de Caso/Suporte","Atribuição decorrida"] if c in df_h_op.columns]
                        st.dataframe(df_h_op[hist_disp].reset_index(drop=True), use_container_width=True, hide_index=True)

    # ── TAB 2 · Gráficos ─────────────────────────────────────────────────────
    with tab_charts:
        st.markdown('<div class="section-header">📊 Análises Visuais</div>', unsafe_allow_html=True)

        r1c1, r1c2 = st.columns(2)
        with r1c1:
            if "Status de caso" in df_view.columns:
                sc = df_view["Status de caso"].value_counts().reset_index()
                sc.columns = ["Status","Qtd"]
                fig_s = px.bar(sc, x="Qtd", y="Status", orientation="h",
                               color="Qtd", color_continuous_scale=["#388bfd","#bc8cff"],
                               template="plotly_dark", text="Qtd", title="📌 Por Status")
                fig_s.update_traces(textposition="outside")
                fig_s.update_layout(**PLOTLY_LAYOUT, height=320, showlegend=False, coloraxis_showscale=False,
                                    yaxis=dict(categoryorder="total ascending"))
                st.plotly_chart(fig_s, use_container_width=True)

        with r1c2:
            if "Código ME" in df_view.columns and "Valor ME" in df_view.columns:
                mv = df_view.groupby("Código ME")["Valor ME"].sum().reset_index()
                mv.columns = ["Moeda","Volume"]
                fig_m = px.pie(mv, values="Volume", names="Moeda", hole=0.45,
                               title="💰 Volume por Moeda", template="plotly_dark",
                               color_discrete_sequence=COLOR_PALETTE)
                fig_m.update_traces(textinfo="label+percent", marker=dict(line=dict(color="#0d1117", width=2)))
                fig_m.update_layout(**PLOTLY_LAYOUT, height=320)
                st.plotly_chart(fig_m, use_container_width=True)

        r2c1, r2c2 = st.columns(2)
        with r2c1:
            if "Tipo Operação" in df_view.columns:
                tc = df_view["Tipo Operação"].value_counts().nlargest(10).reset_index()
                tc.columns = ["Tipo","Qtd"]
                fig_t = px.bar(tc, x="Tipo", y="Qtd", color="Qtd",
                               color_continuous_scale=["#388bfd","#bc8cff"],
                               template="plotly_dark", text="Qtd", title="⚙️ Tipos de Operação")
                fig_t.update_traces(textposition="outside")
                fig_t.update_layout(**PLOTLY_LAYOUT, height=320, showlegend=False, coloraxis_showscale=False,
                                    xaxis=dict(tickangle=-30))
                st.plotly_chart(fig_t, use_container_width=True)

        with r2c2:
            if "Qtd Histórico" in df_view.columns:
                hd = df_view["Qtd Histórico"].value_counts().sort_index().reset_index()
                hd.columns = ["Qtd Histórico","Operações"]
                fig_hd = px.bar(hd, x="Qtd Histórico", y="Operações", color="Operações",
                                color_continuous_scale=["#2ea043","#56d364"],
                                template="plotly_dark", text="Operações",
                                title="📜 Registros de Histórico por Operação")
                fig_hd.update_traces(textposition="outside")
                fig_hd.update_layout(**PLOTLY_LAYOUT, height=320, showlegend=False, coloraxis_showscale=False)
                st.plotly_chart(fig_hd, use_container_width=True)

        # Evolução temporal
        if "Data Criação" in df_view.columns:
            st.markdown("---")
            dt = df_view.copy()
            dt["Mês"] = pd.to_datetime(dt["Data Criação"], errors="coerce").dt.to_period("M").astype(str)
            dt = dt.dropna(subset=["Mês"])
            if len(dt) > 0:
                tempo = dt.groupby("Mês").agg(Quantidade=("ID do Caso","count"), Volume=("Valor ME","sum")).reset_index().sort_values("Mês")
                fig_ev = go.Figure()
                fig_ev.add_trace(go.Bar(x=tempo["Mês"], y=tempo["Quantidade"], name="Qtd Operações",
                                        marker_color="#388bfd", opacity=0.85, yaxis="y1"))
                fig_ev.add_trace(go.Scatter(x=tempo["Mês"], y=tempo["Volume"], name="Volume ME",
                                            mode="lines+markers", line=dict(color="#56d364", width=2.5),
                                            yaxis="y2"))
                fig_ev.update_layout(
                    **PLOTLY_LAYOUT, height=360,
                    title="📅 Evolução Temporal",
                    yaxis=dict(title="Quantidade"),
                    yaxis2=dict(title="Volume ME", overlaying="y", side="right", showgrid=False),
                    legend=dict(**LEGEND_STYLE, orientation="h"),
                )
                st.plotly_chart(fig_ev, use_container_width=True)

        # Top clientes
        if "Razão Social" in df_view.columns and "Valor ME" in df_view.columns:
            st.markdown("---")
            st.markdown('<div class="section-header">🏆 Top 10 Clientes por Volume ME</div>', unsafe_allow_html=True)
            top = df_view.groupby("Razão Social").agg(Operações=("ID do Caso","count"), Volume_ME=("Valor ME","sum")).reset_index().sort_values("Volume_ME",ascending=False).head(10)
            top["Volume_ME"] = top["Volume_ME"].apply(_fmt_val)
            st.dataframe(top.reset_index(drop=True), use_container_width=True, hide_index=True)

    # ── TAB 3 · Tabela Combinada ──────────────────────────────────────────────
    with tab_table:
        st.markdown('<div class="section-header">🔗 Tabela Combinada (Operação × Histórico)</div>', unsafe_allow_html=True)

        hist_disp_cols = [c for c in ["Identificador", COL_HIST, "Nome da Tarefa","Criar hora","Executante","Tipo de Caso/Suporte"] if c in df_hist_raw.columns]
        df_merged = df_view.merge(
            df_hist_raw[hist_disp_cols],
            left_on=COL_CD, right_on=COL_HIST,
            how="left", suffixes=("","_hist"),
        )

        sort_c = st.selectbox("Ordenar por:", df_merged.columns.tolist()[:15], key="c_sort")
        asc    = st.radio("Ordem:", ["Crescente","Decrescente"], horizontal=True, key="c_asc") == "Crescente"
        df_merged = df_merged.sort_values(sort_c, ascending=asc)

        st.caption(f"{len(df_merged):,} linhas (operação × histórico)")
        st.dataframe(df_merged.reset_index(drop=True), use_container_width=True, height=500, hide_index=True)

        @st.cache_data
        def _to_excel(df):
            buf = io.BytesIO()
            with pd.ExcelWriter(buf, engine="openpyxl") as w:
                df.to_excel(w, index=False)
            return buf.getvalue()

        from datetime import datetime as _dt
        st.download_button(
            "📥 Exportar para Excel",
            data=_to_excel(df_merged),
            file_name=f"operacoes_historico_{_dt.now().strftime('%Y%m%d_%H%M')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="c_down",
        )

    st.stop()   # não executar os modos A e B


# ══════════════════════════════════════════════════════════════════════════════
#  MODE A — HISTÓRICO DE OPERAÇÕES
# ══════════════════════════════════════════════════════════════════════════════
if db_mode == "history":


    # ── Identify columns by position (robust to encoding issues)
    col_hist = df_raw.columns[0]   # "Histórico de"
    col_id   = df_raw.columns[1]   # "Identificador"
    col_task = df_raw.columns[2]   # "Nome da Tarefa"
    col_date = df_raw.columns[3]   # "Criar hora"
    col_exec = df_raw.columns[4]   # "Executante"
    col_tipo = df_raw.columns[5]   # "Tipo de Caso/Suporte"
    col_dur  = df_raw.columns[6]   # "Atribuição decorrida"

    total_rows       = len(df_raw)
    total_cols       = len(df_raw.columns)
    operacoes_unicas = df_raw[col_hist].nunique()
    hist_por_op      = df_raw[col_hist].value_counts()
    null_series      = df_raw.isnull().sum()
    null_pct_series  = (null_series / total_rows * 100).round(2)
    null_global      = float((null_series.sum() / (total_rows * total_cols)) * 100)
    cols_completas   = int((null_pct_series == 0).sum())
    cols_vazias      = int((null_pct_series == 100).sum())

    date_min = df_raw[col_date].min()
    date_max = df_raw[col_date].max()

    tab_visao, tab_tarefas, tab_operacoes, tab_qualidade = st.tabs([
        "📊  Visão Geral",
        "⚙️  Tarefas & Executantes",
        "🔗  Por Operação",
        "🔍  Qualidade dos Dados",
    ])

    # ── TAB 1 · Visão Geral ──────────────────────────────────────────────────
    with tab_visao:
        st.markdown('<div class="section-header history">Resumo do Histórico</div>', unsafe_allow_html=True)

        c1, c2, c3, c4, c5 = st.columns(5)
        c1.markdown(metric_card("📜", f"{total_rows:,}", "Registros de Histórico", "purple"), unsafe_allow_html=True)
        c2.markdown(metric_card("🔗", f"{operacoes_unicas:,}", "Operações Referenciadas", "blue"), unsafe_allow_html=True)
        c3.markdown(metric_card("🗂️", total_cols, "Colunas", "teal"), unsafe_allow_html=True)
        c4.markdown(metric_card("📊", f"{hist_por_op.mean():.0f}", "Média de Registros/Op.", "orange"), unsafe_allow_html=True)
        c5.markdown(metric_card("⚠️", f"{null_global:.1f}%", "Nulos (global)", "red"), unsafe_allow_html=True)

        # ── Period info box
        st.markdown(
            f"""
            <div style="background:#1c2333; border:1px solid #30363d; border-radius:12px;
                        padding:14px 20px; margin:16px 0; display:flex; gap:40px; align-items:center;">
                <div>
                    <div style="font-size:.7rem; color:#6e7681; text-transform:uppercase; letter-spacing:.08em;">Período dos dados</div>
                    <div style="font-size:1rem; font-weight:700; color:#e6edf3; margin-top:4px;">
                        {date_min.strftime('%d/%m/%Y %H:%M')} &nbsp;→&nbsp; {date_max.strftime('%d/%m/%Y %H:%M')}
                    </div>
                </div>
                <div>
                    <div style="font-size:.7rem; color:#6e7681; text-transform:uppercase; letter-spacing:.08em;">Duração total registrada</div>
                    <div style="font-size:1rem; font-weight:700; color:#e6edf3; margin-top:4px;">
                        {str(date_max - date_min).split('.')[0]}
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── Task distribution donut
        colA, colB = st.columns([1, 1.4])
        with colA:
            st.markdown('<div class="section-header history">Distribuição por Tarefa</div>', unsafe_allow_html=True)
            task_counts = df_raw[col_task].value_counts().reset_index()
            task_counts.columns = ["Tarefa", "Qtd"]
            colors = [TASK_COLOR_MAP.get(t, "#58a6ff") for t in task_counts["Tarefa"]]
            fig_task = go.Figure(go.Pie(
                labels=task_counts["Tarefa"], values=task_counts["Qtd"],
                hole=0.55,
                marker=dict(colors=colors, line=dict(color="#0d1117", width=2)),
                textinfo="percent+label",
                hovertemplate="<b>%{label}</b><br>Qtd: %{value}<br>%{percent}<extra></extra>",
            ))
            fig_task.update_layout(
                **PLOTLY_LAYOUT, height=340,
                showlegend=False,
                annotations=[dict(text=f"<b>{total_rows:,}</b><br>eventos",
                                  x=0.5, y=0.5, font=dict(size=14, color="#e6edf3"), showarrow=False)],
            )
            st.plotly_chart(fig_task, use_container_width=True)

        with colB:
            st.markdown('<div class="section-header history">Linha do Tempo de Eventos</div>', unsafe_allow_html=True)
            ts = df_raw.copy()
            ts["Hora"] = ts[col_date].dt.floor("H")
            ts_grp = ts.groupby(["Hora", col_task]).size().reset_index(name="Eventos")
            fig_ts = px.line(
                ts_grp, x="Hora", y="Eventos", color=col_task,
                color_discrete_map=TASK_COLOR_MAP,
                template="plotly_dark", markers=False,
            )
            fig_ts.update_layout(
                **PLOTLY_LAYOUT, height=340,
                xaxis_title="", yaxis_title="Eventos/hora",
                legend=dict(**LEGEND_STYLE, title="Tarefa"),
            )
            st.plotly_chart(fig_ts, use_container_width=True)

        # ── Column overview
        st.markdown('<div class="section-header history">Visão das Colunas</div>', unsafe_allow_html=True)
        col_info = []
        for i, col in enumerate(df_raw.columns):
            pct = float(null_pct_series[col])
            n_uniq = int(df_raw[col].nunique(dropna=True))
            col_info.append({
                "Índice": i,
                "Nome da Coluna": col,
                "Tipo": str(df_raw[col].dtype),
                "Únicos": n_uniq,
                "Nulos": int(null_series[col]),
                "% Nulos": pct,
                "Status": "🚫 Vazia" if pct == 100 else ("✅ Completa" if pct == 0 else "🟡 Parcial"),
            })
        st.dataframe(
            pd.DataFrame(col_info),
            use_container_width=True,
            hide_index=True,
            column_config={
                "% Nulos": st.column_config.ProgressColumn("% Nulos", min_value=0, max_value=100, format="%.1f%%"),
                "Nulos": st.column_config.NumberColumn("Nulos", format="%d"),
                "Únicos": st.column_config.NumberColumn("Únicos", format="%d"),
            },
        )
        # Warnings
        if cols_vazias > 0:
            st.warning(
                f"⚠️ **{cols_vazias} coluna(s) completamente vazias** no arquivo de histórico: "
                f"`{col_id}` e `{col_dur}`. Estas colunas não serão úteis na migração.",
                icon="🚫",
            )

    # ── TAB 2 · Tarefas & Executantes ────────────────────────────────────────
    with tab_tarefas:
        st.markdown('<div class="section-header history">Tarefas Registradas</div>', unsafe_allow_html=True)

        # Task bar
        task_counts = df_raw[col_task].value_counts().reset_index()
        task_counts.columns = ["Tarefa", "Quantidade"]
        task_counts["% do Total"] = (task_counts["Quantidade"] / total_rows * 100).round(2)
        colors = [TASK_COLOR_MAP.get(t, "#58a6ff") for t in task_counts["Tarefa"]]

        fig_task_bar = go.Figure(go.Bar(
            x=task_counts["Tarefa"], y=task_counts["Quantidade"],
            marker=dict(color=colors, line=dict(color="#0d1117", width=1.5)),
            text=task_counts["Quantidade"],
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>Qtd: %{y}<extra></extra>",
        ))
        fig_task_bar.update_layout(
            **PLOTLY_LAYOUT, height=320, yaxis_title="Nº de Eventos", legend=LEGEND_STYLE,
        )
        st.plotly_chart(fig_task_bar, use_container_width=True)

        st.dataframe(task_counts, use_container_width=True, hide_index=True,
                     column_config={"Quantidade": st.column_config.NumberColumn(format="%d"),
                                    "% do Total": st.column_config.NumberColumn(format="%.2f%%")})

        # Executante
        st.markdown('<div class="section-header history">Executantes</div>', unsafe_allow_html=True)
        exec_counts = df_raw[col_exec].value_counts().reset_index()
        exec_counts.columns = ["Executante", "Quantidade"]
        exec_counts["% do Total"] = (exec_counts["Quantidade"] / total_rows * 100).round(2)

        fig_exec = px.bar(
            exec_counts, x="Quantidade", y="Executante", orientation="h",
            color="Quantidade", color_continuous_scale=["#388bfd", "#bc8cff"],
            template="plotly_dark", text="Quantidade",
        )
        fig_exec.update_layout(
            **PLOTLY_LAYOUT, height=max(250, len(exec_counts) * 50),
            yaxis=dict(autorange="reversed"), coloraxis_showscale=False,
            legend=LEGEND_STYLE,
        )
        st.plotly_chart(fig_exec, use_container_width=True)

        # Tipo de Caso
        st.markdown('<div class="section-header history">Tipo de Caso/Suporte</div>', unsafe_allow_html=True)
        tipo_counts = df_raw[col_tipo].value_counts().reset_index()
        tipo_counts.columns = ["Tipo", "Quantidade"]
        tipo_counts["% do Total"] = (tipo_counts["Quantidade"] / total_rows * 100).round(2)
        st.dataframe(tipo_counts, use_container_width=True, hide_index=True,
                     column_config={"Quantidade": st.column_config.NumberColumn(format="%d"),
                                    "% do Total": st.column_config.NumberColumn(format="%.2f%%")})

    # ── TAB 3 · Por Operação ─────────────────────────────────────────────────
    with tab_operacoes:
        st.markdown('<div class="section-header history">Registros por Operação</div>', unsafe_allow_html=True)

        hist_por_op_df = hist_por_op.reset_index()
        hist_por_op_df.columns = ["Operação", "Qtd. Registros de Histórico"]
        hist_por_op_df["Índice"] = range(1, len(hist_por_op_df) + 1)

        # Summary cards
        m1, m2, m3, m4 = st.columns(4)
        m1.markdown(metric_card("🔗", f"{operacoes_unicas:,}", "Operações com Histórico", "purple"), unsafe_allow_html=True)
        m2.markdown(metric_card("📊", f"{hist_por_op.mean():.0f}", "Média de Registros/Op.", "blue"), unsafe_allow_html=True)
        m3.markdown(metric_card("⬆️", f"{hist_por_op.max():,}", "Máximo de Registros", "orange"), unsafe_allow_html=True)
        m4.markdown(metric_card("⬇️", f"{hist_por_op.min():,}", "Mínimo de Registros", "teal"), unsafe_allow_html=True)

        # Bar chart — records per operation
        fig_op = px.bar(
            hist_por_op_df.head(30),
            x="Operação", y="Qtd. Registros de Histórico",
            color="Qtd. Registros de Histórico",
            color_continuous_scale=["#388bfd", "#bc8cff"],
            template="plotly_dark", text="Qtd. Registros de Histórico",
        )
        fig_op.update_layout(
            **PLOTLY_LAYOUT, height=400,
            xaxis_tickangle=-45, coloraxis_showscale=False,
            yaxis_title="Registros de Histórico", legend=LEGEND_STYLE,
        )
        st.plotly_chart(fig_op, use_container_width=True)

        # Drill-down: select operation
        st.markdown('<div class="section-header history">Detalhar uma Operação</div>', unsafe_allow_html=True)
        operacoes_lista = sorted(df_raw[col_hist].unique().tolist())
        sel_op = st.selectbox("Selecione uma Operação:", operacoes_lista)
        df_op = df_raw[df_raw[col_hist] == sel_op].copy()

        info_cols = st.columns(3)
        info_cols[0].metric("Registros de histórico", len(df_op))
        info_cols[1].metric("Período", f"{df_op[col_date].min().strftime('%H:%M:%S')} → {df_op[col_date].max().strftime('%H:%M:%S')}")
        info_cols[2].metric("Duração", str(df_op[col_date].max() - df_op[col_date].min()).split('.')[0])

        st.dataframe(
            df_op[[col_hist, col_task, col_date, col_exec]].reset_index(drop=True),
            use_container_width=True,
            height=320,
        )

        # Table of all operations
        st.markdown('<div class="section-header history">Todas as Operações e Contagem</div>', unsafe_allow_html=True)
        st.dataframe(hist_por_op_df, use_container_width=True, hide_index=True,
                     column_config={
                         "Qtd. Registros de Histórico": st.column_config.NumberColumn(
                             "Registros de Histórico", format="%d"
                         )
                     })

        csv_bytes = hist_por_op_df.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            "⬇️ Exportar contagem por operação (CSV)",
            data=csv_bytes, file_name="historico_por_operacao.csv", mime="text/csv",
        )

    # ── TAB 4 · Qualidade dos Dados ──────────────────────────────────────────
    with tab_qualidade:
        st.markdown('<div class="section-header history">Diagnóstico de Qualidade · Pré-Migração</div>', unsafe_allow_html=True)

        q1, q2, q3, q4 = st.columns(4)
        cols_partial  = int(((null_pct_series > 0) & (null_pct_series < 100)).sum())
        cols_critical = int((null_pct_series >= 50).sum())
        q1.markdown(metric_card("✅", cols_completas,  "Colunas Completas",       "green"),  unsafe_allow_html=True)
        q2.markdown(metric_card("🟡", cols_partial,    "Colunas Parciais",        "orange"), unsafe_allow_html=True)
        q3.markdown(metric_card("🚫", cols_vazias,     "Colunas 100% Vazias",     "red"),    unsafe_allow_html=True)
        q4.markdown(metric_card("🔴", cols_critical,   "Colunas Críticas ≥50%",   "red"),    unsafe_allow_html=True)

        # Null bar chart
        st.markdown('<div class="section-header history">Mapa de Nulos por Coluna</div>', unsafe_allow_html=True)
        null_df = pd.DataFrame({"Coluna": null_pct_series.index, "% Nulos": null_pct_series.values}).sort_values("% Nulos", ascending=False)
        fig_null = px.bar(
            null_df, x="Coluna", y="% Nulos",
            color="% Nulos", color_continuous_scale=["#3fb950", "#f0883e", "#f85149"],
            range_color=[0, 100], template="plotly_dark",
            labels={"% Nulos": "% de Valores Nulos"}, height=320,
        )
        fig_null.update_layout(**PLOTLY_LAYOUT, coloraxis_showscale=True, xaxis_tickangle=-15)
        st.plotly_chart(fig_null, use_container_width=True)

        # Per-column detail
        st.markdown('<div class="section-header history">Estatísticas por Coluna</div>', unsafe_allow_html=True)
        render_quality_table(df_raw, total_rows)

        # Migration recommendations
        st.markdown('<div class="section-header history">Recomendações para Migração</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div style="background:#1c2333; border:1px solid #30363d; border-radius:12px; padding:20px 24px;">
                <div style="font-size:.9rem; color:#c9d1d9; line-height:1.8;">
                    <b style="color:#e6edf3;">⚠️ Colunas a desconsiderar na migração:</b><br>
                    &nbsp;• <code style="background:#30363d; padding:1px 6px; border-radius:4px;">Identificador</code> — 100% vazia<br>
                    &nbsp;• <code style="background:#30363d; padding:1px 6px; border-radius:4px;">Atribuição decorrida</code> — 100% vazia<br><br>
                    <b style="color:#e6edf3;">✅ Colunas essenciais para migrar:</b><br>
                    &nbsp;• <code style="background:#30363d; padding:1px 6px; border-radius:4px;">Histórico de</code> — Chave de vínculo com a operação (0% nulos)<br>
                    &nbsp;• <code style="background:#30363d; padding:1px 6px; border-radius:4px;">Nome da Tarefa</code> — Tipo de evento registrado (0% nulos)<br>
                    &nbsp;• <code style="background:#30363d; padding:1px 6px; border-radius:4px;">Criar hora</code> — Timestamp do evento (0% nulos)<br>
                    &nbsp;• <code style="background:#30363d; padding:1px 6px; border-radius:4px;">Executante</code> — Agente responsável (0% nulos)<br>
                    &nbsp;• <code style="background:#30363d; padding:1px 6px; border-radius:4px;">Tipo de Caso/Suporte</code> — Classificação do caso (0% nulos)<br>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        csv_stats = pd.DataFrame({"Coluna": null_pct_series.index, "% Nulos": null_pct_series.values,
                                   "Nulos": null_series.values, "Total": total_rows}).to_csv(index=False).encode("utf-8-sig")
        st.download_button("⬇️ Exportar relatório de qualidade (CSV)", data=csv_stats,
                           file_name="qualidade_historico.csv", mime="text/csv")


# ══════════════════════════════════════════════════════════════════════════════
#  MODE B — REGISTROS DE OPERAÇÕES
# ══════════════════════════════════════════════════════════════════════════════
else:
    # ── Detect key columns
    status_col = next((c for c in df_raw.columns if "status" in c.lower()), None)
    date_col   = next((c for c in df_raw.columns if df_raw[c].dtype == "datetime64[ns]"), None)
    id_col     = df_raw.columns[0]

    total_rows = len(df_raw)
    total_cols = len(df_raw.columns)
    null_total = int(df_raw.isnull().sum().sum())
    null_pct   = null_total / (total_rows * total_cols) * 100 if total_rows else 0
    dup_count  = int(df_raw[id_col].duplicated().sum())
    empty_cols = int((df_raw.isnull().mean() == 1).sum())

    tab_visao, tab_tabela, tab_qualidade, tab_graficos = st.tabs([
        "📊  Visão Geral",
        "📋  Tabela & Filtros",
        "🔍  Qualidade dos Dados",
        "📈  Gráficos Detalhados",
    ])

    # ── TAB 1 · Visão Geral ──────────────────────────────────────────────────
    with tab_visao:
        st.markdown('<div class="section-header">Resumo Geral</div>', unsafe_allow_html=True)
        c1, c2, c3, c4, c5, c6 = st.columns(6)
        c1.markdown(metric_card("📄", f"{total_rows:,}", "Registros", "blue"),        unsafe_allow_html=True)
        c2.markdown(metric_card("🗂️", total_cols, "Colunas", "purple"),               unsafe_allow_html=True)
        c3.markdown(metric_card("⚠️", f"{null_pct:.1f}%", "Nulos (global)", "orange"), unsafe_allow_html=True)
        c4.markdown(metric_card("🔁", dup_count, "IDs Duplicados", "red"),            unsafe_allow_html=True)
        c5.markdown(metric_card("🚫", empty_cols, "Colunas Vazias", "red"),           unsafe_allow_html=True)
        if date_col:
            date_range = f"{df_raw[date_col].min().strftime('%d/%m/%y')} – {df_raw[date_col].max().strftime('%d/%m/%y')}"
            c6.markdown(metric_card("📅", date_range, "Período", "teal"), unsafe_allow_html=True)
        else:
            c6.markdown(metric_card("🆔", f"{df_raw[id_col].nunique():,}", "IDs Únicos", "teal"), unsafe_allow_html=True)

        colA, colB = st.columns([1, 1.5])
        with colA:
            st.markdown('<div class="section-header">Distribuição por Status</div>', unsafe_allow_html=True)
            if status_col:
                sc = df_raw[status_col].value_counts().reset_index()
                sc.columns = ["Status", "Qtd"]
                colors = [STATUS_COLOR_MAP.get(s, "#58a6ff") for s in sc["Status"]]
                fig_donut = go.Figure(go.Pie(
                    labels=sc["Status"], values=sc["Qtd"], hole=0.55,
                    marker=dict(colors=colors, line=dict(color="#0d1117", width=2)),
                    textinfo="percent",
                    hovertemplate="<b>%{label}</b><br>Qtd: %{value}<br>%{percent}<extra></extra>",
                ))
                fig_donut.update_layout(
                    **PLOTLY_LAYOUT, height=380, showlegend=True,
                    legend=dict(orientation="v", x=1.05, y=0.5, bgcolor="rgba(0,0,0,0)", bordercolor="#30363d"),
                    annotations=[dict(text=f"<b>{total_rows}</b><br>total", x=0.5, y=0.5,
                                      font=dict(size=16, color="#e6edf3"), showarrow=False)],
                )
                st.plotly_chart(fig_donut, use_container_width=True)

        with colB:
            st.markdown('<div class="section-header">Registros ao Longo do Tempo</div>', unsafe_allow_html=True)
            if date_col:
                ts = df_raw.copy()
                ts["Mês"] = ts[date_col].dt.to_period("M").dt.to_timestamp()
                ts_grp = ts.groupby("Mês").size().reset_index(name="Registros")
                fig_ts = px.area(ts_grp, x="Mês", y="Registros",
                                 color_discrete_sequence=["#388bfd"], template="plotly_dark")
                fig_ts.update_traces(line=dict(width=2.5), fillcolor="rgba(56,139,253,.15)")
                fig_ts.update_layout(**PLOTLY_LAYOUT, height=380, xaxis_title="",
                                     yaxis_title="Nº de Registros", legend=LEGEND_STYLE)
                st.plotly_chart(fig_ts, use_container_width=True)
            else:
                st.info("Coluna de data não detectada.")

        if status_col:
            st.markdown('<div class="section-header">Detalhe por Status</div>', unsafe_allow_html=True)
            sdf = df_raw[status_col].value_counts().reset_index()
            sdf.columns = ["Status", "Quantidade"]
            sdf["% do Total"] = (sdf["Quantidade"] / total_rows * 100).round(2).astype(str) + "%"
            st.dataframe(sdf, use_container_width=True, hide_index=True,
                         column_config={"Quantidade": st.column_config.NumberColumn(format="%d")})

    # ── TAB 2 · Tabela & Filtros ─────────────────────────────────────────────
    with tab_tabela:
        st.markdown('<div class="section-header">Filtros Interativos</div>', unsafe_allow_html=True)
        df_filtered = df_raw.copy()
        cat_cols = [c for c in df_raw.columns if df_raw[c].dtype == object and 1 < df_raw[c].nunique() <= 50]

        fc = st.columns(min(len(cat_cols), 4))
        active_filters: dict = {}
        for i, col in enumerate(cat_cols[:4]):
            with fc[i]:
                opts = sorted(df_raw[col].dropna().unique().tolist())
                sel  = st.multiselect(f"🔽 {col}", opts, key=f"f_{col}")
                if sel: active_filters[col] = sel

        if len(cat_cols) > 4:
            fc2 = st.columns(min(len(cat_cols) - 4, 4))
            for i, col in enumerate(cat_cols[4:8]):
                with fc2[i]:
                    opts = sorted(df_raw[col].dropna().unique().tolist())
                    sel  = st.multiselect(f"🔽 {col}", opts, key=f"f2_{col}")
                    if sel: active_filters[col] = sel

        if date_col:
            st.markdown("**📅 Filtrar por período:**")
            dc1, dc2 = st.columns(2)
            min_d = df_raw[date_col].min().date()
            max_d = df_raw[date_col].max().date()
            start_d = dc1.date_input("De:", value=min_d, min_value=min_d, max_value=max_d)
            end_d   = dc2.date_input("Até:", value=max_d, min_value=min_d, max_value=max_d)
            df_filtered = df_filtered[(df_filtered[date_col].dt.date >= start_d) & (df_filtered[date_col].dt.date <= end_d)]

        for col, vals in active_filters.items():
            df_filtered = df_filtered[df_filtered[col].isin(vals)]

        search_term = st.text_input("🔎 Busca livre:", placeholder="Ex: P-28007")
        if search_term:
            mask = df_filtered.apply(lambda c: c.astype(str).str.contains(search_term, case=False, na=False)).any(axis=1)
            df_filtered = df_filtered[mask]

        _filter_suffix = (
            f' · 🔽 <b style="color:#f0883e;">{len(active_filters)}</b>'
            '<span style="color:#8b949e;"> filtros ativos</span></div>'
            if active_filters else "</div>"
        )
        st.markdown(
            f'<div style="background:#1c2333;border:1px solid #30363d;border-radius:10px;padding:12px 20px;margin:12px 0;">'
            f'🔢 <b style="color:#58a6ff;">{len(df_filtered):,}</b>'
            f'<span style="color:#8b949e;"> registros filtrados de </span><b style="color:#e6edf3;">{total_rows:,}</b>'
            f'{_filter_suffix}',
            unsafe_allow_html=True,
        )

        with st.expander("⚙️ Selecionar colunas a exibir"):
            selected_cols = st.multiselect("Colunas:", df_filtered.columns.tolist(), default=df_filtered.columns.tolist()[:15])
        display_df = df_filtered[selected_cols] if selected_cols else df_filtered
        st.dataframe(display_df, use_container_width=True, height=480)
        st.download_button("⬇️ Exportar resultado filtrado (CSV)",
                           data=df_filtered.to_csv(index=False).encode("utf-8-sig"),
                           file_name="cambio_filtrado.csv", mime="text/csv")

    # ── TAB 3 · Qualidade dos Dados ──────────────────────────────────────────
    with tab_qualidade:
        st.markdown('<div class="section-header">Diagnóstico de Qualidade · Pré-Migração</div>', unsafe_allow_html=True)
        null_series     = df_raw.isnull().sum()
        null_pct_series = (null_series / total_rows * 100).round(2)

        q1, q2, q3, q4 = st.columns(4)
        cols_complete = int((null_pct_series == 0).sum())
        cols_partial  = int(((null_pct_series > 0) & (null_pct_series < 100)).sum())
        cols_empty    = int((null_pct_series == 100).sum())
        cols_critical = int((null_pct_series >= 50).sum())
        q1.markdown(metric_card("✅", cols_complete, "Colunas Completas",       "green"),  unsafe_allow_html=True)
        q2.markdown(metric_card("🟡", cols_partial,  "Colunas Parciais",        "orange"), unsafe_allow_html=True)
        q3.markdown(metric_card("🚫", cols_empty,    "Colunas Vazias",          "red"),    unsafe_allow_html=True)
        q4.markdown(metric_card("🔴", cols_critical, "Colunas Críticas ≥50%",   "red"),    unsafe_allow_html=True)

        st.markdown('<div class="section-header">Mapa de Nulos por Coluna</div>', unsafe_allow_html=True)
        null_df = pd.DataFrame({"Coluna": null_pct_series.index, "% Nulos": null_pct_series.values}).sort_values("% Nulos", ascending=False)
        fig_bar = px.bar(null_df, x="Coluna", y="% Nulos",
                         color="% Nulos", color_continuous_scale=["#3fb950", "#f0883e", "#f85149"],
                         range_color=[0, 100], template="plotly_dark", height=380)
        fig_bar.update_layout(**PLOTLY_LAYOUT, coloraxis_showscale=True, xaxis_tickangle=-45)
        st.plotly_chart(fig_bar, use_container_width=True)

        sort_opt = st.selectbox("Ordenar por:", ["% de Nulos (↓)", "% de Nulos (↑)", "Nome da Coluna A-Z", "Tipo de Dado"])
        stats_rows = [{"Coluna": c, "Tipo": str(df_raw[c].dtype), "Nulos": int(null_series[c]),
                       "% Nulos": float(null_pct_series[c]), "Únicos": int(df_raw[c].nunique(dropna=True)),
                       "Preenchidos": total_rows - int(null_series[c])} for c in df_raw.columns]
        stats_df = pd.DataFrame(stats_rows)
        if sort_opt == "% de Nulos (↓)":         stats_df = stats_df.sort_values("% Nulos", ascending=False)
        elif sort_opt == "% de Nulos (↑)":        stats_df = stats_df.sort_values("% Nulos")
        elif sort_opt == "Nome da Coluna A-Z":     stats_df = stats_df.sort_values("Coluna")
        else:                                      stats_df = stats_df.sort_values("Tipo")

        render_quality_table(df_raw.reindex(columns=stats_df["Coluna"]), total_rows)

        st.download_button("⬇️ Exportar relatório de qualidade (CSV)",
                           data=stats_df.to_csv(index=False).encode("utf-8-sig"),
                           file_name="qualidade_colunas.csv", mime="text/csv")

    # ── TAB 4 · Gráficos Detalhados ──────────────────────────────────────────
    with tab_graficos:
        st.markdown('<div class="section-header">Gráficos Exploratórios</div>', unsafe_allow_html=True)

        if status_col:
            st.markdown("#### 📊 Registros por Status")
            sc = df_raw[status_col].value_counts().reset_index()
            sc.columns = ["Status", "Qtd"]
            colors = [STATUS_COLOR_MAP.get(s, "#58a6ff") for s in sc["Status"]]
            fig_bs = go.Figure(go.Bar(
                x=sc["Qtd"], y=sc["Status"], orientation="h",
                marker=dict(color=colors, line=dict(color="#0d1117", width=1.5)),
                text=sc["Qtd"], textposition="outside",
                hovertemplate="<b>%{y}</b><br>Qtd: %{x}<extra></extra>",
            ))
            fig_bs.update_layout(**PLOTLY_LAYOUT, height=max(350, len(sc) * 36),
                                 xaxis_title="Nº de Registros", yaxis=dict(autorange="reversed"),
                                 legend=LEGEND_STYLE)
            st.plotly_chart(fig_bs, use_container_width=True)

        if date_col and status_col:
            st.markdown("#### 📅 Evolução Temporal por Status")
            ts2 = df_raw.copy()
            ts2["Mês"] = ts2[date_col].dt.to_period("M").dt.to_timestamp()
            ts2_grp = ts2.groupby(["Mês", status_col]).size().reset_index(name="Registros")
            top_s = df_raw[status_col].value_counts().head(7).index.tolist()
            ts2_grp = ts2_grp[ts2_grp[status_col].isin(top_s)]
            fig_ts2 = px.line(ts2_grp, x="Mês", y="Registros", color=status_col,
                              color_discrete_map=STATUS_COLOR_MAP, template="plotly_dark", markers=True)
            fig_ts2.update_layout(**PLOTLY_LAYOUT, height=400, xaxis_title="", yaxis_title="Nº de Registros",
                                  legend=dict(**LEGEND_STYLE, orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
            st.plotly_chart(fig_ts2, use_container_width=True)

        nome_col = next((c for c in df_raw.columns if "nome" in c.lower() or "fantasia" in c.lower()), None)
        if nome_col and df_raw[nome_col].nunique() > 1:
            st.markdown(f"#### 🏢 Top 15 · {nome_col}")
            tc = df_raw[nome_col].value_counts().head(15).reset_index()
            tc.columns = [nome_col, "Qtd"]
            fig_cli = px.bar(tc, x="Qtd", y=nome_col, orientation="h",
                             color="Qtd", color_continuous_scale=["#388bfd", "#bc8cff"],
                             template="plotly_dark", text="Qtd")
            fig_cli.update_layout(**PLOTLY_LAYOUT, height=460, yaxis=dict(autorange="reversed"),
                                  coloraxis_showscale=False, legend=LEGEND_STYLE)
            st.plotly_chart(fig_cli, use_container_width=True)

        num_cols = df_raw.select_dtypes(include=[np.number]).columns.tolist()
        useful_num = [c for c in num_cols if df_raw[c].nunique() > 5 and df_raw[c].notna().sum() > 50]
        if useful_num:
            st.markdown("#### 📐 Distribuição de Valores Numéricos")
            sel_num  = st.selectbox("Selecione a coluna numérica:", useful_num)
            col_data = df_raw[sel_num].dropna()
            fig_hist = px.histogram(col_data, nbins=40, color_discrete_sequence=["#388bfd"],
                                    template="plotly_dark", labels={"value": sel_num})
            fig_hist.update_layout(**PLOTLY_LAYOUT, height=340, xaxis_title=sel_num,
                                   yaxis_title="Frequência", legend=LEGEND_STYLE)
            st.plotly_chart(fig_hist, use_container_width=True)
            bc = st.columns(4)
            bc[0].metric("Mínimo",  f"{col_data.min():,.2f}")
            bc[1].metric("Média",   f"{col_data.mean():,.2f}")
            bc[2].metric("Máximo",  f"{col_data.max():,.2f}")
            bc[3].metric("Mediana", f"{col_data.median():,.2f}")

        tipo_col = next((c for c in df_raw.columns if "tipo" in c.lower() and "opera" in c.lower()), None)
        if tipo_col:
            st.markdown(f"#### ⚡ Distribuição por {tipo_col}")
            tipo_c = df_raw[tipo_col].value_counts().reset_index()
            tipo_c.columns = [tipo_col, "Qtd"]
            fig_tipo = px.pie(tipo_c, names=tipo_col, values="Qtd",
                              color_discrete_sequence=COLOR_PALETTE, template="plotly_dark", hole=0.4)
            fig_tipo.update_layout(**PLOTLY_LAYOUT, height=360, legend=LEGEND_STYLE)
            st.plotly_chart(fig_tipo, use_container_width=True)
