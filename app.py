from flask import Flask, request, jsonify
from main import class_email, response_email

app = Flask(__name__)

@app.route('/process-email', methods=['POST'])
def process_email():
    dados = request.get_json()
    if not dados or 'email' not in dados:
        return jsonify({'ERROR':'Nenhum dado JSON enviado'}), 400
    try:
        get_email = dados.get('email')
        tipo_email = class_email(get_email)
        resposta = response_email(tipo_email)

        return jsonify({
            'categoria': tipo_email,
            'resposta': resposta
        })
    except Exception as e:
        return jsonify({
            'ERROR': 'Ocorreu um erro interno ao processar o email'
        }), 500

if __name__ == '__main__':
    app.run(debug=True)