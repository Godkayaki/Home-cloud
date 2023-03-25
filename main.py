#!/usr/bin/python3
#-*- coding: utf-8 -*-
#Daniel Gonzalez
# 
#Home-cloud

from flask import Flask, render_template, send_file
from flask_wtf import FlaskForm
from wtforms import MultipleFileField, FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired

#storage location
destination_path = 'static/files'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = destination_path

#uploading button form section
class UploadFileForm(FlaskForm):
    file = MultipleFileField("File(s) Upload", validators=[InputRequired()])
    submit = SubmitField("Upload File")

#define routes
@app.route('/', methods=['GET',"POST"], defaults={'req_path': ''})
@app.route('/<path:req_path>')
def home(req_path):
    #if from listed elements the on clicked is a file redirect to download
    if os.path.isfile(current_path):
        return send_file(current_path, as_attachment=True)

    #define empty file list that will be shown    
    file_list = []
    
    #define current path
    current_path = ""
    if destination_path.endswith("/") or req_path.startswith("/"):
        current_path = destination_path + req_path
    else:
        current_path = destination_path + "/" + req_path
    
    #define form to upload files
    form = UploadFileForm()

    #add a first starting "." that will be used as 'go to previous dir'
    file_list = os.listdir(current_path)
    file_list.insert(0,".")
    print(file_list)

    #manage uploading files
    if form.validate_on_submit():
        files = form.file.data # First grab the file
        return_value = ""
        
        for file in files:
            file_path = os.path.join(os.path.abspath(os.path.dirname(__file__))) + "/" + str(app.config['UPLOAD_FOLDER']) + "/" + str(file.filename)
            
            if os.path.isfile(file_path): 
                return_value = return_value + file_path + " -> file already exists.\n"
            else:
                file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) # Then save the file
                return_value = return_value + file_path + " -> file uploaded.\n"
        
        return return_value
    return render_template('index.html', form=form, files=file_list)

if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')