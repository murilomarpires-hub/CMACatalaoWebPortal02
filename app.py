import streamlit as st
import pandas as pd
import plotly.express as px
import os
from streamlit_option_menu import option_menu

# App Config
st.set_page_config(page_title="Clean Master - Dashboard", page_icon="♻️", layout="wide", initial_sidebar_state="expanded")

# Inject Custom CSS
st.markdown("""
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "BALANÇA_ATERRO.xlsx")
LOGO_PATH = os.path.join(BASE_DIR, "Logo", "image (2).png")

@st.cache_data
def get_sheet_names(file_path, modified_time):
    return pd.ExcelFile(file_path).sheet_names

@st.cache_data
def load_sheet_data(file_path, sheet_name, modified_time):
    return pd.read_excel(file_path, sheet_name=sheet_name)

if os.path.exists(FILE_PATH):
    file_mtime = os.path.getmtime(FILE_PATH)
    sheet_names = get_sheet_names(FILE_PATH, file_mtime)
    
    # -------------------------------------------------------------
    # SIDEBAR
    # -------------------------------------------------------------
    with st.sidebar:
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, use_container_width=True)
            
        st.markdown("""
        <div style="background-color: #187264; border-radius: 10px; padding: 15px; margin-top: 20px; margin-bottom: 20px; color: white; display: flex; align-items: center; gap: 15px;">
            <div style="font-size: 24px;">🏢</div>
            <div>
                <div style="font-size: 10px; font-weight: bold; letter-spacing: 1px; opacity: 0.8;">EMPRESA</div>
                <div style="font-size: 16px; font-weight: bold;">Clean Master</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='font-size: 12px; font-weight: bold; margin-bottom: 10px; letter-spacing: 1px; color: gray;'>GERENCIAMENTO</div>", unsafe_allow_html=True)
        
        pagina = option_menu(
            menu_title=None,
            options=["Dashboard de Controle", "Cálculo de Reciclagem"],
            icons=["display", "calculator"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent", "border": "none"},
                "icon": {"font-size": "18px"},
                "nav-link": {"font-size": "15px", "text-align": "left", "margin": "0px", "border-radius": "8px"},
                "nav-link-selected": {"background-color": "#187264"},
            }
        )

    # Read sheet to get categories
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

    if pagina == "Dashboard de Controle":
        # -------------------------------------------------------------
        # HEADER 
        # -------------------------------------------------------------
        col_header_txt, col_header_admin = st.columns([4, 1])
        with col_header_txt:
            st.markdown("<h2 style='padding-top: 15px;'>Dashboard de Controle</h2>", unsafe_allow_html=True)
        with col_header_admin:
            st.markdown("<div style='text-align: right; padding-top: 25px; color: gray;'>👤 Admin</div>", unsafe_allow_html=True)
            
        st.markdown("---")
        
        # -------------------------------------------------------------
        # FILTERS (Date and Categories) 
        # -------------------------------------------------------------
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
    
        # Process Data for the Selected Month
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
            
            # Extract Summary
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
            
            # -------------------------------------------------------------
            # KPI CARDS 
            # -------------------------------------------------------------
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
            
            # -------------------------------------------------------------
            # CHARTS & TABLES 
            # -------------------------------------------------------------
            st.subheader("Evolução Diária do Peso (Toneladas)")
            df_plot = df_daily_filtered.T.reset_index()
            df_plot = df_plot.rename(columns={'index': 'Dia'})
            
            fig1 = px.bar(df_plot, x='Dia', y=categorias_selecionadas, barmode='group',
                          labels={'value': 'Toneladas', 'variable': 'Categoria'},
                          color_discrete_sequence=['#187264', '#2a9d8f', '#e9c46a', '#f4a261', '#e76f51', '#264653'])
            fig1.update_layout(hovermode='x unified', xaxis=dict(tickangle=0), margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig1, use_container_width=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            col_grafico2, col_tabela = st.columns(2)
            with col_grafico2:
                st.subheader("Distribuição por Categoria")
                totals = df_daily_filtered.sum(axis=1).reset_index()
                totals.columns = ['Categoria', 'Total (Toneladas)']
                fig2 = px.pie(totals, names='Categoria', values='Total (Toneladas)', hole=0.4,
                              color_discrete_sequence=['#187264', '#2a9d8f', '#e9c46a', '#f4a261', '#e76f51', '#264653'])
                fig2.update_traces(textposition='inside', textinfo='percent+label')
                fig2.update_layout(margin=dict(l=0, r=0, t=30, b=0))
                st.plotly_chart(fig2, use_container_width=True)
                
            with col_tabela:
                st.subheader("Registros Diários")
                st.dataframe(df_daily_filtered.T.style.format("{:,.2f}"), use_container_width=True, height=350)
    
        elif not categorias_selecionadas:
            st.warning("Selecione ao menos uma categoria para visualizar os dados.")
        else:
            st.error("Formato de planilha não reconhecido. Certifique-se de que a planilha possui a estrutura correta (linha 'DIAS').")

    elif pagina == "Cálculo de Reciclagem":
        col_header_txt, col_header_admin = st.columns([4, 1])
        with col_header_txt:
            st.markdown("<h2 style='padding-top: 15px;'>Cálculo de Reciclagem</h2>", unsafe_allow_html=True)
        with col_header_admin:
            st.markdown("<div style='text-align: right; padding-top: 25px; color: gray;'>👤 Admin</div>", unsafe_allow_html=True)
            
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
                # Calculations
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
                    
                    # Display results with metrics
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

else:
    st.error(f"Arquivo não encontrado: {FILE_PATH}. Por favor, verifique o diretório.")
