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

# Configurações da página
st.set_page_config(page_title="Corrija sua redação para concurso!!!", page_icon="📝", layout="wide")

# Título da página
st.title("Corretor de Redação")

# Entrar com as credenciais do OPENAI
openai.api_key = st.text_input("Insira sua chave da API do OpenAI")

# Entrada do nome da banca
banca = st.text_input("Nome da Banca")

# Entrada dos critérios de correção
criterios = st.text_area("Critérios de Correção (um por linha)")

# Opção de redação
opcao_redacao = st.radio("Opção de Redação", ("Inserir Redação", "Gerar Redação"))

# Entrada da redação do usuário ou geração de redação com o tema
redacao = ""

if opcao_redacao == "Inserir Redação":
    tema = st.text_input("Tema da Redação")
    redacao = st.text_area("Redação do Usuário")

    # Botão para corrigir a redação
    if st.button("Corrigir Redação") and redacao:
        # Validar o tamanho da redação
        num_linhas = redacao.count("\n") + 1

        if num_linhas < 20 or num_linhas > 30:
            st.warning("A redação deve ter entre 20 e 30 linhas.")
        else:
            # Processar os critérios de correção
            criterios = re.split('\n|,', criterios)
            criterios = [criterio.strip() for criterio in criterios if criterio.strip()]
            criterios.append("Fuga do Tema")  # Adicionar o critério "fuga do tema"
            num_criterios = len(criterios)

            # Verificar se a redação atende aos critérios
            criterios_presentes = [criterio for criterio in criterios if criterio.lower() in redacao.lower()]

            if len(criterios_presentes) != len(criterios):
                st.warning("A redação não atende a todos os critérios fornecidos.")
                criterios_nao_atendidos = set(criterios) - set(criterios_presentes)
                st.subheader("Critérios não atendidos:")
                st.write(criterios_nao_atendidos)
            else:
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
                    nota = 10 - ((len(correcao) / 100) * ((num_criterios - i) / num_criterios))  # Cálculo da nota ponderada
                    nota = max(nota, 0)  # Garantir que a nota não seja negativa
                    nota_total += nota

                nota_final = nota_total / num_criterios
                st.subheader("Nota")
                st.write(nota_final)

elif opcao_redacao == "Gerar Redação":
    tema = st.text_input("Tema da Redação")

    # Botão para gerar a redação
    if st.button("Gerar Redação") and tema:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=tema,
            temperature=0.5,
            max_tokens=1024,
            n=1,
            stop=None
        )
        redacao = response.choices[0].text.strip()

        # Exibir a redação gerada na tela
        st.subheader("Redação Gerada")
        st.write(redacao)
