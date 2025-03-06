#!/usr/bin/python3
#-*- coding: utf-8 -*-
#Drg - Godkayaki
#Home-Cloud 
#app.py

import os
import shutil
import tempfile
import zipfile
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, send_file, redirect, url_for

# Configuration
UPLOAD_FOLDER = 'static/uploads'  # Base directory for storage
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'nef'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Check if file type is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Home Route - Directory Navigation
@app.route('/', defaults={'req_path': ''})
@app.route('/<path:req_path>')
def home(req_path):
    base_path = os.path.abspath(app.config['UPLOAD_FOLDER'])
    current_path = os.path.abspath(os.path.join(base_path, req_path))

    if not current_path.startswith(base_path):
        return "Access Denied!", 403

    if os.path.isfile(current_path):
        return send_file(current_path, as_attachment=True)

    files = os.listdir(current_path)
    
    # Separate folders and files, then sort each group
    folders = sorted([f for f in files if os.path.isdir(os.path.join(current_path, f))])
    files = sorted([f for f in files if os.path.isfile(os.path.join(current_path, f))])

    file_list = folders + files  # Folders first, then files
    parent_path = os.path.relpath(os.path.dirname(current_path), base_path) if req_path else ''
    
    return render_template('index.html', files=file_list, current_path=req_path, parent_path=parent_path)

# File Upload Route
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.referrer)

    files = request.files.getlist('file')  # Get multiple files
    req_path = request.form.get('req_path', '')  
    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], req_path)  

    os.makedirs(upload_path, exist_ok=True)  # Ensure directory exists

    for file in files:
        if file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(upload_path, filename))

    return redirect(request.referrer)

# Bulk download all files within the current directory
@app.route('/download-all', methods=['GET'])
def download_all():
    req_path = request.args.get('req_path', '')
    base_path = os.path.abspath(app.config['UPLOAD_FOLDER'])
    current_path = os.path.abspath(os.path.join(base_path, req_path))

    if not current_path.startswith(base_path):
        return "Access Denied!", 403

    # Create a temporary ZIP file
    temp_dir = tempfile.mkdtemp()
    zip_filename = os.path.join(temp_dir, 'files.zip')

    # Zip the directory
    shutil.make_archive(zip_filename[:-4], 'zip', current_path)

    # Send the ZIP file
    return send_file(zip_filename, as_attachment=True)

# Alternative to specifying the favicon
#@app.route('/favicon.ico')
#def favicon():
#    return '', 204  # Return empty response with HTTP 204 (No Content)

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')