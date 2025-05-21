from flask import Blueprint, render_template, request
import os
from werkzeug.utils import secure_filename
from .utils.processor import summarize_pdf, generate_flashcards

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pdf = request.files['pdf']
        filename = secure_filename(pdf.filename)
        filepath = os.path.join('uploaded_pdfs', filename)
        pdf.save(filepath)

        summary = summarize_pdf(filepath)
        flashcards = generate_flashcards(summary)

        return render_template('result.html', summary=summary, flashcards=flashcards)

    return render_template('index.html')