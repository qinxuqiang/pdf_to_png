from flask import Flask, request, send_file, jsonify
from pdf2image import convert_from_bytes
from io import BytesIO
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size


@app.route('/convert', methods=['POST'])
def convert_pdf_to_png():
    """Convert the first page of a PDF to PNG and return it."""
    
    # Check if file is present in request
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    # Check if file has a filename
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Check if file is a PDF
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'File must be a PDF'}), 400
    
    try:
        # Read PDF file content
        pdf_bytes = file.read()
        
        # Convert first page only (first_page=1, last_page=1)
        images = convert_from_bytes(pdf_bytes, first_page=1, last_page=1)
        
        if not images:
            return jsonify({'error': 'Failed to convert PDF'}), 500
        
        # Get the first (and only) page
        first_page = images[0]
        
        # Save to BytesIO object
        img_io = BytesIO()
        first_page.save(img_io, 'PNG')
        img_io.seek(0)
        
        # Return PNG file
        return send_file(
            img_io,
            mimetype='image/png',
            as_attachment=False,
            download_name='converted_page.png'
        )
        
    except Exception as e:
        return jsonify({'error': f'Conversion failed: {str(e)}'}), 500


@app.route('/', methods=['GET'])
def index():
    """Serve the HTML frontend."""
    return send_file('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4999)

