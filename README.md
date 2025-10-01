# Analisador de E-mails com IA - Case Prático AutoU

## 📜 Descrição

Este projeto é uma solução full-stack desenvolvida como parte do case prático da AutoU. O objetivo é criar uma aplicação web que utiliza a API de IA do Google (Gemini) para automatizar a leitura e classificação de e-mails, liberando tempo da equipe e otimizando o fluxo de trabalho.

A aplicação é capaz de receber o conteúdo de um e-mail (seja por texto direto ou por upload de arquivo `.txt`/.pdf), classificá-lo como "Produtivo" ou "Improdutivo", e sugerir ações contextuais, como um rascunho de resposta ou uma ação interna a ser tomada.

## ✨ Funcionalidades Principais (Features)

-   **🤖 Análise com IA:** Integração com a API Google Gemini para classificação de texto e geração de respostas com base em um prompt robusto e refinado.
-   **✌️ Duas Formas de Entrada:** Interface com abas que permite ao usuário tanto digitar/colar o texto do e-mail quanto fazer o upload de arquivos.
-   **📂 Suporte a Arquivos:** Capacidade de processar arquivos `.txt` e `.pdf`, extraindo o texto do conteúdo para análise.
-   **🖱️ Upload Customizado:** Componente de "arrastar e soltar" (drag and drop) para uma experiência de usuário moderna.
-   **🎨 Interface Reativa:** Feedback visual em tempo real para o usuário, incluindo estados de carregamento (loading), botões dinâmicos e resultados com cores contextuais.
-   **📋 Botão de Copiar:** Funcionalidade de "copiar para a área de transferência" para facilitar o uso das respostas sugeridas.
-   **⚙️ Back-end Robusto:** Construído com Flask, possui uma arquitetura limpa, tratamento de erros e um mecanismo seguro para processamento de arquivos temporários.

## 🚀 Links

-   **Link da Aplicação (Deploy):** 
-   **Vídeo Demonstrativo (YouTube):** 

## 🛠️ Tecnologias Utilizadas

**Back-end:**
-   Python 3.9+
-   Flask (para o servidor web e a API)
-   Google Generative AI (`google-genai`)
-   PyMuPDF (`fitz`) (para extração de texto de PDFs)
-   python-dotenv (para gerenciamento de variáveis de ambiente)
-   Gunicorn (para o deploy em produção)

**Front-end:**
-   HTML5
-   CSS3
-   JavaScript (Vanilla JS)

## 🔧 Configuração do Ambiente Local

Para rodar este projeto na sua máquina, siga os passos abaixo.

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/Hosz/case_autou.git](https://github.com/Hosz/case_autou.git)
    cd case_autou
    ```

2.  **Crie e ative um ambiente virtual:**
    ```powershell
    # Criar o ambiente
    python -m venv venv

    # Ativar o ambiente (Windows PowerShell)
    .\venv\Scripts\Activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as Variáveis de Ambiente:**
    -   Crie um arquivo chamado `.env` na raiz do projeto.
    -   Dentro do `.env`, adicione sua chave da API do Google Gemini:
        ```
        GOOGLE_API_KEY='SUA_CHAVE_DE_API_AQUI'
        ```

5.  **Execute a aplicação:**
    ```bash
    python app.py
    ```

6.  Abra seu navegador e acesse `http://127.0.0.1:5000/`.

## 🕹️ Como Usar

A aplicação possui uma interface simples com duas abas:

-   **Digitar E-mail:** Cole o conteúdo de um e-mail na caixa de texto e clique em "Analisar E-mail".
-   **Importar Arquivo:** Clique na área designada para selecionar um arquivo `.txt` ou `.pdf` do seu computador, ou simplesmente arraste e solte o arquivo na área. Em seguida, clique em "Analisar E-mail".

O resultado da análise será exibido na parte inferior da página.

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
