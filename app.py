#!/usr/bin/env python3
"""
Flask server for IFC Graph Viewer
Handles file uploads and runs build_graphml.py to generate GraphML files
"""

import os
import subprocess
import tempfile
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

# Output path for GraphML (matches build_graphml.py default)
OUTPUT_PATH = os.path.join(DATA_DIR, 'facility')


@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('.', 'index.html')


@app.route('/data/<path:filename>')
def serve_data(filename):
    """Serve files from the data directory"""
    return send_from_directory(DATA_DIR, filename)


@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files (images, etc.)"""
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    return send_from_directory(static_dir, filename)


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle IFC file upload and generate GraphML"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.lower().endswith('.ifc'):
        return jsonify({'error': 'File must be a .ifc file'}), 400
    
    try:
        filename = secure_filename(file.filename)
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(temp_path)
        
        script_path = os.path.join(os.path.dirname(__file__), 'build_graphml.py')
        
        result = subprocess.run(
            ['python3', script_path, temp_path, '--output', OUTPUT_PATH],
            capture_output=True,
            text=True,
            timeout=300  # timeout after 5 minutes
        )
        
        # Clean up 
        try:
            os.remove(temp_path)
        except OSError:
            pass
        
        if result.returncode != 0:
            error_msg = result.stderr or result.stdout or 'Unknown error occurred'
            return jsonify({
                'error': 'Failed to generate graph',
                'details': error_msg
            }), 500
        
        return jsonify({
            'success': True,
            'message': 'Graph generated successfully',
            'output': result.stdout
        })
        
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Processing timed out. File may be too large.'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("Starting IFC Graph Generator server...")
    print("Open http://localhost:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5000)
