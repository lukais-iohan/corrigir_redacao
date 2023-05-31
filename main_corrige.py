import streamlit as st
import openai
import re

# Função para criar a correção da redação usando a API do OpenAI
def criar_correcao_redacao(redacao):
    # Montar o prompt de acordo com as informações inseridas pelo usuário
    prompt = f"Corrija a redação abaixo levando em consideração os seguintes critérios:\n\n"

    for criterio in st.session_state['criterios']:
        prompt += f"- {criterio}\n"

    prompt += f"\nRedação:\n{redacao}\n\nCorreção:"

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

# Função para realizar a correção detalhada da redação
def corrigir_redacao_detalhada(redacao, tema):
    # Adicione aqui a lógica para a correção detalhada da redação
    # Verifique se a redação não foge do tema proposto
    if tema.lower() not in redacao.lower():
        return "A redação não aborda o tema proposto. Certifique-se de que sua redação esteja relacionada ao tema fornecido."

    # Você pode adicionar mais regras e análises de acordo com as necessidades

    correcao_detalhada = "Exemplo de correção detalhada da redação:\n\n"
    correcao_detalhada += "Parágrafo 1: A introdução precisa ser mais clara e concisa. Sugiro reescrever a frase de abertura para captar melhor a atenção do leitor.\n"
    correcao_detalhada += "Parágrafo 2: A argumentação é válida, porém é necessário aprofundar mais os pontos apresentados. Inclua exemplos e evidências para embasar suas ideias.\n"
    correcao_detalhada += "Parágrafo 3: A conclusão deve reforçar a tese e fornecer um fechamento forte. Sugiro reformular a última frase para transmitir mais assertividade.\n"

    return correcao_detalhada

# Configurações da página
st.set_page_config(page_title="Corrija sua redação!!!", page_icon="📝", layout="wide")

# Título da página
st.title("Corretor de Redação")

# Entrar com as credenciais do OPENAI
openai.api_key = st.text_input("Insira sua chave da API do OpenAI")

# Entrada do nome da banca
banca = st.text_input("Nome da Banca")

# Opção para gerar uma redação de acordo com o tema proposto ou corrigir a própria redação
opcao = st.radio("Escolha uma opção", ("Gerar Redação", "Corrigir Redação Própria"))

# Entrada do tema da redação
tema = st.text_input("Tema da Redação")

# Entrada dos critérios de correção
criterios = st.text_area("Critérios de Correção (um por linha)")

# Redação gerada ou redação do usuário
if opcao == "Gerar Redação":
    redacao = st.text_area("Redação Gerada")
else:
    redacao = st.text_area("Redação do Usuário")

# Botão para enviar a redação e obter a correção
if st.button("Corrigir Redação"):
    # Validar o tamanho da redação
    if len(redacao) > 2100 or len(redacao) < 1400:
        st.warning("O tamanho da redação deve estar entre 1400 e 2100 caracteres.") ### equivalente entre 20 a 30 linhas
    else:
        # Processar os critérios de correção
        criterios = re.split('\n|,', criterios)
        criterios = [criterio.strip() for criterio in criterios if criterio.strip()]
        num_criterios = len(criterios)

        # Armazenar as informações do usuário na sessão do Streamlit
        st.session_state['banca'] = banca
        st.session_state['criterios'] = criterios

        # Criar a correção da redação usando a API do OpenAI
        correcao = criar_correcao_redacao(redacao)

        # Exibir a correção da redação na tela
        st.subheader("Correção da Redação")
        st.write(correcao)

        # Calcular e exibir a nota do candidato
        nota_total = 0
        for i, criterio in enumerate(criterios):
            nota = 10 - (len(correcao) / 100) * ((num_criterios - i) / num_criterios)  # Cálculo da nota ponderada
            nota_total += nota

        nota_final = nota_total / num_criterios
        st.subheader("Nota")
        st.write(nota_final)

        # Corrigir a redação como um professor de redação
        st.subheader("Correção Detalhada")
        st.write("Aqui está uma correção detalhada da redação:")
        correcao_detalhada = corrigir_redacao_detalhada(redacao, tema)
        st.write(correcao_detalhada)
