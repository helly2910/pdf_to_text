from flask import Flask, render_template, request, send_file, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from datetime import datetime
import fitz
import os
import time

app = Flask(__name__)
app.secret_key = '1d91145d7f43f915023da009f51340ae82e177cc0f8757a7be40ac4c89070e91'  # Set your secret key here
# UPLOAD_FOLDER = 'D:/Python Project/pdf_to_word/PDW_convertor/PWC_Flask/uploads'

def get_upload_folder():
    try:
        # Try to use the absolute path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(script_dir, 'PWC_Flask/uploads')
    except:
        # If absolute path fails, use the relative path as fallback
        return 'PWC_Flask/uploads'

UPLOAD_FOLDER = get_upload_folder()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Add 'os' module to the Jinja2 environment
app.jinja_env.globals['os'] = os

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        pdf_files = request.files.getlist('pdf_files')
        output_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'output')
        os.makedirs(output_dir, exist_ok=True)

        output_files = []
        for pdf_file in pdf_files:
            pdf_path = save_pdf_file(pdf_file)
            output_file = convert_pdf_to_text(pdf_path,output_dir)
            output_files.append(output_file)

        # Store the list of converted texts in the session
        session['converted_files'] = output_files

        return redirect(url_for('result'))

    return render_template('index.html')

@app.route('/result')
def result():
    # Retrieve the list of converted texts from the session
    converted_files = session.get('converted_files', [])

    output_dir = os.path.join(app.config['UPLOAD_FOLDER'],'output')
    output_files = [os.path.join(output_dir,file)for file in converted_files]

    return render_template('result.html', output_files=output_files)

@app.route('/download/<path:filename>')
def download(filename):
    filename = secure_filename(filename)  # Sanitize the filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output', filename)
    
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        flash('File not found.')
        return redirect(url_for('result'))

def save_pdf_file(file):
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
    file.save(pdf_path)
    return pdf_path

def convert_pdf_to_text(pdf_path, output_dir):
    base_name = os.path.basename(pdf_path)
    base_name_no_ext = os.path.splitext(base_name)[0]

    current_timestamp = int(datetime.now().timestamp())

    output_file = os.path.join(output_dir, f"{base_name_no_ext}_{current_timestamp}.txt")
    
    text = ''
    pdf_document = fitz.open(pdf_path)
    
    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        text += page.get_text('text')

    pdf_document.close()
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(text)

    return output_file

if __name__ == '__main__':
    app.run(debug=True, port=5000)

