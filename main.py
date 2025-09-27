import os
from dotenv import load_dotenv
from transformers import pipeline
import requests

load_dotenv() #Para o acesso do TOKEN

#Função para classificar o email em produtivo ou improdutivo
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
def class_email(text):
    categorias = ['Produtivo', 'Improdutivo']
    result = classifier(text, categorias)
    result = result['labels'][0]
    return result

#Configuração da API
token_access = os.getenv('HUGGING_FACE_TOKEN')
API_URL = "https://api-inference.huggingface.co/models/bigscience/bloomz-560m"
headers = {"Authorization": f"Bearer {token_access}"}

#Faz uma requisição para a API 
def query_api(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

#Função para gerar uma resposta profissional para o email
def response_email(categorias):
    prompt = ''
    if categorias == 'Produtivo':
        prompt = f"Gere uma resposta profissional e curta para um e-mail que pede uma atualização de status, por exemplo:"
    elif categorias == 'Improdutivo':
        prompt = f"Gere uma resposta curta e educada para um e-mail não urgente, como um agradecimento, por exemplo:"
    
    #Aciona a função query adicionando o prompt e definindo um limite de ate 50 novas palavras
    api_output = query_api({
        'inputs': prompt,
        'parameters': {'max_new_tokens': 50}
    })
    #Checa se a API não está vazia e se veio em formato de lista
    if api_output and isinstance(api_output, list):
        full_text = api_output[0].get('generated_text', '')
        response = full_text[len(prompt):].strip() #Fatiamento da resposta, guardando apenas o texto gerado pela IA
        return response
    else:
        print(f'Erro na API: {api_output}')
        return "Agradecemos o seu contato. A sua mensagem foi recebida."