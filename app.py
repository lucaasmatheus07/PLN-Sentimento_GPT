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
        border: none;
        box-shadow: 0 4px 14px 0 rgba(37, 99, 235, 0.35);
        width: 100%;
        transition: all 0.25s ease-in-out;
    }

    .stButton>button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        box-shadow: 0 6px 20px 0 rgba(37, 99, 235, 0.5);
        transform: translateY(-2px);
    }

    /* Estilização da área de texto */
    .stTextArea textarea {
        background-color: #ffffff !important;
        color: #1e293b !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 12px !important;
        font-family: 'Nunito', sans-serif !important;
        font-size: 1rem !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
    }

    .stTextArea textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15) !important;
    }

    /* Sidebar Clean */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }

    /* Badges de Urgência Coloridos e Legíveis */
    .badge-alto {
        background: #fee2e2;
        border: 1px solid #fca5a5;
        color: #dc2626;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 700;
        display: inline-block;
    }
    .badge-medio {
        background: #fef3c7;
        border: 1px solid #fde047;
        color: #d97706;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 700;
        display: inline-block;
    }
    .badge-baixo {
        background: #dcfce7;
        border: 1px solid #86efac;
        color: #16a34a;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 700;
        display: inline-block;
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. SIDEBAR: INFORMAÇÕES DO SISTEMA
# ==============================================================================
with st.sidebar:
    st.markdown("### 🌈 Painel de Controle")
    st.markdown("---")
    st.markdown("""
    **Análise Semântica Divertida & Precisa**
    
    * **Status:** Tudo pronto! 🚀
    * **IA Ativa:** Azure OpenAI Engine
    * **Modelo:** `gpt-4.1-mini`
    """)
    st.markdown("---")
    st.caption("✨ Tenha um ótimo dia!")

# ==============================================================================
# 3. CREDENCIAIS & SANITIZAÇÃO DE URL
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
    st.error(f"Ops! Tivemos um probleminha para conectar com a Azure: {err}")
    st.stop()

# ==============================================================================
# 5. INTERFACE PRINCIPAL
# ==============================================================================
st.markdown('<div class="main-header">☀️ Extração de Dados Inteligente</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Análise de sentimentos e extração de informações num piscar de olhos! ✨</div>', unsafe_allow_html=True)

# Container de Entrada de Texto
with st.container():
    st.markdown("### ✍️ O que você gostaria de analisar hoje?")
    texto_entrada = st.text_area(
        "Insira seu texto abaixo:",
        placeholder="Cole seu texto aqui! Ex: A equipe do projeto liderada por Camila realizou um trabalho incrível e bateu todas as metas da semana!",
        height=150,
        label_visibility="collapsed"
    )

# Botão de Execução
executar_scan = st.button("🚀 Analisar Texto Agora!")

# ==============================================================================
# 6. PROCESSAMENTO E CHAMADA AO AZURE OPENAI
# ==============================================================================
if executar_scan:
    if not texto_entrada.strip():
        st.warning("😊 Por favor, digite ou cole um texto antes de iniciar a análise!")
    else:
        with st.spinner("✨ Analisando seu texto com carinho... Só um instante!"):
            try:
                system_prompt = (
                    "Você é um assistente amigável e preciso de extração de dados. "
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

                st.success("🎉 Análise concluída com sucesso!")
                st.markdown("<br>", unsafe_allow_html=True)

                # ==============================================================
                # 7. EXIBIÇÃO DOS RESULTADOS
                # ==============================================================
                sentimento = dados_json.get("sentimento", "N/A")
                pct = dados_json.get("porcentagem_sentimento", 0)
                urgencia = dados_json.get("nivel_de_urgencia", "Baixo")
                pessoas = dados_json.get("pessoas_citadas", [])
                assunto = dados_json.get("assunto_principal", "Não especificado")

                # Linha 1: Métricas de Destaque
                col1, col2, col3 = st.columns(3)

                with col1:
                    # Emoji animado conforme sentimento
                    emoji_sent = "😊" if sentimento == "Positivo" else ("😟" if sentimento == "Negativo" else "😐")
                    st.metric(
                        label="😃 SENTIMENTO",
                        value=f"{emoji_sent} {sentimento}",
                        delta=f"{pct}% Confiança"
                    )

                with col2:
                    urgencia_class = "badge-baixo"
                    if urgencia == "Alto":
                        urgencia_class = "badge-alto"
                    elif urgencia == "Medio":
                        urgencia_class = "badge-medio"
                    
                    st.markdown(f"""
                        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 14px; text-align: center; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);">
                            <div style="font-size: 0.85rem; color: #64748b; margin-bottom: 6px; font-weight: 700;">⚡ NÍVEL DE URGÊNCIA</div>
                            <div><span class="{urgencia_class}">{urgencia.upper()}</span></div>
                        </div>
                    """, unsafe_allow_html=True)

                with col3:
                    st.metric(
                        label="👥 PESSOAS MENCIONADAS",
                        value=len(pessoas)
                    )

                st.markdown("<br>", unsafe_allow_html=True)

                # Seção: Assunto Principal
                st.markdown(f"""
                    <div class="happy-card">
                        <div style="font-family: 'Fredoka', sans-serif; font-size: 1.25rem; color: #1e293b; margin-bottom: 8px;">📌 Resumo do Assunto</div>
                        <div style="font-size: 1.05rem; color: #475569; line-height: 1.6;">{assunto}</div>
                    </div>
                """, unsafe_allow_html=True)

                # Seção: Pessoas Mencionadas
                st.markdown("### 👥 Pessoas Encontradas")
                if pessoas:
                    tags_html = "".join([f'<span style="background: #eff6ff; color: #2563eb; border: 1px solid #bfdbfe; padding: 6px 16px; border-radius: 20px; margin-right: 8px; font-weight: 700; font-size: 0.95rem;">{p}</span>' for p in pessoas])
                    st.markdown(f"<div style='margin-top: 10px;'>{tags_html}</div>", unsafe_allow_html=True)
                else:
                    st.info("Nenhum nome de pessoa foi identificado no texto.")

                # Seção: Visualizador de JSON
                st.markdown("<br>", unsafe_allow_html=True)
                with st.expander("🔍 Visualizar Dados Completos (JSON)"):
                    st.json(dados_json)

            except json.JSONDecodeError:
                st.error("Ops! Tivemos uma falha ao interpretar a resposta da IA.")
            except Exception as e:
                st.error(f"Ops! Ocorreu um erro durante o processamento: {e}")
