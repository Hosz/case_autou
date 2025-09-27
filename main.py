from transformers import pipeline

#Função para classificar o email em produtivo ou improdutivo
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
def class_email(text):
    categorias = ['Produtivo', 'Improdutivo']
    result = classifier(text, categorias)
    result = result['labels'][0]
    return result

#Função para gerar uma resposta profissional para o email
txt_gen = pipeline("text-generation", model="pierreguillou/gpt2-small-portuguese")
def response_email(categorias):
    prompt_base = f'Uma resposta profissional para o assunto do email {categorias} é:'
    generated = txt_gen(
        prompt_base, 
        max_length=100, 
        num_return_sequences=1
    )
    texto_gerado = generated[0]['generated_text']
    resposta = texto_gerado[len(prompt_base):]
    return resposta