import json
import re
import streamlit as st
from openai import AzureOpenAI

# ==============================================================================
# 1. CONFIGURAÇÃO DA PÁGINA E TEMA FUTURISTA / CYBERPUNK
# ==============================================================================
st.set_page_config(
    page_title="NEURAL-EXTRACT // Azure AI Core",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injeção de CSS Customizado para Estética Futurista / Holográfica / Cyberpunk
st.markdown("""
    <style>
    /* Importação de fontes futuristas do Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800&family=Share+Tech+Mono&display=swap');

    /* Fundo geral e tipografia principal */
    .stApp {
        background-color: #050b14;
        color: #00f0ff;
        font-family: 'Share Tech Mono', monospace;
    }

    /* Cabeçalhos futuristas */
    h1, h2, h3, .cyber-title {
        font-family: 'Orbitron', sans-serif !important;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    .main-header {
        font-size: 2.4rem;
        font-weight: 800;
        color: #00f0ff;
        text-shadow: 0 0 15px rgba(0, 240, 255, 0.6);
        margin-bottom: 0.1rem;
    }

    .sub-header {
        font-size: 1rem;
        color: #a0aec0;
        margin-bottom: 2rem;
        border-left: 3px solid #7928ca;
        padding-left: 10px;
    }

    /* Cartões Holográficos com Glassmorphism */
    .holo-card {
        background: rgba(13, 27, 42, 0.7);
        border: 1px solid rgba(0, 240, 255, 0.3);
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.1), inset 0 0 15px rgba(0, 240, 255, 0.05);
        border-radius: 12px;
        padding: 20px;
        backdrop-filter: blur(10px);
        margin-bottom: 20px;
    }

    /* Botão Cibernético */
    .stButton>button {
        background: linear-gradient(135deg, #00f0ff 0%, #7928ca 100%);
        color: #050b14 !important;
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 700;
        font-size: 1rem;
        border-radius: 6px;
        padding: 0.7rem 1.5rem;
        border: 1px solid #00f0ff;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.4);
        width: 100%;
        transition: all 0.3s ease-in-out;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stButton>button:hover {
        background: linear-gradient(135deg, #7928ca 0%, #00f0ff 100%);
        color: #ffffff !important;
        box-shadow: 0 0 25px rgba(121, 40, 202, 0.8), 0 0 10px rgba(0, 240, 255, 0.8);
        border-color: #ff007f;
    }

    /* Estilização da área de texto */
    .stTextArea textarea {
        background-color: #081120 !important;
        color: #00f0ff !important;
        border: 1px solid rgba(0, 240, 255, 0.4) !important;
        border-radius: 8px;
        font-family: 'Share Tech Mono', monospace !important;
    }

    /* Sidebar futurista */
    [data-testid="stSidebar"] {
        background-color: #03070d;
        border-right: 1px solid rgba(121, 40, 202, 0.3);
    }

    /* Badges de Urgência */
    .badge-alto {
        background: rgba(255, 0, 85, 0.2);
        border: 1px solid #ff0055;
        color: #ff0055;
        padding: 4px 10px;
        border-radius: 4px;
        font-weight: bold;
        box-shadow: 0 0 10px rgba(255, 0, 85, 0.4);
    }
    .badge-medio {
        background: rgba(255, 184, 0, 0.2);
        border: 1px solid #ffb800;
        color: #ffb800;
        padding: 4px 10px;
        border-radius: 4px;
        font-weight: bold;
        box-shadow: 0 0 10px rgba(255, 184, 0, 0.4);
    }
    .badge-baixo {
        background: rgba(0, 255, 136, 0.2);
        border: 1px solid #00ff88;
        color: #00ff88;
        padding: 4px 10px;
        border-radius: 4px;
        font-weight: bold;
        box-shadow: 0 0 10px rgba(0, 255, 136, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. SIDEBAR: GUIA DE CONFIGURAÇÃO DE SECRETS
# ==============================================================================
with st.sidebar:
    st.markdown("### 🌐 SYSTEM CONFIG")
    st.markdown("---")
    st.markdown("""
    **Azure OpenAI Neural Interface**
    
    Para conectar sua instância privada com segurança via `st.secrets`, configure localmente:
    
    **Path:** `.streamlit/secrets.toml`
    ```toml
    AZURE_OPENAI_KEY = "sua_chave_aqui"
    AZURE_OPENAI_ENDPOINT = "https://seu-recurso.services.ai.azure.com/"
    AZURE_OPENAI_DEPLOYMENT = "gpt-4.1-mini"
    ```
    """)
    st.markdown("---")
    st.caption("⚡ Status: Neural Link Pronto (Fallback Ativo)")

# ==============================================================================
# 3. TRATAMENTO DE CREDENCIAIS & SANITIZAÇÃO DE URL
# ==============================================================================
def sanitizar_url(url: str) -> str:
    # Remove entidades HTML persistentes como &quot;, aspas ou espaços em branco
    return re.sub(r'&quot;|"|\'|\s+', '', url).strip()

DEFAULT_KEY = "6t2pTNsmNafDyo53MDAFIrvvQRBZXP7dLcr5j3TLxMS34LQVq3ZUJQQJ99CHACHYHv6XJ3w3AAAAACOGT7os"
DEFAULT_ENDPOINT = "https://marcelomaffeis-05082026-resource.services.ai.azure.com/"
DEFAULT_DEPLOYMENT = "gpt-4.1-mini"

try:
    API_KEY = st.secrets.get("AZURE_OPENAI_KEY", DEFAULT_KEY)
    RAW_ENDPOINT = st.secrets.get("AZURE_OPENAI_ENDPOINT", DEFAULT_ENDPOINT)
    DEPLOYMENT_NAME = st.secrets.get("AZURE_OPENAI_DEPLOYMENT", DEFAULT_DEPLOYMENT)
except Exception:
    API_KEY = DEFAULT_KEY
    RAW_ENDPOINT = DEFAULT_ENDPOINT
    DEPLOYMENT_NAME = DEFAULT_DEPLOYMENT

ENDPOINT = sanitizar_url(RAW_ENDPOINT)

# ==============================================================================
# 4. INICIALIZAÇÃO DO CLIENTE AZURE OPENAI
# ==============================================================================
try:
    client = AzureOpenAI(
        api_key=API_KEY,
        api_version="2024-02-01",
        azure_endpoint=ENDPOINT
    )
except Exception as err:
    st.error(f"CRITICAL ERROR // Falha na inicialização do link Azure OpenAI: {err}")
    st.stop()

# ==============================================================================
# 5. INTERFACE PRINCIPAL (HOLO-LAYOUT)
# ==============================================================================
st.markdown('<div class="main-header">⚡ NEURAL DATA EXTRACTOR</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Azure OpenAI Intelligence Core // Análise Semântica Estruturada v4.1</div>', unsafe_allow_html=True)

# Container de Entrada de Texto
with st.container():
    st.markdown("### 📥 Input de Dados Textuais")
    texto_entrada = st.text_area(
        "Insira o fluxo de dados para varredura neural:",
        placeholder="Ex: Marcus e Sarah reportaram anomalias críticas no cluster principal do servidor. Requer intervenção imediata.",
        height=150,
        label_visibility="collapsed"
    )

# Botão de Execução
executar_scan = st.button("🚀 Iniciar Neural Scan & Extração")

# ==============================================================================
# 6. PROCESSAMENTO E CHAMADA AO AZURE OPENAI
# ==============================================================================
if executar_scan:
    if not texto_entrada.strip():
        st.warning("⚠️ Alerta: Insira dados no campo de texto para processamento.")
    else:
        with st.spinner("🔮 Estabelecendo link quântico com Azure OpenAI... Analisando sintaxe..."):
            try:
                system_prompt = (
                    "Você é um motor cibernético de extração de dados e IA analítica de alta precisão. "
                    "Analise o texto fornecido e retorne EXCLUSIVAMENTE UM OBJETO JSON VÁLIDO, sem marcações markdown adicionais fora do JSON. "
                    "O JSON deve conter exatamente as seguintes chaves:\n"
                    "1. 'sentimento': string ('Positivo', 'Negativo', 'Neutro').\n"
                    "2. 'porcentagem_sentimento': inteiro de 0 a 100.\n"
                    "3. 'assunto_principal': string com resumo conciso.\n"
                    "4. 'pessoas_citadas': lista de strings com nomes de pessoas identificadas.\n"
                    "5. 'nivel_de_urgencia': string estritamente entre: 'Baixo', 'Medio', 'Alto'."
                )

                resposta = client.chat.completions.create(
                    model=DEPLOYMENT_NAME,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": texto_entrada}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.1
                )

                dados_json = json.loads(resposta.choices[0].message.content)

                st.success("✨ SUCESSO // Varredura Neural Concluída.")
                st.markdown("<br>", unsafe_allow_html=True)

                # ==============================================================
                # 7. EXIBIÇÃO DOS RESULTADOS (WIDGETS HOLOGRÁFICOS)
                # ==============================================================
                sentimento = dados_json.get("sentimento", "N/A")
                pct = dados_json.get("porcentagem_sentimento", 0)
                urgencia = dados_json.get("nivel_de_urgencia", "Baixo")
                pessoas = dados_json.get("pessoas_citadas", [])
                assunto = dados_json.get("assunto_principal", "Não especificado")

                # Linha 1: Métricas holográficas
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        label="🧬 SENTIMENTO DETECTADO",
                        value=f"{sentimento}",
                        delta=f"{pct}% Confiança"
                    )

                with col2:
                    # Mapeamento estético para urgência
                    urgencia_class = "badge-baixo"
                    if urgencia == "Alto":
                        urgencia_class = "badge-alto"
                    elif urgencia == "Medio":
                        urgencia_class = "badge-medio"
                    
                    st.markdown(f"""
                        <div style="background: rgba(13, 27, 42, 0.7); border: 1px solid rgba(0, 240, 255, 0.3); border-radius: 8px; padding: 14px; text-align: center;">
                            <div style="font-size: 0.8rem; color: #a0aec0; margin-bottom: 8px;">⚡ NÍVEL DE URGÊNCIA</div>
                            <div><span class="{urgencia_class}">{urgencia.upper()}</span></div>
                        </div>
                    """, unsafe_allow_html=True)

                with col3:
                    st.metric(
                        label="👥 ENTIDADES (PESSOAS)",
                        value=len(pessoas)
                    )

                st.markdown("<br>", unsafe_allow_html=True)

                # Seção: Assunto Principal
                st.markdown("""
                    <div class="holo-card">
                        <div style="font-family: 'Orbitron', sans-serif; font-size: 1.1rem; color: #00f0ff; margin-bottom: 10px;">📌 ASSUNTO PRINCIPAL</div>
                        <div style="font-size: 1.05rem; color: #e2e8f0; line-height: 1.5;">{}</div>
                    </div>
                """.format(assunto), unsafe_allow_html=True)

                # Seção: Pessoas Mencionadas
                st.markdown("### 👥 Pessoas Identificadas no Fluxo")
                if pessoas:
                    # Renderização em pílulas cibernéticas
                    if hasattr(st, "pills"):
                        st.pills("Alvos:", pessoas, selection_mode=None)
                    else:
                        tags_html = "".join([f'<span style="background: rgba(0,240,255,0.1); border: 1px solid #00f0ff; padding: 4px 12px; border-radius: 15px; margin-right: 8px; color: #00f0ff;">{p}</span>' for p in pessoas])
                        st.markdown(f"<div>{tags_html}</div>", unsafe_allow_html=True)
                else:
                    st.caption("Nenhuma entidade humana identificada nos parâmetros atuais.")

                # Seção: Visualizador de JSON Bruto (Terminal Style)
                st.markdown("<br>", unsafe_allow_html=True)
                with st.expander("💻 INSPEÇÃO DE DADOS (RAW TERMINAL JSON)"):
                    st.json(dados_json)
