from flask import Flask, flash, request, redirect, render_template, Response, jsonify
from werkzeug.utils import secure_filename
import os.path
from os import listdir
from os.path import isfile, join
import json
import pandas as pd


app = Flask(__name__)

# root_dir = os.path.dirname(os.path.abspath(__file__))
# CSV_FOLDER = f'{root_dir}/uploaded_csv_files'
# JSON_FOLDER = f'{root_dir}/returned_json_files'
# app.config['UPLOAD_FOLDER'] = CSV_FOLDER
# app.config['JSON_FOLDER'] = JSON_FOLDER

csv_uploads_dir = os.path.join(app.instance_path, 'csv_uploads')
json_uploads_dir = os.path.join(app.instance_path, 'json_uploads')

os.makedirs(csv_uploads_dir, exists_ok=True)
os.makedirs(json_uploads_dir, exists_ok=True)

app.config['csv_uploads_dir'] = csv_uploads_dir
app.config['json_uploads_dir'] = json_uploads_dir

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

            file.save(os.path.join(app.config['csv_uploads_dir'], filename))

            files = [f for f in listdir(app.config['csv_uploads_dir']) if isfile(join(app.config['csv_uploads_dir'], f))]

            json_data = get_json_data(os.path.join(app.config['csv_uploads_dir'], files[0]))
            response = Response(headers={'Access-Control-Allow-Origin': '*'})
            response.set_data(json.dumps(json_data))

            filename = get_filename(os.path.join(app.config['csv_uploads_dir'], files[0]))
            json_filename = filename + '.json'

            delete_file(os.path.join(app.config['csv_uploads_dir'], files[0]))
            delete_file(os.path.join(app.config['json_uploads_dir'], json_filename))

            return json_data
    else:
        return render_template('index.html')


def get_filename(path):
    filename = path.split('/')[-1].split('.')[0]
    return filename


def get_json_data(path):
    df = pd.read_csv(path)

    folder_path = "/".join(path.split('/')[:-1])
    filename = get_filename(path)

    json_path = folder_path + '/' + filename + '.json'

    df.to_json(json_path)
    with open(json_path) as f:
        return json.loads(f.read())


def delete_file(path):
    os.remove(path)


port = int(os.environ.get('PORT', 5000))
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)