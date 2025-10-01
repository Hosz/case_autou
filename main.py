from dotenv import load_dotenv  #Pra carregar a API key do arquivo .env
import os                       #Pra acessar as variaveis de ambiente que o dotenv carregou
from google import genai        #Biblioteca da API de IA
import ast                      #"Tradutor" de string para objeto
import fitz                     #Ferramenta de leitura de texto de PDF
import re                       #Regular o padrão do texto

#Carregar a API Key
load_dotenv()

#Função para extrair o texto do PDF
def extract_text_from_pdf(filepath):
    #Tenta fazer a leitura do arquivo PDF
    try:
        #Abre o arquivo PDF e salva uma variável para guardar o texto das páginas
        with open(filepath, 'rb') as pdf_file:
            pdf_bytes = pdf_file.read()
        pdf_document = fitz.open('pdf', pdf_bytes)
        text = ''
        for page in pdf_document:
            text += page.get_text()
        pdf_document.close()
        return text
    except Exception as e:
        print(f'Erro ao extrair texto do PDF: {e}')
        return None

#Função que classifica e gera sugestões de acordo com a classificação
def email_analysis(text: str) -> dict:
    #Prompt com instruções para a IA do que se deve fazer, regras e como retornar
    prompt = f"""
Você é um assistente especialista em análise de e-mails para a empresa AutoU.
Sua única função é analisar o e-mail fornecido e retornar um ÚNICO objeto JSON com três chaves: "categoria", "acao_interna", e "rascunho_resposta".

Siga estas regras RIGOROSAMENTE:
1.  **"categoria"**: Classifique o e-mail em "Produtivo" ou "Improdutivo".
    * **Produtivo**: Requer uma ação ou resposta específica (solicitações, dúvidas, etc)
    * **Improdutivo**: Não necessita de ação imediata (agradecimentos, spam, felicitações, **e-mails que confirmam que um problema já foi resolvido**).
2.  **"acao_interna"**: Descreva a ação que o funcionário deve tomar (ex: "Responder ao cliente", "Arquivar").
3.  **"rascunho_resposta"**: Gere um rascunho de resposta se for 'Produtivo' ou uma resposta de cortesia se for um agradecimento. Se for spam ou irrelevante, retorne uma string vazia "".

**Formato Final**: Sua saída DEVE SER APENAS o objeto JSON, começando com {{{{ e terminando com }}}}.

Texto para Análise:
---
{text}
---
"""
    try:
        #Faz a conexão com a API do Gemini
        GEMINI_API_KEY = os.getenv('GOOGLE_API_KEY')
        if not GEMINI_API_KEY:
            raise ValueError('A Key não foi encontrada')
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        generate = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        
        #Processo de limpeza da resposta
        response = generate.text
        response = response.strip()

        #Faz a busca de onde começa e onde termina pra pegar o objeto JSON da resposta
        match = re.search(r'(\{.*\})', response, re.DOTALL)
        if not match:
            raise ValueError('Nenhum objeto JSON válido foi encontrado na resposta da API.')
        
        #Pega o texto limpo após busca feita pelo "re.search"
        json_string = match.group(0)
        return ast.literal_eval(json_string)

    except Exception as e:
        print(f'Erro na conexão da API: {e}')
        return {'error': 'Ocorreu um erro na tentativa de se conectar com a API da IA'}