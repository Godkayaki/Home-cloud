#!/usr/bin/python3
#-*- coding: utf-8 -*-
#Drg - Godkayaki
#Home-Cloud 
#app.py

import json
import zipfile
import shutil
import tempfile
from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_wtf import FlaskForm
from wtforms import MultipleFileField, SubmitField, StringField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired

# Configuration
CONFIG_FILE = "config.json"

# Load storage path from JSON file
def load_storage_path():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            return data.get("storage_path", "static/files")  # Default path
    return "static/files"

# Save storage path to JSON file
def save_storage_path(path):
    with open(CONFIG_FILE, "w") as f:
        json.dump({"storage_path": path}, f)

# Ensure the directory exists
def ensure_directory_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)  # Create folder if missing

# Initialize storage path
destination_path = load_storage_path()
ensure_directory_exists(destination_path)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = destination_path

# Upload form
class UploadFileForm(FlaskForm):
    file = MultipleFileField("Upload File(s)", validators=[InputRequired()])
    submit = SubmitField("Upload")

# Change storage path form
class ChangePathForm(FlaskForm):
    new_path = StringField("New Storage Path", validators=[InputRequired()])
    change = SubmitField("Change Path")

# Check if file type is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Home Route - Directory Navigation
@app.route('/', methods=['GET', 'POST'], defaults={'req_path': ''})
@app.route('/<path:req_path>', methods=['GET', 'POST'])
def home(req_path):
    global destination_path
    destination_path = load_storage_path()

    # Resolve full path
    current_path = os.path.join(destination_path, req_path)

    # If a file is clicked, download it
    if os.path.isfile(current_path):
        return send_file(current_path, as_attachment=True)

    # Upload form
    upload_form = UploadFileForm()
    if upload_form.validate_on_submit():
        for file in upload_form.file.data:
            file_path = os.path.join(current_path, secure_filename(file.filename))
            file.save(file_path)

    # Change storage path form
    change_path_form = ChangePathForm()
    if change_path_form.validate_on_submit():
        new_path = change_path_form.new_path.data
        if os.path.exists(new_path):
            save_storage_path(new_path)
            app.config['UPLOAD_FOLDER'] = new_path
            return redirect(url_for('home'))

    # Handle missing folder
    if not os.path.exists(current_path):
        os.makedirs(current_path)  # Auto-create missing directories

    # List files and folders
    try:
        file_list = sorted(os.listdir(current_path), key=lambda x: (not os.path.isdir(os.path.join(current_path, x)), x.lower()))
    except FileNotFoundError:
        file_list = []  # If directory is missing, show an empty list

    return render_template('index.html', upload_form=upload_form, change_path_form=change_path_form, files=file_list, current_path=req_path, storage_path=destination_path)

# Set storage path
@app.route('/set-storage-path', methods=['POST'])
def set_storage_path():
    data = request.get_json()
    new_path = data.get("new_path")
    
    if os.path.exists(new_path) and os.path.isdir(new_path):
        save_storage_path(new_path)
        app.config['UPLOAD_FOLDER'] = new_path
        return jsonify({"success": True, "message": "Storage path updated!", "new_path": new_path})
    
    return jsonify({"success": False, "message": "Invalid directory!"})

# Bulk download all files within the current directory
@app.route('/download-all', methods=['GET'])
def download_all():
    req_path = request.args.get('req_path', '')
    base_path = load_storage_path()
    current_path = os.path.abspath(os.path.join(base_path, req_path))

    if not current_path.startswith(base_path):
        return "Access Denied!", 403

    temp_dir = tempfile.mkdtemp()
    zip_filename = os.path.join(temp_dir, 'files.zip')

    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(current_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, current_path))

    return send_file(zip_filename, as_attachment=True)

# Alternative to specifying the favicon
#@app.route('/favicon.ico')
#def favicon():
#    return '', 204  # Return empty response with HTTP 204 (No Content)

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')