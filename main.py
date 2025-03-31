from flask import Flask, request, send_file, jsonify
from markdown_pdf import MarkdownPdf, Section
import os
import tempfile
import uuid

app = Flask(__name__)

def convert_md_to_pdf(md_content, output_file):
    pdf = MarkdownPdf(toc_level=2)
    pdf.add_section(Section(md_content))
    pdf.meta["title"] = "Converted Document"
    pdf.save(output_file)
    return output_file

@app.route('/convert', methods=['POST'])
def convert_endpoint():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not file.filename.lower().endswith('.md'):
        return jsonify({'error': 'File must be a Markdown (.md) file'}), 400

    try:
        temp_dir = tempfile.mkdtemp()
        md_content = file.read().decode('utf-8')
        pdf_filename = f"{uuid.uuid4().hex}.pdf"
        pdf_path = os.path.join(temp_dir, pdf_filename)
        
        convert_md_to_pdf(md_content, pdf_path)
        
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=f"{os.path.splitext(file.filename)[0]}.pdf",
            mimetype='application/pdf'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/test', methods=['GET'])
def test():
    return "testing", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
