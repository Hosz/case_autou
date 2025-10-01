document.addEventListener('DOMContentLoaded', () => {
    const emailTextArea = document.getElementById('email-text')
    const analyzeBtn = document.getElementById('analyze-btn')
    const resultDiv = document.getElementById('result-container')
    const loader = document.getElementById('loader')
    const tabButtons = document.querySelectorAll('.tab-btn')
    const tabPanes = document.querySelectorAll('.tab-pane')
    const dropZone = document.querySelector('.drop-zone')
    const fileInput = document.querySelector('.drop-zone__input')
    
    let selectedFile = null

    //Função chamada quando o botão "Analisar" é clicado.
    //Ela valida a entrada, mostra o loading, chama a API e exibe o resultado
    async function handAnalyzeClick() {
        //Descobre qual aba (texto ou arquivo) está ativa para saber onde pegar os dados.
        const isTextTabActive = document.querySelector('#tab-text').classList.contains('active')
        let payload = null  //É o que será enviado para o back-end

        if (isTextTabActive) {
            //Se a aba de texto for a ativa, o payload será da "textarea"
            const emailText = emailTextArea.value
            if (!emailText.trim()) {
                alert('Por favor, insira o texto de um e-mail.')
                return
            }
            payload = emailText
        } else {
            //Se a aba de arquivo for a ativa, o payload será o arquivo selecionado
            if (!selectedFile) {
                alert('Por favor, selecione ou arraste um arquivo primeiro.')
                return
            }
            payload = selectedFile
        }
        
        //Ativa o estado de "carregando" na interface antes de chamar a APIa
        resultDiv.style.display = 'none'
        analyzeBtn.style.display = 'none'
        loader.style.display = 'block'

        try {
            //Chama a função da API e espera pelo resultado
            const analysisResult = await fetchAnalysis(payload)
            
            //Mostra a área de resultado
            resultDiv.style.display = 'block'

            //Checa se o back-end retornou um erro e exibe
            if (analysisResult.error) {
                resultDiv.innerHTML = `<strong>Erro:</strong> ${analysisResult.error}`
            } else {
                //Monta o HTML do resultado
                const result = analysisResult
                const categoryClass = result.categoria === 'Produtivo' ? 'badge-produtivo' : 'badge-improdutivo'

                let detailsHtml = ''

                //Monta a seção de detalhes de forma diferente para cada categoria
                if (result.categoria === 'Produtivo') {
                    detailsHtml = `
                        <div class='response-container'>
                            <p class='suggested-response'>${result.rascunho_resposta}</p>
                            <button id='copy-btn'>Copiar</button>
                        </div>
                    `
                } else { //Improdutivo
                    detailsHtml = `<p class='suggested-response'><strong>Ação Interna:</strong> ${result.acao_interna}</p>`
                    if (result.rascunho_resposta) {
                        detailsHtml += `
                            <div class='response-container' style='margin-top: 1rem;'>
                                <strong class='result-label'>Rascunho de Resposta (Opcional):</strong>
                                <p class='suggested-response'>${result.rascunho_resposta}</p>
                                <button id='copy-btn'>Copiar</button>
                            </div>
                        `
                    }
                }

                //Junta tudo e coloca na página
                resultDiv.innerHTML = `
                    <div class='result-item'>
                        <strong class='result-label'>Categoria:</strong>
                        <span class='category-badge ${categoryClass}'>${result.categoria}</span>
                    </div>
                    <div class='result-item' style='display: block; align-items: initial;'>
                          ${detailsHtml}  
                    </div>`;

                //Adiciona funcionalidade ao botão copiar quando ele estiver na página
                const copyBtn = document.getElementById('copy-btn')
                if (copyBtn) {
                    copyBtn.addEventListener('click', () => {
                        navigator.clipboard.writeText(result.rascunho_resposta).then(() => {
                            copyBtn.textContent = 'Copiado!'
                            setTimeout(() => { copyBtn.textContent = 'Copiar'; }, 2000)
                        })
                    })
                }
            }
    } catch (e) {
        resultDiv.style.display = 'block'
        resultDiv.innerHTML = `<strong>Erro Inesperado:</strong> Ocorreu um problema na interface.`
        console.error('Erro em handAnalyzeClick', e)
    } finally {
        analyzeBtn.style.display = 'block'
        loader.style.display = 'none'
    }}
        
    //Fetch: Apenas para se comunicar com o back-end
    async function fetchAnalysis(payload) {
        let requestBody;
        let requestHeaders = {}
        
        //Checa se estamos enviando um texto ou arquivo
        if (typeof payload === 'string') {
            requestHeaders['Content-Type'] = 'application/json'
            requestBody = JSON.stringify({ email: payload})
        } else {
            const formData = new FormData()
            formData.append('email_file', payload)
            requestBody = formData
        }
        //Tenta fazer a chamada de rede para a API
        try {
            const response = await fetch('/process-email', {
                method: 'POST',
                headers: requestHeaders,
                body: requestBody,
            });
            const data = await response.json()
            return data
            
        } catch (error) {
            console.error('Erro no fetch:', error)
            return {error: 'Falha ao se comunicar com a API'}
        }
    }

    //Faz a leitura do conteúdo do arquivo como uma "tradutora"
    function readFileAsText(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader()
            reader.onload = () => resolve(reader.result)
            reader.onerror = () => reject(reader.error)
            reader.readAsText(file)
        })
    }
    
    //Faz a caixa de texto crescer com o conteúdo
    function auto_grow(element) {
        element.style.height = '5px'
        element.style.height = (element.scrollHeight) + 'px'
    }

    //Adiciona uma ação quando o usuário seleciona um arquivo clicando no seletor
    fileInput.addEventListener('change', () => {
        selectedFile = fileInput.files[0]
        const promptSpan = dropZone.querySelector('.drop-zone__prompt')
        promptSpan.innerHTML = `Arquivo selecionado: <strong>${selectedFile.name}</strong>`
    })

    //Ações na área de colocar o arquivo para quando arrasta pra dentro ou fora da área e quando soltar
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('drop-zone--over');
    })
    dropZone.addEventListener('dragleave', (e) => {
        dropZone.classList.remove('drop-zone--over');
    })
    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('drop-zone--over')
        const files = e.dataTransfer.files
        if (files.length) {
            console.log('Arquivo solto:', files[0])
            selectedFile = files[0]
            const fileName = files[0].name
            const promptSpan = dropZone.querySelector('.drop-zone__prompt')
            promptSpan.innerHTML = `Arquivo selecionado: <strong>${fileName}</strong>`
        }
    })

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetId = button.dataset.tab

            tabButtons.forEach(btn => {
                btn.classList.remove('active')
            }) 

            tabPanes.forEach(pane => {
                pane.classList.remove('active')
            })

            button.classList.add('active')
            document.getElementById(targetId).classList.add('active')
        })
    })

    analyzeBtn.addEventListener('click', handAnalyzeClick)
    emailTextArea.addEventListener('input', () => auto_grow(emailTextArea));  
});
 