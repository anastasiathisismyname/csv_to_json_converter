from flask import Flask, flash, request, redirect, render_template, Response, jsonify
from werkzeug.utils import secure_filename
import os.path
from os import listdir
from os.path import isfile, join
from src.script_pandas import *


app = Flask(__name__)


root_dir = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = f'{root_dir}\\uploaded_csv_files'
json_folder = f'{root_dir}\\returned_json_files'


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():

    if request.method == 'POST':

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No selected file')

            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            files = [f for f in listdir(UPLOAD_FOLDER) if isfile(join(UPLOAD_FOLDER, f))]

            json_data = get_json_data(os.path.join(app.config['UPLOAD_FOLDER'], files[0]))
            response = Response(headers={'Access-Control-Allow-Origin': '*'})
            response.set_data(json.dumps(json_data))

            delete_file(os.path.join(UPLOAD_FOLDER, files[0]))
            delete_file(os.path.join(json_folder, files[0]))

            return json_data
    else:
        return render_template('index.html')
