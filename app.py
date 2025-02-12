from flask import Flask, request, send_file
from pdf2docx import Converter
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return "<h1>PDF to Word Converter API</h1><p>Use POST /convert with a PDF file.</p>"

@app.route('/convert', methods=['POST'])
def convert_pdf_to_word():
    if 'file' not in request.files:
        return {"error": "No file uploaded"}, 400
    
    pdf_file = request.files['file']
    if not pdf_file.filename.lower().endswith(".pdf"):
        return {"error": "Invalid file type. Please upload a PDF."}, 400
    
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file.filename)
    pdf_file.save(pdf_path)
    
    word_path = pdf_path.replace(".pdf", ".docx")
    
    try:
        cv = Converter(pdf_path)
        cv.convert(word_path, start=0, end=None)
        cv.close()
    except Exception as e:
        return {"error": f"Conversion failed: {str(e)}"}, 500
    
    return send_file(word_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
