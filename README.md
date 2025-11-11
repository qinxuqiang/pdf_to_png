# PDF to PNG Conversion API

A minimal Flask API that converts the first page of a PDF file to PNG format.

## Requirements

- Python 3.7+
- poppler-utils (system dependency for pdf2image)

### Install poppler-utils

**macOS:**
```bash
brew install poppler
```

**Ubuntu/Debian:**
```bash
sudo apt-get install poppler-utils
```

**Windows:**
Download from: https://github.com/oschwartz10612/poppler-windows/releases/

## Installation

1. Clone or download this repository

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the server:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

2. Convert a PDF to PNG:

**Using curl:**
```bash
curl -X POST -F "file=@your_document.pdf" http://localhost:5000/convert --output output.png
```

**Using Python requests:**
```python
import requests

with open('your_document.pdf', 'rb') as f:
    response = requests.post('http://localhost:5000/convert', files={'file': f})
    
if response.status_code == 200:
    with open('output.png', 'wb') as out:
        out.write(response.content)
```

## API Endpoints

### POST /convert
Converts the first page of a PDF to PNG.

- **Request:** multipart/form-data with a `file` field containing the PDF
- **Response:** PNG image (image/png)
- **Max file size:** 16MB

### GET /
Health check endpoint that returns API status and available endpoints.

## Error Responses

- `400` - Bad request (no file provided, invalid file type)
- `500` - Server error (conversion failed)

