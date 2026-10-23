import json
import re
import streamlit as st
from openai import AzureOpenAI

# ==============================================================================
# 1. CONFIGURAÇÃO DA PÁGINA E TEMA LEVE, ALEGRE E BRANCO ☀️
# ==============================================================================
st.set_page_config(
    page_title="Neural Data Extractor ☀️",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injeção de CSS Customizado - Layout Claro, Feliz e Moderno
st.markdown("""
    <style>
    /* Importação de fontes arredondadas e amigáveis */
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600;700&family=Nunito:wght@400;600;700;800&display=swap');

    /* Fundo branco e limpo com tipografia amigável */
    .stApp {
        background-color: #f8fafc;
        color: #1e293b;
        font-family: 'Nunito', sans-serif;
    }

    /* Cabeçalhos vibrantes e amigáveis */
    h1, h2, h3, .happy-title {
        font-family: 'Fredoka', sans-serif !important;
        letter-spacing: 0.5px;
    }

    .main-header {
        font-size: 2.6rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.2rem;
        display: inline-block;
    }

    .sub-header {
        font-size: 1.1rem;
        color: #64748b;
        margin-top: 4px;
        margin-bottom: 2rem;
        border-left: 4px solid #f59e0b;
        padding-left: 12px;
        font-weight: 600;
    }

    /* Cartões Claros com Sombras Suaves */
    .happy-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01);
    }

    /* Botão Vibrante e Amigável */
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: #ffffff !important;
        font-family: 'Fredoka', sans-serif !important;
        font-weight: 600;
        font-size: 1.1rem;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
