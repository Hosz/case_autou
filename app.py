from flask import Flask, request, jsonify, render_template
import flask
from main import email_analysis
import os

app = Flask(__name__)

#Rota do Front/Interface
@app.route('/', methods=['GET'])
def homepage():
    return render_template('index.html')

#Define uma rota com o metodo "POST"
@app.route('/process-email', methods=['POST'])
def process_email():
    data = request.get_json()

    #Checagem do JSON e da chave 'email' se foram enviados
    if not data or 'email' not in data:
        return jsonify({'error':'Nenhum dado JSON enviado'}), 400
    
    #Tratamento de erros
    try:
        #Faz a separação dos dados pegando apenas o conteúdo do 'email'
        get_email = data.get('email')
        analysis_result = email_analysis(get_email)

        if 'error' in analysis_result:
            return jsonify(analysis_result), 500

        #Faz a separação de 'categoria' e 'resposta_sugerida' da resposta bruta
        categoria = analysis_result.get('categoria')
        resposta_sugerida = analysis_result.get('resposta_sugerida')

        #Caso a resposta venha com quebras de linhas imbutidas no texto, isso faz a limpeza delas
        if resposta_sugerida:
            resposta_sugerida.replace('\n', ' ')

        #Transforma a resposta bruta em uma resposta em formato JSON
        return jsonify({
            'categoria': categoria,
            'resposta_sugerida': resposta_sugerida
        })
    except Exception as e:
        return jsonify({
            'ERROR': f'Ocorreu um erro interno ao processar o email: {e}'
        }), 500
        
if __name__ == '__main__':
    app.run(debug=True)