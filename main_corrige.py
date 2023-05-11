import streamlit as st
import openai
import re

# Função para criar a correção da redação usando a API do OpenAI
def criar_correcao_redacao(redacao):
    # Montar o prompt de acordo com as informações inseridas pelo usuário
    prompt = f"Corrija a redação abaixo levando em consideração os seguintes critérios:\n\n"

    for criterio in st.session_state['critérios']:
        prompt += f"- {criterio}\n"

    prompt += f"\nTexto Motivador:\n{st.session_state['Textos_Motivadores']}\n\nRedação:\n{redacao}\n\nCorreção:"

    # Enviar o prompt para a API do OpenAI
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.5,
        max_tokens=1024,
        n=1,
        stop=None
    )

    # Retornar a correção da redação gerada pela API do OpenAI
    return response.choices[0].text


# Configurações da página
st.set_page_config(page_title="Corrija sua redação para concurso!!!", page_icon="📝", layout="wide")




# Título da página
st.title("Corretor de Redação para Concursos")

### Entrar com as credencias do OPENAI
openai.api_key = st.text_input("Insira sua chave da API do OpenAI")

# Entrada do nome da banca
banca = st.text_input("Nome da Banca")

# Entrada dos critérios de correção
criterios = st.text_area("Critérios de Correção (um por linha)")

# Entrada dos textos motivadores
textos_motivadores = st.text_area("Textos Motivadores")

# Entrada da redação do usuário
redacao = st.text_area("Redação do Usuário")

# Botão para enviar a redação e obter a correção
if st.button("Corrigir Redação"):
    # Validar o tamanho da redação
    if len(redacao) > 2100 or len(redacao) < 1400:
        st.warning("O tamanho da redação deve estar entre 1400 e 2100 caracteres.") ### equivalante entre 20 a 30 linhas
    else:
        # Processar os critérios de correção
        criterios = re.split('\n|,', criterios)
        criterios = [criterio.strip() for criterio in criterios if criterio.strip()]

        # Armazenar as informações do usuário na sessão do Streamlit
        st.session_state['banca'] = banca
        st.session_state['criterios'] = criterios
        st.session_state['textos_motivadores'] = textos_motivadores

        # Criar a correção da redação usando a API do OpenAI
        correcao = criar_correcao_redacao(redacao)

        # Exibir a correção da redação na tela
        st.subheader("Correção da Redação")
        st.write(correcao)
