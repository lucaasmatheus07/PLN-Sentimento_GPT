import json
import re
import streamlit as st
from openai import AzureOpenAI

# ==============================================================================
# 1. CONFIGURAÇÃO DA PÁGINA E TEMA ALVINEGRO // CORINTHIANO
# ==============================================================================
st.set_page_config(
    page_title="NEURAL-EXTRACT // Timão AI Core",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injeção de CSS Customizado - Tema Corinthiano
st.markdown("""
    <style>
    /* Importação de fontes marcantes */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;900&family=Oswald:wght@500;700&display=swap');

    /* Fundo escuro com padrão discreto de listras do Timão */
    .stApp {
        background-color: #0b0c0e;
        background-image: repeating-linear-gradient(
            0deg,
            #0b0c0e,
            #0b0c0e 40px,
            #121418 40px,
            #121418 80px
        );
        color: #f1f1f1;
        font-family: 'Montserrat', sans-serif;
    }

    /* Cabeçalhos e Títulos estilo Bando de Loucos */
    h1, h2, h3, .timao-title {
        font-family: 'Oswald', sans-serif !important;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    .main-header {
        font-size: 2.6rem;
        font-weight: 900;
        color: #ffffff;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
        margin-bottom: 0.1rem;
        border-bottom: 3px solid #cc0000;
        display: inline-block;
        padding-bottom: 5px;
    }

    .sub-header {
        font-size: 1.05rem;
        color: #a0a0a0;
        margin-top: 8px;
        margin-bottom: 2rem;
        border-left: 4px solid #ffffff;
        padding-left: 12px;
    }

    /* Cartões Escuros com Borda Branca/Fogo */
    .holo-card {
        background: rgba(18, 20, 24, 0.95);
        border: 1px solid #333333;
        border-left: 4px solid #ffffff;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.8);
        border-radius: 8px;
        padding: 22px;
        margin-bottom: 20px;
    }

    /* Botão Oficial Corinthiano */
    .stButton>button {
        background: linear-gradient(135deg, #111111 0%, #222222 100%);
        color: #ffffff !important;
        font-family: 'Oswald', sans-serif !important;
        font-weight: 700;
        font-size: 1.1rem;
        border-radius: 4px;
        padding: 0.75rem 1.5rem;
        border: 1px solid #ffffff;
        box-shadow: 0 4px 15px rgba(255, 255, 255, 0.1);
        width: 100%;
        transition: all 0.3s ease-in-out;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stButton>button:hover {
        background: #ffffff;
        color: #000000 !important;
        box-shadow: 0 0 20px rgba(255, 255, 255, 0.6);
        border-color: #ffffff;
    }

    /* Estilização da área de texto */
    .stTextArea textarea {
        background-color: #121418 !important;
        color: #ffffff !important;
        border: 1px solid #333333 !important;
        border-radius: 6px;
        font-family: 'Montserrat', sans-serif !important;
    }
    .stTextArea textarea:focus {
        border-color: #ffffff !important;
    }

    /* Sidebar alvinegra */
    [data-testid="stSidebar"] {
        background-color: #050506;
        border-right: 1px solid #222222;
    }

    /* Badges de Urgência em Tom Corinthiano */
    .badge-alto {
        background: rgba(204, 0, 0, 0.2);
        border: 1px solid #cc0000;
        color: #ff4d4d;
        padding: 4px 12px;
        border-radius: 4px;
        font-weight: bold;
    }
    .badge-medio {
        background: rgba(230, 160, 0, 0.2);
        border: 1px solid #e6a000;
        color: #ffc83b;
        padding: 4px 12px;
        border-radius: 4px;
        font-weight: bold;
    }
    .badge-baixo {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid #ffffff;
        color: #ffffff;
        padding: 4px 12px;
        border-radius: 4px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. SIDEBAR: GUIA DE CONFIGURAÇÃO DO SISTEMA
# ==============================================================================
with st.sidebar:
    st.markdown("### 🦅 TIMÃO AI CORE")
    st.markdown("---")
    st.markdown("""
    **S.C. Corinthians Paulista - Neural Engine**
    
    * **Status:** Conexão Ativa
    * **Módulo:** Análise Semântica de Dados
    * **Modelo:** `gpt-4.1-mini`
    """)
    st.markdown("---")
    st.caption("🏁 Vai Corinthians!")

# ==============================================================================
# 3. CREDENCIAIS & CORREÇÃO DO ENDPOINT
# ==============================================================================
def sanitizar_url(url: str) -> str:
    url_limpa = re.sub(r'&quot;|"|\'|\s+', '', url).strip()
    url_limpa = re.sub(r'/openai/v1/?$', '', url_limpa)
    return url_limpa.rstrip('/')

minha_chave = "1gsyJYiGIr1rIjIm6heIq96VWJI5gMgXeXCaYCHx5WeeWGm3AMYvJQQJ99CJACHYHv6XJ3w3AAAAACOGUF3S"
meu_endpoint = "https://marcelomaffeis-7430-resource.services.ai.azure.com/openai/v1&quot;"
meu_modelo = "gpt-4.1-mini"

API_KEY = minha_chave
ENDPOINT = sanitizar_url(meu_endpoint)
DEPLOYMENT_NAME = meu_modelo

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
    st.error(f"ERRO CRÍTICO // Falha ao conectar ao motor da Azure: {err}")
    st.stop()

# ==============================================================================
# 5. INTERFACE PRINCIPAL
# ==============================================================================
st.markdown('<div class="main-header">🦅 CORINTHIANS NEURAL EXTRACT</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Central Alvinegra de Inteligência & Processamento de Dados</div>', unsafe_allow_html=True)

# Container de Entrada de Texto
with st.container():
    st.markdown("### 📥 Entrada de Informações / Relatório")
    texto_entrada = st.text_area(
        "Insira o texto para análise semântica:",
        placeholder="Ex: Yuri Alberto e Rodrigo Garro relataram excelente desempenho no treino de hoje antes da decisão. A comissão técnica está muito confiante.",
        height=150,
        label_visibility="collapsed"
    )

# Botão de Execução
executar_scan = st.button("🏁 Executar Análise Alvinegra")

# ==============================================================================
# 6. PROCESSAMENTO E CHAMADA AO AZURE OPENAI
# ==============================================================================
if executar_scan:
    if not texto_entrada.strip():
        st.warning("⚠️ Alerta: Insira um texto para processar a análise.")
    else:
        with st.spinner("🦅 Processando dados com a garra do Timão..."):
            try:
                system_prompt = (
                    "Você é um motor analítico de IA de alta precisão. "
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

                st.success("⚽ SUCESSO // Análise Concluída com Sucesso!")
                st.markdown("<br>", unsafe_allow_html=True)

                # ==============================================================
                # 7. EXIBIÇÃO DOS RESULTADOS
                # ==============================================================
                sentimento = dados_json.get("sentimento", "N/A")
                pct = dados_json.get("porcentagem_sentimento", 0)
                urgencia = dados_json.get("nivel_de_urgencia", "Baixo")
                pessoas = dados_json.get("pessoas_citadas", [])
                assunto = dados_json.get("assunto_principal", "Não especificado")

                # Linha 1: Métricas Principais
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        label="📊 SENTIMENTO DETECTADO",
                        value=f"{sentimento}",
                        delta=f"{pct}% Precisão"
                    )

                with col2:
                    urgencia_class = "badge-baixo"
                    if urgencia == "Alto":
                        urgencia_class = "badge-alto"
                    elif urgencia == "Medio":
                        urgencia_class = "badge-medio"
                    
                    st.markdown(f"""
                        <div style="background: rgba(18, 20, 24, 0.95); border: 1px solid #333333; border-radius: 8px; padding: 14px; text-align: center;">
                            <div style="font-size: 0.8rem; color: #a0a0a0; margin-bottom: 8px; font-weight: bold;">⚡ NÍVEL DE URGÊNCIA</div>
                            <div><span class="{urgencia_class}">{urgencia.upper()}</span></div>
                        </div>
                    """, unsafe_allow_html=True)

                with col3:
                    st.metric(
                        label="👥 NOMES / ENTIDADES",
                        value=len(pessoas)
                    )

                st.markdown("<br>", unsafe_allow_html=True)

                # Seção: Assunto Principal
                st.markdown(f"""
                    <div class="holo-card">
                        <div style="font-family: 'Oswald', sans-serif; font-size: 1.2rem; color: #ffffff; margin-bottom: 8px; letter-spacing: 1px;">📌 RESUMO DO ASSUNTO</div>
                        <div style="font-size: 1.05rem; color: #d0d0d0; line-height: 1.5;">{assunto}</div>
                    </div>
                """, unsafe_allow_html=True)

                # Seção: Pessoas Mencionadas
                st.markdown("### 👥 Pessoas Mencionadas")
                if pessoas:
                    tags_html = "".join([f'<span style="background: #ffffff; color: #000000; padding: 5px 14px; border-radius: 20px; margin-right: 8px; font-weight: bold; font-size: 0.9rem;">{p}</span>' for p in pessoas])
                    st.markdown(f"<div style='margin-top: 10px;'>{tags_html}</div>", unsafe_allow_html=True)
                else:
                    st.caption("Nenhuma pessoa foi identificada no texto fornecido.")

                # Seção: Visualizador de JSON Bruto
                st.markdown("<br>", unsafe_allow_html=True)
                with st.expander("💻 DADOS BRUTOS EM JSON"):
                    st.json(dados_json)

            except json.JSONDecodeError:
                st.error("❌ ERRO DE PARSER // Falha ao processar a resposta JSON.")
            except Exception as e:
                st.error(f"❌ ERRO CRÍTICO NO PROCESSAMENTO: {e}")
