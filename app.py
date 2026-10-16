"""
MIT License

Copyright (c) 2026 Arquiteto de Software / Instrutor

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import json
import streamlit as st
from openai import AzureOpenAI

# ==============================================================================
# CONFIGURAÇÃO DIDÁTICA DO .streamlit/secrets.toml
# ==============================================================================
# Para que este aplicativo funcione localmente sem expor chaves no código fonte,
# você deve criar uma pasta chamada `.streamlit` no mesmo diretório onde este
# arquivo `app.py` está salvo. Dentro da pasta `.streamlit`, crie um arquivo
# chamado `secrets.toml` com o seguinte conteúdo exato:
#
# [azure_openai]
# api_key = "SUA_API_KEY_AQUI"
# endpoint = "SEU_ENDPOINT_AQUI"
# deployment_name = "gpt-4.1-mini"
#
# No código abaixo, utilizamos st.secrets para ler essas credenciais de forma segura.
# ==============================================================================

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Extrator de Dados Inteligente | Azure OpenAI",
    page_icon="🤖",
    layout="centered"
)

# Estilização moderna com CSS injetado
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        background-color: #0078d4;
        color: white;
        font-weight: bold;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #106ebe;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 Extrator de Dados Inteligente")
st.markdown("Utilizando **Azure OpenAI** e infraestrutura da Microsoft para análise estruturada de texto.")

# Carregamento seguro das credenciais via st.secrets com fallback didático para fins de demonstração
try:
    AZURE_API_KEY = st.secrets["azure_openai"]["api_key"]
    AZURE_ENDPOINT = st.secrets["azure_openai"]["endpoint"]
    DEPLOYMENT_NAME = st.secrets["azure_openai"]["deployment_name"]
except Exception:
    # Fallback utilizando os dados fornecidos no escopo para facilitar o primeiro teste acadêmico/local
    AZURE_API_KEY = "6t2pTNsmNafDyo53MDAFIrvvQRBZXP7dLcr5j3TLxMS34LQVq3ZUJQQJ99CHACHYHv6XJ3w3AAAAACOGT7os"
    AZURE_ENDPOINT = "https://marcelomaffeis-05082026-resource.services.ai.azure.com/"
    DEPLOYMENT_NAME = "gpt-4.1-mini"

# Inicialização do cliente Azure OpenAI
try:
    client = AzureOpenAI(
        api_key=AZURE_API_KEY,
        api_version="2024-02-15-preview",
        azure_endpoint=AZURE_ENDPOINT
    )
except Exception as e:
    st.error(f"Erro ao inicializar o cliente AzureOpenAI: {e}")

# Campo de texto para entrada do usuário
st.markdown("### 📝 Insira o texto para análise")
texto_usuario = st.text_area(
    "Digite ou cole sua mensagem, e-mail ou feedback abaixo:",
    placeholder="Ex: João e Maria reclamaram fortemente sobre o atraso na entrega do projeto X, exigindo uma solução urgente até amanhã.",
    height=150
)

# Botão de processamento
if st.button("Processar Texto"):
    if not texto_usuario.strip():
        st.warning("Por favor, digite algum texto antes de clicar em Processar.")
    else:
        with st.spinner("Analisando dados com Azure OpenAI..."):
            try:
                # System Prompt estrito garantindo resposta em formato JSON válido
                system_prompt = (
                    "Você é um assistente especialista em extração de dados e análise de texto. "
                    "Analise o texto fornecido pelo usuário e retorne ESTRITAMENTE UM OBJETO JSON VÁLIDO "
                    "(sem blocos de código markdown adicionais se possível, ou apenas JSON puro) com exatamente as seguintes chaves:\n"
                    "- 'sentimento': string descritiva do sentimento predominante (ex: Positivo, Negativo, Neutro).\n"
                    "- 'porcentagem_sentimento': número inteiro de 0 a 100 indicando a intensidade/confiança desse sentimento.\n"
                    "- 'assunto_principal': string resumindo o tema central do texto.\n"
                    "- 'pessoas_citadas': lista de strings contendo os nomes das pessoas mencionadas no texto (vazia se não houver).\n"
                    "- 'nivel_de_urgencia': string contendo estritamente um destes três valores: 'Baixo', 'Medio', ou 'Alto'."
                )

                response = client.chat.completions.create(
                    model=DEPLOYMENT_NAME,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": texto_usuario}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.1
                )

                # Extração e parsing do conteúdo JSON retornado
                conteudo_resposta = response.choices[0].message.content
                dados_extraidos = json.loads(conteudo_resposta)

                st.success("Processamento concluído com sucesso!")
                st.divider()

                # Exibição estruturada na interface
                st.subheader("📊 Resultados da Extração")

                # Métricas visuais utilizando st.metric
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        label="Sentimento",
                        value=dados_extraidos.get("sentimento", "N/A")
                    )
                
                with col2:
                    pct = dados_extraidos.get("porcentagem_sentimento", 0)
                    st.metric(
                        label="Intensidade",
                        value=f"{pct}%"
                    )

                with col3:
                    urgencia = dados_extraidos.get("nivel_de_urgencia", "Baixo")
                    st.metric(
                        label="Urgência",
                        value=urgencia
                    )
