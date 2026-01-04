import streamlit as st
import pandas as pd
import ast
import plotly.express as px

# 1. Configuração da Página
st.set_page_config(page_title="Job Hunter Skills", layout="wide", page_icon="💼")

st.title("💼 Job Hunter AI: Análise de Mercado Tech")
st.markdown("Descubra as tecnologias e skills mais pedidas nas vagas do LinkedIn.")

# 2. Carregar Dados
@st.cache_data # Isso faz o site ficar rápido, não recarrega o CSV toda hora
def load_data():
    try:
        # Tenta ler o CSV. Se não existir, cria um DataFrame vazio para não dar erro na tela
        df = pd.read_csv('dados_vagas_linkedin.csv')
        return df
    except FileNotFoundError:
        return pd.DataFrame()

df = load_data()

# 3. Verificar se tem dados
if df.empty:
    st.warning("⚠️ Nenhum dado encontrado. O arquivo 'dados_vagas_linkedin.csv' não está no repositório ou está vazio.")
    st.info("Dica: Rode o scraper localmente, gere o CSV e suba para o Hugging Face.")
    st.stop() # Para a execução aqui se não tiver dados

# 4. Limpeza e Conversão (O mesmo truque do Jupyter)
def limpar_lista(item):
    try:
        if pd.isna(item) or item == 'N/A' or item == '[]': return []
        return ast.literal_eval(item) # Converte string "['Python']" em lista ['Python']
    except: return []

# Aplica a conversão
if 'tech_stack' in df.columns:
    df['tech_stack_lista'] = df['tech_stack'].apply(limpar_lista)
if 'cloud' in df.columns:
    df['cloud_lista'] = df['cloud'].apply(limpar_lista)

# --- DASHBOARD ---

# Métricas no topo
col1, col2, col3 = st.columns(3)
col1.metric("Vagas Analisadas", len(df))
col2.metric("Localização Principal", df['local'].mode()[0] if 'local' in df.columns else "N/A")
col3.metric("Cargo Mais Comum", df['titulo'].mode()[0] if 'titulo' in df.columns else "N/A")

st.divider()

# Gráficos Lado a Lado
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🛠️ Top Tecnologias (Hard Skills)")
    if 'tech_stack_lista' in df.columns:
        # Explode a lista para contar individualmente
        tech_counts = df.explode('tech_stack_lista')['tech_stack_lista'].value_counts().head(10).reset_index()
        tech_counts.columns = ['Tecnologia', 'Contagem']
        
        # Gráfico bonito com Plotly
        fig_tech = px.bar(tech_counts, x='Contagem', y='Tecnologia', orientation='h', color='Contagem', color_continuous_scale='viridis')
        fig_tech.update_layout(yaxis={'categoryorder':'total ascending'}) # Ordenar
        st.plotly_chart(fig_tech, use_container_width=True)

with col_right:
    st.subheader("☁️ Cloud & Ferramentas")
    if 'cloud_lista' in df.columns:
        cloud_counts = df.explode('cloud_lista')['cloud_lista'].value_counts().head(10).reset_index()
        cloud_counts.columns = ['Ferramenta', 'Contagem']
        
        if not cloud_counts.empty:
            fig_cloud = px.bar(cloud_counts, x='Contagem', y='Ferramenta', orientation='h', color='Contagem', color_continuous_scale='magma')
            fig_cloud.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_cloud, use_container_width=True)
        else:
            st.info("Nenhuma ferramenta de Cloud identificada nas vagas atuais.")

# Tabela de Dados Brutos (Expansível)
with st.expander("Ver todas as vagas (Tabela)"):
    st.dataframe(df[['data_coleta', 'titulo', 'empresa', 'local', 'senioridade', 'link']])