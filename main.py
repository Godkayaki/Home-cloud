#!/usr/bin/python3
#-*- coding: utf-8 -*-
#Daniel Gonzalez
# 
# Home-cloud

from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import MultipleFileField, FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'

class UploadFileForm(FlaskForm):
    file = MultipleFileField("File(s) Upload", validators=[InputRequired()])
    submit = SubmitField("Upload File")

@app.route('/', methods=['GET',"POST"])
@app.route('/home', methods=['GET',"POST"])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        files = form.file.data # First grab the file
        return_value = ""
        #print(files)
        
        for file in files:
            file_path = os.path.join(os.path.abspath(os.path.dirname(__file__))) + "/" + str(app.config['UPLOAD_FOLDER']) + "/" + str(file.filename)
            
            if os.path.isfile(file_path): 
                return_value = return_value + file_path + " -> file already exists.\n"
            else:
                file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) # Then save the file
                return_value = return_value + file_path + " -> file uploaded.\n"
        
        return return_value
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
    #app.run()