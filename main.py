from dotenv import load_dotenv
import os
from google import genai
import json
import re


load_dotenv()

#Função para classificar o email em produtivo ou improdutivo
def email_analysis(text: str) -> dict:
    print('Passo 1 = analise iniciada.')
    prompt = f"""
Você é um assistente especialista em análise de e-mails para a empresa AutoU.
Sua tarefa é analisar o e-mail fornecido e retornar um objeto JSON.

Sua resposta DEVE SER APENAS o objeto JSON, sem nenhum texto adicional, explicação ou formatação Markdown. Sua resposta deve começar com {{ e terminar com }}.

O objeto JSON deve ter duas chaves: "categoria" e "resposta_sugerida".

1.  **"categoria"**: Classifique o e-mail em "Produtivo" ou "Improdutivo".
    * **Produtivo**: E-mails que requerem uma ação ou resposta específica (ex.: solicitações de suporte, atualização sobre casos, dúvidas sobre o sistema).
    * **Improdutivo**: E-mails que não necessitam de uma ação imediata (ex.: mensagens de felicitações, **agradecimentos por um problema já resolvido**, spam, newsletters).

2.  **"resposta_sugerida"**: Gere uma resposta curta e profissional. **IMPORTANTE: Se o e-mail original estiver em um idioma diferente do português, a resposta sugerida DEVE ser nesse mesmo idioma.** Se a categoria for **'Produtivo'**, a sugestão deve ser um **rascunho de resposta para enviar ao cliente**. Se a categoria for **'Improdutivo'**, a sugestão deve ser uma **ação interna para o funcionário** (ex: "Nenhuma ação necessária. Arquivar.").

O e-mail para análise é:
---
{text}
---
"""
    try:
        GEMINI_API_KEY = os.getenv('GOOGLE_API_KEY')
        
        print(f'Passo 2: Verificando a API Key: {bool(GEMINI_API_KEY)}')
        if not GEMINI_API_KEY:
            raise ValueError('A Key não foi encontrada')

        client = genai.Client(api_key=GEMINI_API_KEY)
        print('Passo 3: Enviando requisição')

        generate = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )

        response = generate.text

        print("--- PASSO 4: Resposta CRUA recebida da API ---")
        print(response)

        match = re.search(r'\{.*}', response, re.DOTALL)
        if match:
            clean_response = match.group(0)
            return json.loads(clean_response)
        else:
            raise ValueError('Nenhum JSON foi encontrado na resposta da API.')

    except Exception as e:
        print(f'Erro na conexão da API: {e}')
        return {'error': 'Ocorreu um erro na tentativa de se conectar com a API da IA.'}
