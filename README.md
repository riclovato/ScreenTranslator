# Tradutor de Tela

O **Tradutor de Tela** é uma aplicação que permite capturar textos diretamente da tela, processá-los para correção e traduzi-los para diferentes idiomas. O foco inicial está na tradução para inglês e chinês, mas o suporte a outros idiomas também está disponível.

---

## Funcionalidades

- **Captura de Tela Completa:** Captura toda a tela do computador.
- **Captura de Área Selecionada:** Permite selecionar uma área específica para captura.
- **Reconhecimento Óptico de Caracteres (OCR):** Extrai textos das imagens capturadas.
- **Processamento de Texto:** Limpa e formata o texto extraído, corrigindo erros comuns de OCR.
- **Tradução Multilíngue (Em Desenvolvimento):** Planejada integração com APIs de tradução gratuitas.

---

## Como Usar

1. Instale as dependências necessárias:
   ```bash
   pip install -r requirements.txt

2. Certifique-se de que o Tesseract OCR está instalado e configurado.
Atualize o caminho no arquivo ocr_processor.py, caso necessário:

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

3. Execute a aplicação:
    python main.py


## Estrutura do Projeto

- **main.py:** Interface principal e fluxo da aplicação.
- **screenshot.py:** Módulo para captura de tela.
- **ocr_processor.py:** Responsável pela extração de texto via OCR.
- **text_processor.py:** Limpeza e formatação do texto extraído.
- **translator.py:** (Em desenvolvimento) Integração com API de tradução.
