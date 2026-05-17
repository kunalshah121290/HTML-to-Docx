from flask import Flask, request, send_file, render_template
from bs4 import BeautifulSoup
from docx import Document
import os
import zipfile

app = Flask(__name__)

def html_to_docx(html_content, output_file):
    doc = Document()
    soup = BeautifulSoup(html_content, 'html.parser')

    for element in soup.find_all():
        if element.name == 'p':
            doc.add_paragraph(element.text)
        elif element.name == 'h1':
            doc.add_heading(element.text, level=1)
        elif element.name == 'h2':
            doc.add_heading(element.text, level=2)
        elif element.name == 'li':
            doc.add_paragraph(element.text, style='List Bullet')

    doc.save(output_file)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    files = request.files.getlist('files')
    zip_path = "converted_files.zip"

    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in files:
            if file.filename.endswith(".html"):
                html_content = file.read().decode('utf-8')
                output_name = file.filename.replace(".html", ".docx")

                html_to_docx(html_content, output_name)
                zipf.write(output_name)

    return send_file(zip_path, as_attachment=True)

if __name__ == "__main__":
    app.run()