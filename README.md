
# Projeto - Corrigir Redação

A Redação é uma das etapas de muitas provas conhecidas entre os estudantes. Como exemplo podemos citar o Enem (Exame Nacional do Ensino Médio) que ocorre todos os anos e tem a a redação como uma das ferramentas de avaliação. Além do ENEM, a grande maioria dos concursos utiliza esse tipo de avaliação para selecionar seus candidatos. 
Para que o candidato obtenha uma boa nota, muitas redações precisam ser escritas e avaliadas por um profissional da língua portuguesa. No entanto, nem todos tem a condição de frequentarem um cursinho, onde há professores aptos a corrigirem as redações, ou mesmo pagar alguém. 

Este repositório dedica-se à construção de uma API que ajude o estudante/candidato a ter sua redação corrigida através do Chat-GPT.


## Instalação

Para utilizar a API é necessário:

- Python instalado
- Uma chave API do da OPENAI (https://openai.com/)
- As seguintes bibliotecas instaladas
    - openai
    - streamlit
    - re

Com isso, siga os seguintes passos:
```bash
# Clone ese repositório
$ git clone <https://github.com/lukais-iohan/corrigir_redacao.git>

# Acesse a pasta do projeto no terminal
$ cd corrigir_redacao

# No terminal digite:
$ streamlit run main.py
```


## Como utilizar

Ao rodar o código anterior, a seguinte janela irá aparecer: 

![](/src/streamlit_window.png)

As informações necessárias para gerar ou corrigir uma redação baseada no tema escolhido são:
    
    1. Chave da OpenAi
    2. Nome da Banca
    3. Escolher entre gerar ou corrigir uma redação
    4. Tema da redação
    5. Critérios para correção (um por linha)

Com essas informações o usuário deve apertar o botão 'Corrigir Redação' ou 'Gerar Redação'. A redação gerada ou corrigida aparecerá no último campo.

## Exemplo

Para demonstrar o uso da ferramenta, iremos utilizar a opção para gerar redação, O tema escolhido foi o da prova de 2012: O movimento imigratório para o Brasil no século XXI. Seguindo o passo anterior para, e clicando no botão 'Run' no canto superior direito na janela aberta, teremos o seguinte resultado:

![](/src/redacao.png)

