from flask import Flask, request, jsonify
from main import email_analysis
import os

app = Flask(__name__)

#Define uma rota com o metodo "POST"
@app.route('/process-email', methods=['POST'])
def process_email():
    data = request.get_json()

    #Checagem do JSON e da chave 'email' se foram enviados
    if not data or 'email' not in data:
        return jsonify({'error':'Nenhum dado JSON enviado'}), 400
    
    #Tratamento de erros
    try:
        get_email = data.get('email')
        analysis_result = email_analysis(get_email)

        if 'error' in analysis_result:
            return jsonify(analysis_result), 500

        categoria = analysis_result.get('categoria')
        resposta_sugerida = analysis_result.get('resposta_sugerida')

        if resposta_sugerida:
            resposta_sugerida.replace('\n', ' ')

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