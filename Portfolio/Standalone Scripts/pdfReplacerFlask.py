from flask import Flask, request, render_template, send_file
from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('pdfReplacer.html')

questionNum = 1

@app.route('/update_pdf', methods=['POST'])
def update_pdf():
    global questionNum

    question = request.form['question']
    answer = request.form['answer']
    template_path = 'template.pdf'
    output_path = 'output.pdf'

    pdf = PdfReader(template_path)
    writer = PdfWriter()
    for page in pdf.pages:
        text = page.extract_text()
        text = text.replace(f'QUESTION_PLACEHOLDER {questionNum}', question)
        text = text.replace(f'ANSWER_PLACEHOLDER {questionNum}', answer)
        
        # Create a new PDF page with the modified text using reportlab
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.drawString(100, 750, text)
        can.save()

        # Move to the beginning of the StringIO buffer
        packet.seek(0)
        new_pdf = PdfReader(packet)
        new_page = new_pdf.pages[0]
        writer.add_page(new_page)

    with open(output_path, 'wb') as f:
        writer.write(f)

    questionNum += 1
    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run()