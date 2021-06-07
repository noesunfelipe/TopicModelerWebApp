import os
import pandas as pd
import openpyxl
import werkzeug.utils
from flask import Flask, render_template, request, session
from flask import send_file, send_from_directory, safe_join, abort
from werkzeug.utils import secure_filename
import jdk
import json



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] ="./ReceptorArchivos"
# The absolute path of the directory containing CSV files for users to download
app.config["CLIENT_CSV"] = "./CSVFolder"
app.config["TEMP_DATA"] = "./TempData"
app.config["MALLET_PATH"]= ".\mallet-2.0.8"
app.config["STATIC"] = ".\static"



@app.route('/')
def home():
    os.system('python Cleaner.py') 
    return render_template('home.html')

@app.route('/uploader', methods=['POST'])
def uploader(): 
    if request.method == "POST":
        f = request.files['archivo']
        filename = secure_filename(f.filename)
        FPATHNAME = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        f.save(FPATHNAME)
        return show_tables(filename)


@app.route('/tables')
def show_tables(filename):
    data = pd.read_excel(os.path.join(app.config['UPLOAD_FOLDER'], filename), engine='openpyxl')
    data.set_index(['caso_numero'], inplace=True)
    data.index.name = None
    return render_template('Confirm.html', tables=[data.to_html(max_rows = 10)],  titles = ['caso_numero', 'reclamo_descripcion'])
    
@app.route('/parametros/', methods =['GET', 'POST'])
def set_params():
    #NTopics = request.form['Ntopic']
    #with open ("C:/Users/Felipe/Desktop/TopicModelerApp - Python/src/TempData/parametros.json", 'w') as f:
    #    json.dump(NTopics, f, indent =2)
    #print(NTopics)
    #os.system('python App.py') 
    os.system('python Preprocess.py')
    return render_template('SelectorParametros.html')

@app.route('/parametros_fin/', methods =['GET', 'POST'])
def set_parametros_fin():
    NTopicsFin = request.form['NTopicsFin']
    ModeloSelec = request.form['Modelos']
    NTOPICSPATH = os.path.join(app.config["TEMP_DATA"], "NTopicsFin.json")
    MODELOSELECTPATH = os.path.join(app.config["TEMP_DATA"], "ModeloSelec.json")
    
    with open(NTOPICSPATH, 'w') as f:
        json.dump(NTopicsFin, f, indent =2)
    
    with open(MODELOSELECTPATH, 'w') as f:
        json.dump(ModeloSelec, f, indent =2)
    
    print(NTopicsFin, ModeloSelec)

    os.system('python FinalPre-Process.py') 
    return render_template('Out.html')


@app.route('/my-link/', methods =['GET','POST'])
def my_link():
    print ('I got clicked!')
    os.system('python Preprocess.py')  
    return 'Click'


@app.route("/get-csv/topico_dominante.csv", methods =['GET', 'POST'])
def get_csv():

    filename = "topico_dominante.csv"
    #filename = f"{csv_id}.csv"

    try:
        return send_from_directory(app.config["CLIENT_CSV"], filename=filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)



@app.route('/about')
def about():
    return render_template('about.html')



if __name__ == '__main__':
    app.run(debug=True)