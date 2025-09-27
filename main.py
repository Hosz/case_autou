from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def class_email(text):
    categorias = ['Produtivo', 'Improdutivo']
    result = classifier(text, categorias)
    result = result['labels'][0]
    return result