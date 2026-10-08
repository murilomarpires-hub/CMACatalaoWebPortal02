import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from streamlit_option_menu import option_menu

# App Config
st.set_page_config(
    page_title="Clean Master - Portal de Gestão", 
    page_icon="♻️", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# O modo padrão é o MODO CLARO (False)
if "toggle_tema" not in st.session_state:
    st.session_state["toggle_tema"] = False

modo_escuro = st.session_state.get("toggle_tema", False)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "BALANÇA_ATERRO.xlsx")
LOGO_PATH = os.path.join(BASE_DIR, "Logo", "image (2).png")

# -------------------------------------------------------------
# SIDEBAR
# -------------------------------------------------------------
with st.sidebar:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, use_container_width=True)
        
    st.markdown("""
    <div style="background-color: #187264; border-radius: 10px; padding: 15px; margin-top: 15px; margin-bottom: 20px; color: white; display: flex; align-items: center; gap: 15px;">
        <div style="font-size: 24px;">🏢</div>
        <div>
            <div style="font-size: 10px; font-weight: bold; letter-spacing: 1px; opacity: 0.85;">EMPRESA</div>
            <div style="font-size: 16px; font-weight: bold;">Clean Master</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"<div style='font-size: 11px; font-weight: bold; margin-bottom: 8px; letter-spacing: 1.5px; color: {'#94a3b8' if modo_escuro else '#64748b'};'>GERENCIAMENTO</div>", unsafe_allow_html=True)
    
    # Menus em Ordem Alfabética estrita com subtópicos aninhados em Painel de Engenharia
    menu_opcoes = [
        "Cálculo de Reciclagem",
        "Dashboard de Controle",
        "Gestão de Efluentes",
        "Painel de Engenharia ▴",
        "\u00A0\u00A0↳ Vida Útil",
        "\u00A0\u00A0↳ Calendário Ambiental",
        "Painel Executivo"
    ]
    
    menu_icones = [
        "calculator",
        "speedometer2",
        "droplet-half",
        "gear-wide-connected",
        "hourglass-split",
        "calendar-event",
        "briefcase"
    ]
    
    nav_bg = "#111c30" if modo_escuro else "#ffffff"
    nav_color = "#f8fafc" if modo_escuro else "#1e293b"
    nav_hover = "#1e293b" if modo_escuro else "#f1f5f9"
    sel_bg = "#10b981" if modo_escuro else "#187264"
    icon_color = "#2dd4bf" if modo_escuro else "#187264"

    pagina = option_menu(
        menu_title=None,
        options=menu_opcoes,
        icons=menu_icones,
        menu_icon="cast",
        default_index=1, # Default to Dashboard de Controle
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"font-size": "17px", "color": icon_color},
            "nav-link": {
                "font-size": "14px", 
                "text-align": "left", 
                "margin": "4px 0", 
                "border-radius": "8px", 
                "background-color": nav_bg,
                "color": nav_color,
                "--hover-color": nav_hover
            },
            "nav-link-selected": {
                "background-color": sel_bg, 
                "color": "#ffffff",
                "font-weight": "bold"
            },
        }
    )
    
    # Normalização da rota selecionada para roteamento interno
    pagina_limpa = pagina.replace('\u00A0', '').replace('↳', '').strip()

    st.markdown("<div style='margin-top: 35px;'></div>", unsafe_allow_html=True)
    st.markdown("---")
    
    # -------------------------------------------------------------
    # SELECIONADOR DE TEMA CLARO E ESCURO ANIMADO
    # -------------------------------------------------------------
    st.markdown(f"<div style='font-size: 11px; font-weight: bold; margin-bottom: 6px; letter-spacing: 1.2px; color: {'#94a3b8' if modo_escuro else '#64748b'};'>TEMA DA INTERFACE</div>", unsafe_allow_html=True)
    
    modo_escuro_toggle = st.toggle("Modo Escuro", value=modo_escuro, key="toggle_tema")

# -------------------------------------------------------------
# PALETAS DE CORES ADAPTATIVAS (ALTO CONTRASTE)
# -------------------------------------------------------------
plotly_template = "plotly_dark" if modo_escuro else "plotly_white"

cores_paleta = (
    ['#2dd4bf', '#38bdf8', '#fbbf24', '#fb923c', '#f87171', '#c084fc']
    if modo_escuro else
    ['#0d9488', '#0284c7', '#d97706', '#ea580c', '#e11d48', '#7c3aed']
)

def aplicar_estilo_grafico(fig):
    """Garante fundo 100% transparente, eixos visíveis e legendas legíveis em ambos os modos."""
    cor_texto = "#f8fafc" if modo_escuro else "#1e293b"
    cor_grid = "#334155" if modo_escuro else "#e2e8f0"
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=cor_texto, family="sans-serif"),
        xaxis=dict(
            gridcolor=cor_grid,
            tickfont=dict(color=cor_texto),
            title_font=dict(color=cor_texto)
        ),
        yaxis=dict(
            gridcolor=cor_grid,
            tickfont=dict(color=cor_texto),
            title_font=dict(color=cor_texto)
        ),
        legend=dict(
            font=dict(color=cor_texto, size=13),
            bgcolor="rgba(0,0,0,0)"
        )
    )

# -------------------------------------------------------------
# ESTILIZAÇÃO CSS GLOBAL (COMPATIBILIDADE CLARO / ESCURO)
# -------------------------------------------------------------
if modo_escuro:
    css_modo_especifico = """
        body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background-color: #0b1120 !important;
            color: #f1f5f9 !important;
        }
        
        [data-testid="stSidebar"] {
            background-color: #060b14 !important;
            border-right: 1px solid #1e293b !important;
        }
        
        /* Rótulos e Textos dos Filtros e Widgets */
        div[data-testid="stWidgetLabel"] p,
        div[data-testid="stWidgetLabel"] label,
        label[data-testid="stWidgetLabel"],
        label[data-testid="stWidgetLabel"] p,
        [data-testid="stWidgetLabel"] span {
            color: #f8fafc !important;
            font-weight: 600 !important;
            font-size: 14px !important;
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: #ffffff !important;
        }

        /* Inputs e seletores escuros */
        [data-testid="stSelectbox"] div[data-baseweb="select"],
        [data-testid="stSelectbox"] div[data-baseweb="select"] > div,
        [data-testid="stMultiSelect"] div[data-baseweb="select"],
        [data-testid="stMultiSelect"] div[data-baseweb="select"] > div,
        div[data-baseweb="base-input"] > div,
        div[data-baseweb="input"] > div,
        input[data-baseweb="input"] {
            background-color: #111c30 !important;
            color: #f8fafc !important;
            border: 1px solid #334155 !important;
        }
        
        div[data-baseweb="select"] span {
            color: #f8fafc !important;
        }
        div[data-baseweb="select"] svg {
            fill: #f8fafc !important;
        }

        /* Tags no Multiselect */
        div[data-baseweb="tag"] {
            background-color: #0d3830 !important;
            border: 1px solid #10b981 !important;
        }
        div[data-baseweb="tag"] * {
            color: #ffffff !important;
        }

        /* Dropdown aberto */
        div[data-baseweb="popover"],
        ul[data-baseweb="menu"],
        div[data-baseweb="popover"] > div {
            background-color: #111c30 !important;
            border: 1px solid #334155 !important;
        }
        li[data-baseweb="menu-item"] {
            color: #f8fafc !important;
            background-color: #111c30 !important;
        }
        li[data-baseweb="menu-item"]:hover {
            background-color: #0f766e !important;
        }

        /* Cards de Métricas no Escuro */
        [data-testid="stMetricValue"], [data-testid="stMetricValue"] div {
            color: #34d399 !important;
        }
        [data-testid="stMetricLabel"], [data-testid="stMetricLabel"] p {
            color: #cbd5e1 !important;
            font-weight: 600 !important;
        }
        [data-testid="stMetricWidget"] {
            background-color: #111c30 !important;
            border: 1px solid #1e293b !important;
            border-radius: 10px !important;
            padding: 12px !important;
        }

        /* Abas no Escuro */
        button[data-baseweb="tab"] {
            color: #94a3b8 !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #2dd4bf !important;
            border-bottom-color: #2dd4bf !important;
        }
    """
else:
    css_modo_especifico = """
        body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background-color: #ffffff !important;
            color: #1e293b !important;
        }
        
        [data-testid="stSidebar"] {
            background-color: #f8fafc !important;
            border-right: 1px solid #e2e8f0 !important;
        }
        
        /* Rótulos e Textos no Modo Claro */
        div[data-testid="stWidgetLabel"] p,
        div[data-testid="stWidgetLabel"] label,
        label[data-testid="stWidgetLabel"],
        label[data-testid="stWidgetLabel"] p,
        [data-testid="stWidgetLabel"] span {
            color: #1e293b !important;
            font-weight: 600 !important;
            font-size: 14px !important;
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: #0f172a !important;
        }

        /* Inputs e seletores claros */
        [data-testid="stSelectbox"] div[data-baseweb="select"],
        [data-testid="stSelectbox"] div[data-baseweb="select"] > div,
        [data-testid="stMultiSelect"] div[data-baseweb="select"],
        [data-testid="stMultiSelect"] div[data-baseweb="select"] > div,
        div[data-baseweb="base-input"] > div,
        div[data-baseweb="input"] > div,
        input[data-baseweb="input"] {
            background-color: #ffffff !important;
            color: #0f172a !important;
            border: 1px solid #cbd5e1 !important;
        }
        
        div[data-baseweb="select"] span {
            color: #0f172a !important;
        }
        div[data-baseweb="select"] svg {
            fill: #0f172a !important;
        }

        /* Tags no Multiselect no claro */
        div[data-baseweb="tag"] {
            background-color: #e6f4f1 !important;
            border: 1px solid #187264 !important;
        }
        div[data-baseweb="tag"] * {
            color: #187264 !important;
        }

        /* Cards de Métricas no Claro: NÚMEROS VERDES E NÍTIDOS */
        [data-testid="stMetricValue"], [data-testid="stMetricValue"] div {
            color: #187264 !important;
            font-weight: bold !important;
        }
        [data-testid="stMetricLabel"], [data-testid="stMetricLabel"] p {
            color: #475569 !important;
            font-weight: 600 !important;
        }
        [data-testid="stMetricWidget"] {
            background-color: #f8fafc !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 10px !important;
            padding: 12px !important;
        }

        /* Abas no Modo Claro: TÍTULOS ESCUROS E NÍTIDOS */
        button[data-baseweb="tab"] {
            color: #475569 !important;
            font-weight: 600 !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #187264 !important;
            border-bottom-color: #187264 !important;
        }
    """

css_tema = f"""
    <style>
        .block-container {{
            padding-top: 1.8rem;
            padding-bottom: 2rem;
        }}
        
        /* ----------------------------------------------------------- */
        /* ANIMAÇÃO E DESIGN DO SELECIONADOR (CLARO / ESCURO)          */
        /* ----------------------------------------------------------- */
        .st-key-toggle_tema {{
            margin-top: 5px;
            margin-bottom: 15px;
        }}
        
        .st-key-toggle_tema label p {{
            font-size: 13px !important;
            font-weight: 600 !important;
            color: {'#e2e8f0' if modo_escuro else '#334155'} !important;
        }}

        /* O Pill Switch (Cápsula) */
        .st-key-toggle_tema div[data-baseweb="toggle"] {{
            width: 70px !important;
            height: 34px !important;
            border-radius: 9999px !important;
            padding: 3px !important;
            transition: background-color 0.4s cubic-bezier(0.4, 0, 0.2, 1), border-color 0.4s ease, box-shadow 0.3s ease !important;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.2) !important;
            position: relative !important;
        }}

        /* Estado Claro (Desmarcado): Verde vibrante */
        .st-key-toggle_tema input:not(:checked) + div[data-baseweb="toggle"] {{
            background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
            border: 2px solid #059669 !important;
        }}

        /* Estado Escuro (Marcado): Verde escuro/azulado profundo */
        .st-key-toggle_tema input:checked + div[data-baseweb="toggle"] {{
            background: linear-gradient(135deg, #0d3830 0%, #061f1a 100%) !important;
            border: 2px solid #082d26 !important;
        }}

        /* O Botão Deslizante (Knob Circular) */
        .st-key-toggle_tema div[data-baseweb="toggle"] > div {{
            width: 26px !important;
            height: 26px !important;
            border-radius: 50% !important;
            transition: transform 0.38s cubic-bezier(0.34, 1.56, 0.64, 1), background-color 0.35s ease, box-shadow 0.3s ease !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            box-shadow: 0 3px 8px rgba(0,0,0,0.35) !important;
        }}

        /* Knob no Modo Claro: Círculo Branco com ícone de Sol ☀️ */
        .st-key-toggle_tema input:not(:checked) + div[data-baseweb="toggle"] > div {{
            background-color: #ffffff !important;
            transform: translateX(0px) !important;
            background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="%2384cc16" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg>') !important;
            background-repeat: no-repeat !important;
            background-position: center !important;
        }}

        /* Knob no Modo Escuro: Círculo Preto com ícone de Lua e estrelas 🌙✨ */
        .st-key-toggle_tema input:checked + div[data-baseweb="toggle"] > div {{
            background-color: #051613 !important;
            transform: translateX(36px) !important;
            background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="%2338bdf8" stroke="%2338bdf8" stroke-width="1.5"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/><path d="M19 3v4"/><path d="M21 5h-4"/></svg>') !important;
            background-repeat: no-repeat !important;
            background-position: center !important;
        }}

        {css_modo_especifico}
    </style>
"""
st.markdown(css_tema, unsafe_allow_html=True)

# -------------------------------------------------------------
# FUNÇÕES DE CARREGAMENTO DE DADOS
# -------------------------------------------------------------
@st.cache_data
def get_sheet_names(file_path, modified_time):
    return pd.ExcelFile(file_path).sheet_names

@st.cache_data
def load_sheet_data(file_path, sheet_name, modified_time):
    return pd.read_excel(file_path, sheet_name=sheet_name)

# =============================================================
# 1. CÁLCULO DE RECICLAGEM
# =============================================================
if pagina_limpa == "Cálculo de Reciclagem":
    col_header_txt, col_header_admin = st.columns([4, 1])
    with col_header_txt:
        st.markdown("<h2 style='padding-top: 10px;'>♻️ Cálculo de Reciclagem</h2>", unsafe_allow_html=True)
    with col_header_admin:
        st.markdown(f"<div style='text-align: right; padding-top: 20px; color: {'#94a3b8' if modo_escuro else '#64748b'};'>👤 Admin</div>", unsafe_allow_html=True)
        
    st.markdown("---")
    st.markdown("Insira os dados semanais abaixo para obter o diagnóstico e as taxas de eficiência de reciclagem da cooperativa.")
    
    with st.form("form_calculo_reciclagem"):
        st.subheader("Entrada de Dados (Semanal)")
        
        col1, col2 = st.columns(2)
        with col1:
            lixo_domiciliar = st.number_input("Lixo domiciliar no Aterro (kg)", min_value=0.0, value=0.0, step=100.0)
            outros_residuos = st.number_input("Outros resíduos no Aterro (kg)", min_value=0.0, value=0.0, step=10.0)
            total_caminhoes = st.number_input("Total de caminhões que entraram no Aterro", min_value=1, value=1, step=1)
            
        with col2:
            coleta_seletiva = st.number_input("Entrada de Coleta Seletiva na Cooperativa (kg)", min_value=0.0, value=0.0, step=10.0)
            vendas_totais = st.number_input("Total de resíduos reciclados vendidos (kg)", min_value=0.0, value=0.0, step=10.0)
            
            col2_1, col2_2 = st.columns(2)
            with col2_1:
                caminhoes_dia = st.number_input("Caminhões/dia na Coop.", min_value=0, value=3, step=1)
            with col2_2:
                dias_uteis = st.number_input("Dias úteis na semana", min_value=1, max_value=7, value=5, step=1)
                
        submit_button = st.form_submit_button("📊 Calcular Eficiência")
        
    if submit_button:
        try:
            peso_medio = (lixo_domiciliar + outros_residuos) / total_caminhoes
            descarregamento = peso_medio * caminhoes_dia * dias_uteis
            
            if descarregamento == 0:
                st.error("O descarregamento na cooperativa resultou em zero. Verifique os dados inseridos.")
            else:
                reciclado_domiciliar = vendas_totais - coleta_seletiva
                raz_dom = (reciclado_domiciliar / descarregamento) * 100
                raz_tot = (vendas_totais / descarregamento) * 100
                
                st.markdown("---")
                st.subheader("📊 Relatório de Desempenho Semanal")
                
                col_res1, col_res2, col_res3 = st.columns(3)
                col_res1.metric("Média de peso por caminhão", f"{peso_medio:,.2f} kg".replace(',', 'X').replace('.', ',').replace('X', '.'))
                col_res2.metric("Descarregamento na Coop.", f"{descarregamento:,.2f} kg".replace(',', 'X').replace('.', ',').replace('X', '.'))
                col_res3.metric("Reciclados Domiciliares", f"{reciclado_domiciliar:,.2f} kg".replace(',', 'X').replace('.', ',').replace('X', '.'))
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                col_res4, col_res5 = st.columns(2)
                col_res4.info(f"**🟢 Razão Reciclado / Lixo Domiciliar:** {raz_dom:,.2f}%".replace(',', 'X').replace('.', ',').replace('X', '.'))
                col_res5.info(f"**🔵 Razão Reciclado / Lixo Total:** {raz_tot:,.2f}%".replace(',', 'X').replace('.', ',').replace('X', '.'))
                
        except Exception as e:
            st.error(f"Erro no cálculo: {e}")

# =============================================================
# 2. DASHBOARD DE CONTROLE
# =============================================================
elif pagina_limpa == "Dashboard de Controle":
    col_header_txt, col_header_admin = st.columns([4, 1])
    with col_header_txt:
        st.markdown("<h2 style='padding-top: 10px;'>📊 Dashboard de Controle</h2>", unsafe_allow_html=True)
    with col_header_admin:
        st.markdown(f"<div style='text-align: right; padding-top: 20px; color: {'#94a3b8' if modo_escuro else '#64748b'};'>👤 Admin</div>", unsafe_allow_html=True)
        
    st.markdown("---")
    
    if os.path.exists(FILE_PATH):
        file_mtime = os.path.getmtime(FILE_PATH)
        sheet_names = get_sheet_names(FILE_PATH, file_mtime)
        
        mes_padrao = sheet_names[0]
        df_temp = load_sheet_data(FILE_PATH, mes_padrao, file_mtime)
        dias_idx = df_temp.index[df_temp.iloc[:, 0] == 'DIAS'].tolist()
        all_categories = []
        if dias_idx:
            start_row = dias_idx[0] + 2
            for i in range(start_row, len(df_temp)):
                cat = str(df_temp.iloc[i, 0]).strip()
                if cat == 'nan' or cat == 'None' or cat == '' or cat.startswith('SOMA') or cat.startswith('TEMPO') or cat.startswith('DIST'):
                    break
                all_categories.append(cat)
                
        col_filtro1, col_filtro2 = st.columns([1, 3])
        with col_filtro1:
            mes_selecionado = st.selectbox("📅 Período (Mês)", sheet_names)
        with col_filtro2:
            categorias_selecionadas = st.multiselect(
                "🏷️ Categorias (Filtro Geral)",
                options=all_categories,
                default=all_categories
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
    
        df = load_sheet_data(FILE_PATH, mes_selecionado, file_mtime)
        dias_idx = df.index[df.iloc[:, 0] == 'DIAS'].tolist()
        
        if dias_idx and categorias_selecionadas:
            start_row = dias_idx[0] + 2 
            
            days_numbers = df.iloc[dias_idx[0], 1:32].astype(str).tolist()
            days_names = df.iloc[dias_idx[0] + 1, 1:32].astype(str).tolist()
            x_labels = [f"{num}<br>{name}" if name != 'nan' else str(num) for num, name in zip(days_numbers, days_names)]
            
            daily_data = []
            categories = []
            for i in range(start_row, len(df)):
                cat = str(df.iloc[i, 0]).strip()
                if cat == 'nan' or cat == 'None' or cat == '' or cat.startswith('SOMA') or cat.startswith('TEMPO') or cat.startswith('DIST'):
                    break
                categories.append(cat)
                row_vals = df.iloc[i, 1:32].values
                daily_data.append(row_vals)
                
            df_daily = pd.DataFrame(daily_data, columns=x_labels, index=categories)
            df_daily = df_daily.replace(['FERIADO', 'MANUT.', 'MANUT', ' '], 0)
            df_daily = df_daily.apply(pd.to_numeric, errors='coerce').fillna(0)
            df_daily = df_daily / 1000.0  # KG to Tonnes
            
            soma_idx = df.index[df.iloc[:, 1] == 'SOMA (KG)'].tolist()
            summary_data = {}
            if soma_idx:
                soma_start = soma_idx[0] + 1
                for i in range(soma_start, len(df)):
                    cat = str(df.iloc[i, 0]).strip()
                    if cat == 'nan' or cat == 'None' or cat == '':
                        break
                    try:
                        val = pd.to_numeric(df.iloc[i, 1], errors='coerce') / 1000.0
                        if pd.notna(val):
                            summary_data[cat] = val
                    except:
                        pass
                        
            df_daily_filtered = df_daily.loc[categorias_selecionadas]
            
            # KPI Cards
            num_cards = min(len(categorias_selecionadas), 5) 
            if num_cards > 0:
                cols_kpi = st.columns(num_cards)
                for i in range(num_cards):
                    cat = categorias_selecionadas[i]
                    if summary_data and cat in summary_data:
                        val = summary_data[cat]
                    else:
                        val = df_daily_filtered.loc[cat].sum()
                        
                    with cols_kpi[i]:
                        val_format = f"{float(val):,.2f} t".replace(',', 'X').replace('.', ',').replace('X', '.')
                        st.metric(label=cat, value=val_format)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Gráficos
            st.subheader("Evolução Diária do Peso (Toneladas)")
            
            selected_category = st.session_state.get("categoria_focada", None)
            
            df_plot = df_daily_filtered.T.reset_index()
            df_plot = df_plot.rename(columns={'index': 'Dia'})
            
            fig1 = px.bar(df_plot, x='Dia', y=categorias_selecionadas, barmode='group',
                          labels={'value': 'Toneladas', 'variable': 'Categoria'},
                          color_discrete_sequence=cores_paleta,
                          template=plotly_template)
            
            for trace in fig1.data:
                trace.hovertemplate = f"<b>{trace.name}</b><br>Pesagem: %{{y:.2f}} t<extra></extra>"
                if selected_category:
                    if trace.name == selected_category:
                        trace.marker.opacity = 1.0
                    else:
                        trace.marker.opacity = 0.22
                else:
                    trace.marker.opacity = 1.0

            fig1.update_layout(
                hovermode='closest',
                clickmode='event+select',
                xaxis=dict(tickangle=0),
                margin=dict(l=0, r=0, t=30, b=0),
                legend=dict(title_text="", itemclick="toggleothers", itemdoubleclick="toggle")
            )
            aplicar_estilo_grafico(fig1)
            
            if selected_category:
                col_sel_info, col_sel_btn = st.columns([4, 1])
                with col_sel_info:
                    st.caption(f"🔍 Destaque: **{selected_category}** (as demais categorias estão esmaecidas).")
                with col_sel_btn:
                    if st.button("Restaurar todas", key="btn_clear_focus"):
                        st.session_state["categoria_focada"] = None
                        st.session_state["last_handled_point"] = None
                        st.rerun()

            chart_event = st.plotly_chart(
                fig1, 
                use_container_width=True, 
                on_select="rerun", 
                selection_mode=["points"],
                key="grafico_evolucao"
            )
            
            if chart_event and hasattr(chart_event, 'get'):
                sel = chart_event.get("selection", {})
                pts = sel.get("points", [])
                if pts:
                    curve_idx = pts[0].get("curve_number")
                    point_idx = pts[0].get("point_index")
                    point_id = (curve_idx, point_idx)
                    
                    if point_id != st.session_state.get("last_handled_point"):
                        st.session_state["last_handled_point"] = point_id
                        if curve_idx is not None and curve_idx < len(fig1.data):
                            clicked_cat = fig1.data[curve_idx].name
                            if clicked_cat == selected_category:
                                st.session_state["categoria_focada"] = None
                            else:
                                st.session_state["categoria_focada"] = clicked_cat
                            st.rerun()
                else:
                    if st.session_state.get("last_handled_point") is not None and not selected_category:
                        st.session_state["last_handled_point"] = None
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            col_grafico2, col_tabela = st.columns(2)
            with col_grafico2:
                st.subheader("Distribuição por Categoria")
                totals = df_daily_filtered.sum(axis=1).reset_index()
                totals.columns = ['Categoria', 'Total (Toneladas)']
                fig2 = px.pie(totals, names='Categoria', values='Total (Toneladas)', hole=0.4,
                              color_discrete_sequence=cores_paleta,
                              template=plotly_template)
                fig2.update_traces(
                    textposition='inside', 
                    textinfo='percent+label',
                    hovertemplate="<b>%{label}</b><br>Pesagem: %{value:.2f} t<extra></extra>"
                )
                fig2.update_layout(margin=dict(l=0, r=0, t=30, b=0))
                aplicar_estilo_grafico(fig2)
                st.plotly_chart(fig2, use_container_width=True)
                
            with col_tabela:
                st.subheader("Registros Diários")
                st.dataframe(df_daily_filtered.T.style.format("{:,.2f}"), use_container_width=True, height=350)
        
        elif not categorias_selecionadas:
            st.warning("Selecione ao menos uma categoria para visualizar os dados.")
        else:
            st.error("Formato de planilha não reconhecido. Certifique-se de que a planilha possui a estrutura correta (linha 'DIAS').")
    else:
        st.error(f"Arquivo não encontrado: {FILE_PATH}. Por favor, verifique o diretório.")

# =============================================================
# 3. GESTÃO DE EFLUENTES
# =============================================================
elif pagina_limpa == "Gestão de Efluentes":
    col_header_txt, col_header_admin = st.columns([4, 1])
    with col_header_txt:
        st.markdown("<h2 style='padding-top: 10px;'>💧 Gestão de Efluentes</h2>", unsafe_allow_html=True)
    with col_header_admin:
        st.markdown(f"<div style='text-align: right; padding-top: 20px; color: {'#94a3b8' if modo_escuro else '#64748b'};'>👤 Admin</div>", unsafe_allow_html=True)
        
    st.markdown("---")
    
    sub_tab1, sub_tab2 = st.tabs([
        "🌊 Balanço Hídrico das Lagoas", 
        "⛈️ Previsão Meteorológica e Risco de Transbordamento"
    ])
    
    with sub_tab1:
        st.markdown("### Monitoramento Operacional das Lagoas de Lixiviado")
        st.caption("Acompanhamento volumétrico, vazão de recirculação e capacidade disponível do sistema de lagoas de chorume.")
        
        col_b1, col_b2, col_b3, col_b4 = st.columns(4)
        with col_b1:
            st.metric("Nível Atual das Lagoas", "64.8 %", "-1.2 % (Estável)")
        with col_b2:
            st.metric("Volume Armazenado", "4.536 m³", "Capacidade: 7.000 m³")
        with col_b3:
            st.metric("Geração / Entrada Média", "42.5 m³/dia", "+3.1 m³")
        with col_b4:
            st.metric("Tratamento / Recirculação", "48.0 m³/dia", "Balanço Positivo")
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        dias_sim = [f"Dia {i}" for i in range(1, 16)]
        vol_lagoa1 = [4200, 4250, 4310, 4290, 4380, 4420, 4400, 4450, 4510, 4490, 4520, 4560, 4540, 4520, 4536]
        cota_seguranca = [5800] * 15
        capacidade_max = [7000] * 15
        
        df_lagoas = pd.DataFrame({
            "Dia": dias_sim,
            "Volume Efetivo (m³)": vol_lagoa1,
            "Cota de Alerta (m³)": cota_seguranca,
            "Capacidade Máxima (m³)": capacidade_max
        })
        
        fig_hidrico = go.Figure()
        fig_hidrico.add_trace(go.Scatter(
            x=df_lagoas["Dia"], y=df_lagoas["Volume Efetivo (m³)"], 
            name="Volume Efetivo", mode="lines+markers",
            line=dict(color="#10b981", width=3),
            fill='tozeroy', fillcolor='rgba(16, 185, 129, 0.15)'
        ))
        fig_hidrico.add_trace(go.Scatter(
            x=df_lagoas["Dia"], y=df_lagoas["Cota de Alerta (m³)"], 
            name="Limite de Alerta Operacional", mode="lines",
            line=dict(color="#f59e0b", width=2, dash="dash")
        ))
        fig_hidrico.add_trace(go.Scatter(
            x=df_lagoas["Dia"], y=df_lagoas["Capacidade Máxima (m³)"], 
            name="Capacidade Máxima Estrutural", mode="lines",
            line=dict(color="#ef4444", width=2, dash="dot")
        ))
        
        fig_hidrico.update_layout(
            title="Evolução Volumétrica do Sistema de Lagoas (Últimos 15 Dias)",
            xaxis_title="Período de Monitoramento",
            yaxis_title="Volume Acumulado (m³)",
            template=plotly_template,
            hovermode="x unified",
            margin=dict(l=0, r=0, t=40, b=0)
        )
        aplicar_estilo_grafico(fig_hidrico)
        st.plotly_chart(fig_hidrico, use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.subheader("📋 Registro Físico-Químico e Vazões Recentes")
        df_quali = pd.DataFrame({
            "Data": ["08/10/2026", "07/10/2026", "06/10/2026", "05/10/2026", "04/10/2026"],
            "Unidade": ["Lagoa de Acumulação 01", "Lagoa de Acumulação 01", "Lagoa 02 (Polimento)", "Lagoa 02 (Polimento)", "Lagoa de Acumulação 01"],
            "Nível Borda Livre (m)": [1.38, 1.40, 1.55, 1.58, 1.42],
            "pH": [7.8, 7.9, 7.6, 7.7, 8.0],
            "DQO (mg/L)": [4200, 4350, 890, 850, 4400],
            "Vazão Bombeada (m³/d)": [48.0, 47.5, 52.0, 50.0, 46.0],
            "Status Operacional": ["🟢 Normal", "🟢 Normal", "🟢 Normal", "🟢 Normal", "🟢 Normal"]
        })
        st.dataframe(df_quali, use_container_width=True)

    with sub_tab2:
        st.markdown("### Diagnóstico Meteorológico & Análise Preventiva de Borda Livre")
        st.caption("Cruzamento de dados pluviométricos previstos para a microrregião de Catalão com a capacidade de retenção hidráulica.")
        
        col_m1, col_m2 = st.columns([1, 2])
        with col_m1:
            st.success("### 🟢 RISCO BAIXO\n**Borda Livre Atual: 1.38 metros**\n\nNenhuma probabilidade de extravasamento nos próximos 7 dias sob as condições climáticas estimadas.")
            st.metric("Chuva Acumulada Prevista (7 dias)", "34.5 mm", "Dentro da média")
            st.metric("Capacidade de Retenção Residual", "2.464 m³", "Margem Segura")
            
        with col_m2:
            st.markdown("#### Precipitação Prevista — Próximos 7 Dias (Catalão/GO)")
            dias_meteo = ["Hoje (Qui)", "Sex", "Sáb", "Dom", "Seg", "Ter", "Qua"]
            chuva_mm = [2.0, 5.5, 14.0, 8.0, 3.0, 1.5, 0.5]
            
            fig_chuva = px.bar(
                x=dias_meteo, y=chuva_mm,
                labels={"x": "Dia", "y": "Precipitação (mm)"},
                color=chuva_mm,
                color_continuous_scale="Teal",
                template=plotly_template
            )
            fig_chuva.update_layout(
                margin=dict(l=0, r=0, t=30, b=0),
                coloraxis_showscale=False
            )
            fig_chuva.update_traces(
                hovertemplate="<b>%{x}</b><br>Precipitação: %{y:.1f} mm<extra></extra>"
            )
            aplicar_estilo_grafico(fig_chuva)
            st.plotly_chart(fig_chuva, use_container_width=True)
            
        st.markdown("---")
        
        st.subheader("⚡ Simulador de Estresse Hídrico / Chuva Intensa")
        st.markdown("Selecione um volume hipotético de chuva para simular a resposta imediata da lagoa:")
        
        chuva_simulada = st.slider("Simular tempestade súbita em 24h (mm de chuva):", min_value=0, max_value=120, value=45, step=5)
        
        area_captacao = 25000 # m²
        runoff = 0.65
        aporte_estimado_m3 = (area_captacao * (chuva_simulada / 1000.0)) * runoff
        volume_pos_chuva = 4536 + aporte_estimado_m3
        nivel_pos_chuva = (volume_pos_chuva / 7000) * 100
        borda_restante = max(0.0, 1.38 - (aporte_estimado_m3 / 1800))
        
        col_s1, col_s2, col_s3 = st.columns(3)
        col_s1.metric("Aporte de Água Pluvial Gerado", f"{aporte_estimado_m3:,.1f} m³".replace(',', 'X').replace('.', ',').replace('X', '.'))
        col_s2.metric("Ocupação Projetada da Lagoa", f"{nivel_pos_chuva:.1f} %")
        col_s3.metric("Borda Livre Resultante", f"{borda_restante:.2f} m", "Segurança: > 0.80 m")
        
        if borda_restante >= 0.80:
            st.info("✅ **Conclusão:** O sistema possui capacidade de amortecimento suficiente. Nenhuma ação de emergência necessária.")
        else:
            st.warning("⚠️ **Atenção:** A borda livre simulada atinge níveis de alerta. Recomenda-se acionar recirculação preventiva nas frentes de aterro.")

# =============================================================
# 4. PAINEL DE ENGENHARIA - SUBTÓPICO 1: VIDA ÚTIL
# =============================================================
elif "Vida Útil" in pagina_limpa or pagina_limpa == "Painel de Engenharia ▴":
    col_header_txt, col_header_admin = st.columns([4, 1])
    with col_header_txt:
        st.markdown("<h2 style='padding-top: 10px;'>⚙️ Painel de Engenharia — Vida Útil</h2>", unsafe_allow_html=True)
        st.caption("Acompanhamento volumétrico, taxas de preenchimento e horizonte de vida útil das células e jazida de solo.")
    with col_header_admin:
        st.markdown(f"<div style='text-align: right; padding-top: 20px; color: {'#94a3b8' if modo_escuro else '#64748b'};'>👤 Admin</div>", unsafe_allow_html=True)
        
    st.markdown("---")
    
    tab_inertes, tab_celula2a, tab_jazida = st.tabs([
        "🧱 Vida Útil da Célula de Inertes",
        "🏗️ Vida Útil da Célula 2A",
        "⛰️ Vida Útil da Jazida de Terra"
    ])
    
    # -------------------------------------------------------------
    # ABA 1: Vida Útil da Célula de Inertes
    # -------------------------------------------------------------
    with tab_inertes:
        st.markdown("### Capacidade & Vida Útil — Célula de Resíduos Inertes (Classe II-B)")
        st.caption("Monitoramento volumétrico de materiais inertes de construção civil (RCD), escavação, concretos e cerâmicas no aterro de Catalão.")
        
        col_ci1, col_ci2, col_ci3, col_ci4 = st.columns(4)
        with col_ci1:
            st.metric("Vida Útil Estimada", "11.8 anos", "Projeção: até 2038")
        with col_ci2:
            st.metric("Capacidade Total Licenciada", "250.000 m³", "Outorga SEMAD/GO")
        with col_ci3:
            st.metric("Volume Ocupado Acumulado", "67.500 m³", "27.0% preenchido")
        with col_ci4:
            st.metric("Volume Disponível", "182.500 m³", "73.0% remanescente")
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_ci_g1, col_ci_g2 = st.columns([2, 1])
        with col_ci_g1:
            st.subheader("Curva de Preenchimento Volumétrico (Inertes)")
            anos_ci = [2022, 2023, 2024, 2025, 2026, 2028, 2030, 2032, 2034, 2036, 2038]
            vol_ci_hist = [12000, 25000, 39000, 53000, 67500]
            vol_ci_proj = [67500, 98000, 130000, 165000, 202000, 235000, 250000]
            cap_max_ci = [250000] * len(anos_ci)
            
            fig_ci = go.Figure()
            fig_ci.add_trace(go.Scatter(
                x=anos_ci[:5], y=vol_ci_hist,
                name="Volume Inerte Disposto (Histórico)",
                mode="lines+markers",
                line=dict(color="#10b981", width=3),
                fill='tozeroy', fillcolor='rgba(16, 185, 129, 0.15)'
            ))
            fig_ci.add_trace(go.Scatter(
                x=anos_ci[4:], y=vol_ci_proj,
                name="Projeção de Preenchimento",
                mode="lines+markers",
                line=dict(color="#38bdf8", width=3, dash="dash")
            ))
            fig_ci.add_trace(go.Scatter(
                x=anos_ci, y=cap_max_ci,
                name="Capacidade Máxima Licenciada (250k m³)",
                mode="lines",
                line=dict(color="#ef4444", width=2, dash="dot")
            ))
            fig_ci.update_layout(
                xaxis_title="Ano",
                yaxis_title="Volume Acumulado (m³)",
                template=plotly_template,
                hovermode="x unified",
                margin=dict(l=0, r=0, t=30, b=0)
            )
            aplicar_estilo_grafico(fig_ci)
            st.plotly_chart(fig_ci, use_container_width=True)
            
        with col_ci_g2:
            st.subheader("Composição dos Inertes Dispostos")
            fig_comp_ci = px.pie(
                values=[42, 28, 18, 12],
                names=["Concreto & Alvenaria", "Solos & Cascalho", "Cerâmicas & Telhas", "Outros Inertes"],
                hole=0.45,
                color_discrete_sequence=['#187264', '#2dd4bf', '#38bdf8', '#94a3b8'] if modo_escuro else ['#187264', '#2a9d8f', '#0284c7', '#64748b'],
                template=plotly_template
            )
            fig_comp_ci.update_traces(textposition='inside', textinfo='percent+label')
            aplicar_estilo_grafico(fig_comp_ci)
            st.plotly_chart(fig_comp_ci, use_container_width=True)
            
        st.markdown("---")
        st.subheader("📋 Parâmetros Operacionais e Geotécnicos da Célula de Inertes")
        df_ci_oper = pd.DataFrame({
            "Parâmetro": [
                "Taxa Média de Recebimento",
                "Densidade Aparente no Maciço",
                "Cota Atual do Platô",
                "Cota Final de Projeto",
                "Fator de Segurança Geotécnico (Taludes)",
                "Sistema de Drenagem Superficial"
            ],
            "Valor Atual": [
                "~490 m³/mês (~685 t/mês)",
                "1,40 t/m³ (Compactado com Trator de Esteira)",
                "824,50 m (Nível do Mar)",
                "840,00 m (Nível do Mar)",
                "FS = 1,85 (Norma ABNT NBR 11682: Estável)",
                "Canaletas em concreto e bacia de sedimentação ativas"
            ],
            "Status Operacional": [
                "🟢 Fluxo regular",
                "🟢 Dentro do padrão",
                "🟢 Em elevação controlada",
                "🔵 15,5 m disponíveis até o topo",
                "🟢 Geotecnia aprovada",
                "🟢 Manutenção preventiva em dia"
            ]
        })
        st.dataframe(df_ci_oper, use_container_width=True)

    # -------------------------------------------------------------
    # ABA 2: Vida Útil da Célula 2A
    # -------------------------------------------------------------
    with tab_celula2a:
        st.markdown("### Capacidade & Saturação Volumétrica — Célula 2A (Classe II-A Ativa)")
        st.caption("Acompanhamento da célula operacional principal de resíduos domiciliares e comerciais, taxas de adensamento e transição.")
        
        col_c2_1, col_c2_2, col_c2_3, col_c2_4 = st.columns(4)
        with col_c2_1:
            st.metric("Vida Útil Restante", "2.8 anos", "Término previsto: Mar/2029")
        with col_c2_2:
            st.metric("Capacidade Total Licenciada", "420.000 m³", "Geomembrana PEAD 2.0mm")
        with col_c2_3:
            st.metric("Volume Já Disposto", "188.200 m³", "44.8% ocupado")
        with col_c2_4:
            st.metric("Volume Disponível para Disposição", "231.800 m³", "55.2% livre")
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_c2_g1, col_c2_g2 = st.columns([2, 1])
        with col_c2_g1:
            st.subheader("Curva de Elevação e Preenchimento — Célula 2A (2023 - 2029)")
            anos_c2 = [2023, 2024, 2025, 2026, 2027, 2028, 2029]
            vol_c2_hist = [45000, 95000, 142000, 188200]
            vol_c2_proj = [188200, 265000, 345000, 420000]
            cap_max_c2 = [420000] * len(anos_c2)
            
            fig_c2 = go.Figure()
            fig_c2.add_trace(go.Scatter(
                x=anos_c2[:4], y=vol_c2_hist,
                name="Volume Acumulado Real (Histórico)",
                mode="lines+markers",
                line=dict(color="#187264", width=3),
                fill='tozeroy', fillcolor='rgba(24, 114, 100, 0.15)'
            ))
            fig_c2.add_trace(go.Scatter(
                x=anos_c2[3:], y=vol_c2_proj,
                name="Projeção até a Saturação",
                mode="lines+markers",
                line=dict(color="#f59e0b", width=3, dash="dash")
            ))
            fig_c2.add_trace(go.Scatter(
                x=anos_c2, y=cap_max_c2,
                name="Cota Máxima da Célula 2A (420k m³)",
                mode="lines",
                line=dict(color="#ef4444", width=2, dash="dot")
            ))
            fig_c2.update_layout(
                xaxis_title="Ano",
                yaxis_title="Volume Acumulado (m³)",
                template=plotly_template,
                hovermode="x unified",
                margin=dict(l=0, r=0, t=30, b=0)
            )
            aplicar_estilo_grafico(fig_c2)
            st.plotly_chart(fig_c2, use_container_width=True)
            
        with col_c2_g2:
            st.subheader("Balanço de Ocupação da Célula 2A")
            fig_bal_c2 = px.pie(
                values=[188200, 231800],
                names=["Ocupado (188.2k m³)", "Disponível (231.8k m³)"],
                hole=0.45,
                color_discrete_sequence=['#187264', '#2dd4bf'] if modo_escuro else ['#187264', '#2a9d8f'],
                template=plotly_template
            )
            fig_bal_c2.update_traces(textposition='inside', textinfo='percent+label')
            aplicar_estilo_grafico(fig_bal_c2)
            st.plotly_chart(fig_bal_c2, use_container_width=True)
            
        st.markdown("---")
        st.subheader("🧭 Cronograma de Transição de Fases do Maciço Sanitário")
        df_fases_aterro = pd.DataFrame({
            "Fase / Célula": ["Célula 01", "Célula 2A (Em Operação)", "Célula 03 (Futura)"],
            "Capacidade de Projeto": ["300.000 m³", "420.000 m³", "480.000 m³"],
            "Situação Atual": ["Saturada e Encerrada", "Operação ativa com 44.8% de volume", "Terraplenagem e Licenciamento Executivo"],
            "Período de Operação": ["2018 a 2023", "2023 a Mar/2029 (~2.8 anos restantes)", "Previsão 2029 a 2035 (~6 anos)"],
            "Ações Técnicas Imediatas": [
                "Monitoramento de recalque e drenagem de biogás",
                "Compactação diária e controle de percolado",
                "Instalação do liner PEAD programada para 2028"
            ]
        })
        st.dataframe(df_fases_aterro, use_container_width=True)

    # -------------------------------------------------------------
    # ABA 3: Vida Útil da Jazida de Terra
    # -------------------------------------------------------------
    with tab_jazida:
        st.markdown("### Autonomia & Reserva Mineral — Jazida de Terra de Empréstimo")
        st.caption("Balanço volumétrico da jazida interna para selagem diária das frentes de resíduos, regularização de bermas e taludes.")
        
        col_jz1, col_jz2, col_jz3, col_jz4 = st.columns(4)
        with col_jz1:
            st.metric("Vida Útil da Jazida", "6.5 anos", "Autonomia de cobertura até 2033")
        with col_jz2:
            st.metric("Reserva Total Licenciada", "320.000 m³", "Área demarcada no aterro")
        with col_jz3:
            st.metric("Solo Já Extraído / Lavrado", "128.000 m³", "40.0% lavrado")
        with col_jz4:
            st.metric("Reserva de Solo Remanescente", "192.000 m³", "60.0% disponível em jazida")
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_jz_g1, col_jz_g2 = st.columns([2, 1])
        with col_jz_g1:
            st.subheader("Evolução da Lavra & Reserva Remanescente de Terra (2022 - 2033)")
            anos_jz = [2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033]
            solo_extraido_hist = [24000, 52000, 80000, 105000, 128000]
            solo_extraido_proj = [128000, 155000, 183000, 212000, 243000, 275000, 305000, 320000]
            
            fig_jz = go.Figure()
            fig_jz.add_trace(go.Scatter(
                x=anos_jz[:5], y=solo_extraido_hist,
                name="Solo Já Extraído (m³)",
                mode="lines+markers",
                line=dict(color="#f59e0b", width=3),
                fill='tozeroy', fillcolor='rgba(245, 158, 11, 0.15)'
            ))
            fig_jz.add_trace(go.Scatter(
                x=anos_jz[4:], y=solo_extraido_proj,
                name="Projeção de Consumo de Solo",
                mode="lines+markers",
                line=dict(color="#38bdf8", width=3, dash="dash")
            ))
            fig_jz.add_trace(go.Scatter(
                x=anos_jz, y=[320000] * len(anos_jz),
                name="Reserva Total da Jazida (320k m³)",
                mode="lines",
                line=dict(color="#ef4444", width=2, dash="dot")
            ))
            fig_jz.update_layout(
                xaxis_title="Ano",
                yaxis_title="Volume Acumulado de Solo (m³)",
                template=plotly_template,
                hovermode="x unified",
                margin=dict(l=0, r=0, t=30, b=0)
            )
            aplicar_estilo_grafico(fig_jz)
            st.plotly_chart(fig_jz, use_container_width=True)
            
        with col_jz_g2:
            st.subheader("Aplicação do Solo Extraído")
            fig_ap_jz = px.pie(
                values=[65, 15, 12, 8],
                names=["Cobertura Diária (Célula 2A)", "Diques & Taludes", "Selagem Célula Inertes", "Obras & Manutenção"],
                hole=0.45,
                color_discrete_sequence=['#f59e0b', '#187264', '#2dd4bf', '#94a3b8'] if modo_escuro else ['#d97706', '#187264', '#2a9d8f', '#64748b'],
                template=plotly_template
            )
            fig_ap_jz.update_traces(textposition='inside', textinfo='percent+label')
            aplicar_estilo_grafico(fig_ap_jz)
            st.plotly_chart(fig_ap_jz, use_container_width=True)
            
        st.markdown("---")
        st.subheader("📋 Balanço de Consumo de Solo & Controle Geotécnico")
        df_jz_ctrl = pd.DataFrame({
            "Indicador de Lavra": [
                "Fator Solo / Lixo (Taxa de Cobertura Diária)",
                "Consumo Mensal Médio de Solo",
                "Espessura Média da Selagem Diária",
                "Classificação Geotécnica do Solo",
                "Permeabilidade Hidráulica (k)",
                "Plano de Recuperação da Área Degradada (PRAD)"
            ],
            "Valor / Especificação": [
                "1 : 5 (20% do volume do resíduo)",
                "~1.450 m³/mês",
                "15 a 20 cm compactados",
                "Argila silto-arenosa (alta coesão)",
                "k < 10⁻⁷ cm/s (Excelente impermeabilização natural)",
                "Revegetação e drenagem das bermas de corte em conformidade"
            ],
            "Avaliação Técnica": [
                "🟢 Consumo otimizado",
                "🟢 Cobertura garantida",
                "🟢 Conforme norma NBR 8419",
                "🟢 Adequado para selagem",
                "🟢 Barreira contra odores/água pluvial",
                "🟢 Aprovado pela SEMAD"
            ]
        })
        st.dataframe(df_jz_ctrl, use_container_width=True)

# =============================================================
# 4. PAINEL DE ENGENHARIA - SUBTÓPICO 2: CALENDÁRIO AMBIENTAL
# =============================================================
elif "Calendário Ambiental" in pagina_limpa:
    col_header_txt, col_header_admin = st.columns([4, 1])
    with col_header_txt:
        st.markdown("<h2 style='padding-top: 10px;'>⚙️ Painel de Engenharia — Calendário Ambiental</h2>", unsafe_allow_html=True)
        st.caption("Acompanhamento de obrigações perante os órgãos reguladores (SEMAD / IBAMA / Prefeitura) e auditorias periódicas.")
    with col_header_admin:
        st.markdown(f"<div style='text-align: right; padding-top: 20px; color: {'#94a3b8' if modo_escuro else '#64748b'};'>👤 Admin</div>", unsafe_allow_html=True)
        
    st.markdown("---")
    
    col_ca1, col_ca2, col_ca3, col_ca4 = st.columns(4)
    with col_ca1:
        st.metric("Licença de Operação (L.O.)", "Vigente", "Validade: Nov/2028")
    with col_ca2:
        st.metric("Condicionantes em Dia", "100 %", "18 de 18 cumpridas")
    with col_ca3:
        st.metric("Próxima Entrega Legal", "7 dias", "15/10/2026")
    with col_ca4:
        st.metric("Auditoria Externa", "45 dias", "Previsão Nov/2026")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.subheader("📅 Cronograma Anual de Condicionantes e Obrigações Ambientais (2026 / 2027)")
    
    col_filtro_ca1, col_filtro_ca2 = st.columns([1, 2])
    with col_filtro_ca1:
        filtro_status = st.selectbox("Filtrar por Status:", ["Todos", "🟡 Prazo Próximo", "🔵 Programado", "🟢 Concluído"])
        
    df_calendario = pd.DataFrame([
        {
            "Prazo Limite": "15/10/2026",
            "Obrigação / Condicionante": "Coleta e Análise Laboratorial de Águas Subterrâneas (Poços Piezométricos)",
            "Órgão / Destino": "SEMAD / GO",
            "Frequência": "Trimestral",
            "Responsável": "Laboratório Ambiental / Eng. Química",
            "Status": "🟡 Prazo Próximo"
        },
        {
            "Prazo Limite": "30/10/2026",
            "Obrigação / Condicionante": "Relatório Mensal de Balanço Hídrico e Recirculação de Lixiviado",
            "Órgão / Destino": "SEMAD / GO",
            "Frequência": "Mensal",
            "Responsável": "Engenharia de Operações",
            "Status": "🔵 Programado"
        },
        {
            "Prazo Limite": "15/11/2026",
            "Obrigação / Condicionante": "Monitoramento Semestral de Emissões de Biogás e Eficiência do Queimador (Flare)",
            "Órgão / Destino": "SEMAD / GO",
            "Frequência": "Semestral",
            "Responsável": "Consultoria de Emissões Atmosféricas",
            "Status": "🔵 Programado"
        },
        {
            "Prazo Limite": "10/12/2026",
            "Obrigação / Condicionante": "Laudo Semestral de Estabilidade Geotécnica de Taludes e Acompanhamento de Recalque",
            "Órgão / Destino": "SEMAD / Defesa Civil",
            "Frequência": "Semestral",
            "Responsável": "Engenharia Geotécnica",
            "Status": "🔵 Programado"
        },
        {
            "Prazo Limite": "31/01/2027",
            "Obrigação / Condicionante": "Inventário Anual de Resíduos Sólidos Dispostos e Triados",
            "Órgão / Destino": "Prefeitura de Catalão",
            "Frequência": "Anual",
            "Responsável": "Gerência de Operações",
            "Status": "🔵 Programado"
        },
        {
            "Prazo Limite": "31/03/2027",
            "Obrigação / Condicionante": "Relatório Anual de Atividades Potencialmente Poluidoras (RAPP)",
            "Órgão / Destino": "IBAMA",
            "Frequência": "Anual",
            "Responsável": "Departamento Jurídico-Ambiental",
            "Status": "🔵 Programado"
        },
        {
            "Prazo Limite": "30/09/2026",
            "Obrigação / Condicionante": "Renovação e Calibração Periódica das Células de Carga da Balança Rodoviária",
            "Órgão / Destino": "IPEM / INMETRO",
            "Frequência": "Anual",
            "Responsável": "Manutenção Metrológica",
            "Status": "🟢 Concluído"
        }
    ])
    
    if filtro_status != "Todos":
        df_calendario = df_calendario[df_calendario["Status"] == filtro_status]
        
    st.dataframe(df_calendario, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("💡 **Aviso Executivo:** As condicionantes ambientais possuem protocolo com 15 dias de antecedência mínima para validação do responsável técnico perante a SEMAD.")

# =============================================================
# 5. PAINEL EXECUTIVO
# =============================================================
elif pagina_limpa == "Painel Executivo":
    col_header_txt, col_header_admin = st.columns([4, 1])
    with col_header_txt:
        st.markdown("<h2 style='padding-top: 10px;'>💼 Painel Executivo</h2>", unsafe_allow_html=True)
    with col_header_admin:
        st.markdown(f"<div style='text-align: right; padding-top: 20px; color: {'#94a3b8' if modo_escuro else '#64748b'};'>👤 Admin</div>", unsafe_allow_html=True)
        
    st.markdown("---")
    st.markdown("Visão executiva estratégica com indicadores consolidados para tomada de decisão da diretoria e gerência geral.")
    
    col_ex1, col_ex2, col_ex3, col_ex4 = st.columns(4)
    with col_ex1:
        st.metric("Custo Médio Operacional", "R$ 49,20 / t", "-3.5% vs orçado")
    with col_ex2:
        st.metric("Disposição Total (2026)", "42.850 t", "Dentro do cronograma")
    with col_ex3:
        st.metric("Eficiência de Triagem", "98.8 %", "+0.4% no mês")
    with col_ex4:
        st.metric("Conformidade Ambiental", "100 %", "Licença Vigente")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        st.subheader("Desempenho Mensal de Resíduos Dispostos (t)")
        meses_disp = ["Maio", "Junho", "Julho", "Agosto", "Setembro"]
        ton_disp = [7120, 7450, 7890, 8120, 8350]
        fig_exec1 = px.bar(
            x=meses_disp, y=ton_disp,
            labels={"x": "Mês", "y": "Toneladas Dispostas"},
            template=plotly_template,
            color_discrete_sequence=['#187264']
        )
        fig_exec1.update_traces(
            hovertemplate="<b>%{x}</b><br>Disposição: %{y:,.0f} t<extra></extra>"
        )
        aplicar_estilo_grafico(fig_exec1)
        st.plotly_chart(fig_exec1, use_container_width=True)
        
    with col_e2:
        st.subheader("Distribuição dos Custos Operacionais")
        custos = ["Operação de Máquinas", "Mão de Obra", "Tratamento de Lixiviado", "Monitoramento Ambiental", "Manutenção"]
        valores = [38, 26, 16, 11, 9]
        fig_exec2 = px.pie(
            names=custos, values=valores, hole=0.4,
            template=plotly_template,
            color_discrete_sequence=['#187264', '#2a9d8f', '#e9c46a', '#f4a261', '#e76f51']
        )
        fig_exec2.update_traces(textposition='inside', textinfo='percent+label')
        aplicar_estilo_grafico(fig_exec2)
        st.plotly_chart(fig_exec2, use_container_width=True)
