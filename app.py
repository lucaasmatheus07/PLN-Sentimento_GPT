import json
import re
import streamlit as st
from openai import AzureOpenAI

# ==============================================================================
# 1. CONFIGURAÇÃO DA PÁGINA E ESTILIZAÇÃO (STREAMLIT UI)
# ==============================================================================
st.set_page_config(
    page_title="Extrator de Dados Inteligente | Azure OpenAI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Customização de CSS para um visual moderno e limpo
st.markdown("""
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .stButton>button {
        background-color: #0078D4;
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        border: none;
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #106EBE;
        color: white;
        box-shadow: 0 4px 12px rgba(0, 120, 212, 0.25);
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. SIDEBAR DIDÁTICO: INSTRUÇÕES DO .streamlit/secrets.toml
# ==============================================================================
with st.sidebar:
    st.image("https://img.icons8.com/color/96/azure-1.png", width=64)
    st.title(" Configurações & Guia")
    st.markdown("""
    Este aplicativo se conecta ao **Azure OpenAI** utilizando credenciais seguras.
    
    ---
    ### 📂 Como configurar localmente:
    Para evitar expor suas chaves de API no código, crie a pasta e o arquivo localmente:
    
    **Caminho:** `.streamlit/secrets.toml`
    
    ```toml
    AZURE_OPENAI_KEY = "Sua_Chave_Aqui"
    AZURE_OPENAI_ENDPOINT = "https://seu-recurso.services.ai.azure.com/"
    AZURE_OPENAI_DEPLOYMENT = "gpt-4.1-mini"
    ```
    """)
    st.info("💡 Se o arquivo `secrets.toml` não for encontrado, o app utilizará os valores de fallback predefinidos no código.")

# ==============================================================================
# 3. GERENCIAMENTO DE CREDENCIAIS E SANITIZAÇÃO
# ==============================================================================
# Função auxiliar para limpar URLs com eventuais entidades HTML como `&quot;` ou aspas
def sanitizar_url(url: str) -> str:
    url_limpa = re.sub(r'&quot;|"|\'|\s+', '', url)
    return url_limpa.strip()

# Valores de Fallback fornecidos no projeto
DEFAULT_KEY = "6t2pTNsmNafDyo53MDAFIrvvQRBZXP7dLcr5j3TLxMS34LQVq3ZUJQQJ99CHACHYHv6XJ3w3AAAAACOGT7os"
DEFAULT_ENDPOINT = "https://marcelomaffeis-05082026-resource.services.ai.azure.com/"
DEFAULT_DEPLOYMENT = "gpt-4.1-mini"

# Tenta ler prioritariamente de st.secrets, senão usa os fallbacks
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
# 4. INSTANCIAÇÃO DO CLIENTE AZURE OPENAI
# ==============================================================================
try:
    client = AzureOpenAI(
        api_key=API_KEY,
        api_version="2024-02-01",
        azure_endpoint=ENDPOINT
    )
except Exception as err:
    st.error(f"Erro ao inicializar o cliente Azure OpenAI: {err}")
    st.stop()

# ==============================================================================
# 5. INTERFACE PRINCIPAL
# ==============================================================================
st.markdown('<div class="main-header">⚡ Extrator de Dados Inteligente</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Análise estruturada de texto impulsionada pela infraestrutura Azure OpenAI</div>', unsafe_allow_html=True)

# Entrada do Usuário
texto_entrada = st.text_area(
    "Insira o texto que deseja analisar:",
    placeholder="Exemplo: Roberto e Amanda enviaram uma reclamação grave referente à falha técnica no servidor principal. Precisamos de uma solução urgente para esse problema ainda hoje.",
    height=160
)

# ==============================================================================
# 6. PROCESSAMENTO DA REQUISIÇÃO (SYSTEM PROMPT RÍGIDO)
# ==============================================================================
if st.button("🚀 Processar e Extrair Dados", use_container_width=True):
    if not texto_entrada.strip():
        st.warning("⚠️ Por favor, digite algum texto antes de iniciar o processamento.")
    else:
        with st.spinner("🔍 Analisando conteúdo com Azure OpenAI..."):
            try:
                # System Prompt Rígido para forçar retorno estrito de JSON
                system_prompt = (
                    "Você é um motor de extração de dados e IA analítica de alta precisão. "
                    "Analise o texto fornecido pelo usuário e retorne EXCLUSIVAMENTE UM OBJETO JSON VÁLIDO "
                    "sem nenhuma formatação adicional fora do JSON. O objeto JSON deve possuir estritamente as seguintes chaves:\n"
                    "1. 'sentimento': string indicando o sentimento predominante (ex: 'Positivo', 'Negativo', 'Neutro').\n"
                    "2. 'porcentagem_sentimento': número inteiro de 0 a 100 representando a confiança/intensidade do sentimento.\n"
                    "3. 'assunto_principal': string com um resumo conciso do tema central.\n"
                    "4. 'pessoas_citadas': array/lista de strings com os nomes de pessoas físicas identificadas no texto.\n"
                    "5. 'nivel_de_urgencia': string contendo estritamente uma destas opções: 'Baixo', 'Medio', 'Alto'."
                )

                # Chamada da API com formato de resposta forçado em json_object
                resposta = client.chat.completions.create(
                    model=DEPLOYMENT_NAME,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": texto_entrada}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.1
                )

                # Parsing do JSON
                conteudo_json = json.loads(resposta.choices[0].message.content)

                st.success("✨ Processamento concluído com sucesso!")
                st.markdown("---")

                # ==============================================================
                # 7. EXIBIÇÃO VISUAL DOS RESULTADOS
                # ==============================================================
                
                # Extração de campos
                sentimento = conteudo_json.get("sentimento", "N/A")
                pct_sentimento = conteudo_json.get("porcentagem_sentimento", 0)
                urgencia = conteudo_json.get("nivel_de_urgencia", "Baixo")
                pessoas = conteudo_json.get("pessoas_citadas", [])
                assunto = conteudo_json.get("assunto_principal", "Não identificado")

                # Métrica 1: 3 Colunas principais com st.metric
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        label="Sentimento / Confiança",
                        value=f"{sentimento}",
                        delta=f"{pct_sentimento}% Relevância"
                    )

                with col2:
                    # Formatação visual simples para o Nível de Urgência
                    indicador_urgencia = {
                        "Alto": "🔴 Alto",
                        "Medio": "🟡 Médio",
                        "Baixo": "🟢 Baixo"
                    }.get(urgencia, urgencia)
                    
                    st.metric(
                        label="Nível de Urgência",
                        value=indicador_urgencia
                    )

                with col3:
                    st.metric(
                        label="Pessoas Citadas",
                        value=len(pessoas)
                    )

                st.markdown("---")

                # Seção: Assunto Principal
                st.markdown("### 📌 Assunto Principal")
                st.info(assunto)

                # Seção: Pessoas Citadas
                st.markdown("### 👥 Pessoas Mencionadas")
                if pessoas:
                    # Utilização do recurso st.pills (Streamlit nativo) se disponível, ou lista estilizada
                    if hasattr(st, "pills"):
                        st.pills("Identificados:", pessoas, selection_mode=None)
                    else:
                        st.write(" • ".join([f"**{p}**" for p in pessoas]))
                else:
                    st.caption("Nenhuma pessoa específica foi identificada no texto analisado.")

                # Seção: JSON Bruto
                st.markdown("---")
                with st.expander("🛠️ Visualizar JSON Bruto (Dados Estruturados)"):
                    st.json(conteudo_json)

            except json.JSONDecodeError:
                st.error("❌ Erro ao converter a resposta do modelo em JSON válido.")
            except Exception as e:
                st.error(f"❌ Erro durante a execução da requisição: {e}")
