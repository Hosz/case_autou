import json
from flask import Flask, request, jsonify, render_template
from main import email_analysis, extract_text_from_pdf
import os

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'temp_uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Rota do Front/Interface
@app.route('/', methods=['GET'])
def homepage():
    return render_template('index.html')

#Define uma rota com o metodo "POST"
@app.route('/process-email', methods=['POST'])
def process_email():
    content_to_analyze = None

    #Checagem se algum arquivo foi enviado
    if request.files:

        #Extrai o texto do arquivo
        uploaded_file = request.files.get('email_file')

        #Verifica se há um arquivo ou se tem algum arquivo nomeado, caso contrario exibe um erro
        if not uploaded_file or not uploaded_file.filename:
            return jsonify({'error': 'O arquivo não existe'}), 400
        
        safe_filename = uploaded_file.filename.replace(" ", "_")
        temp_filepath = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)

        try:
            uploaded_file.save(temp_filepath)

            if temp_filepath.endswith('.pdf'):
                content_to_analyze = extract_text_from_pdf(temp_filepath)
                if not content_to_analyze:
                    return jsonify({'error': 'Falha ao ler o arquivo PDF.'}), 400

            elif temp_filepath.endswith('.txt'):
                with open(temp_filepath, 'r', encoding='utf-8') as f:
                    content_to_analyze = f.read()

            else:
                return jsonify({'error': 'Tipo de arquivo não permitido.'}), 400
                
        finally:
            if os.path.exists(temp_filepath):
                os.remove(temp_filepath)

    elif request.is_json:       
        data = request.get_json()

        #Checagem do JSON e da chave 'email' se foram enviados
        if not data or 'email' not in data:
            return jsonify({'error':'Nenhum dado JSON enviado'}), 400
        
        content_to_analyze = data.get('email')
    
    if not content_to_analyze:
        return jsonify({'error': 'Nenhum conteúdo para analisar foi fornecido.'}), 400
        
    #Tratamento de erros
    try:
        #Faz a separação dos dados pegando apenas o conteúdo do 'email'
        analysis_result = email_analysis(content_to_analyze)

        if 'error' in analysis_result:
            return jsonify(analysis_result), 500

        #Faz a separação de 'categoria' e 'resposta_sugerida' da resposta bruta
        categoria = analysis_result.get('categoria')
        rascunho_resposta = analysis_result.get('rascunho_resposta')
        acao_interna = analysis_result.get('acao_interna')     

        #Transforma a resposta bruta em uma resposta em formato JSON
        return jsonify({
            'categoria': categoria,
            'rascunho_resposta': rascunho_resposta,
            'acao_interna': acao_interna
        })
    except Exception as e:
        return jsonify({
            'error': f'Ocorreu um erro interno ao processar o email: {e}'
        }), 500
        
if __name__ == '__main__':
    app.run(debug=True)