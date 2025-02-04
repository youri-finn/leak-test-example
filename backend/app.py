from flask import Flask, request, jsonify, render_template, send_file
import pandas as pd
import io
import os
import matplotlib.pyplot as plt
from datetime import date

app = Flask(__name__)
UPLOAD_FOLDER = '/tmp/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['POST', 'GET'])
def home():

    average = None

    first_name = 'Youri'
    last_name = 'Penders'
    today = date.today()

    if request.method == 'POST':

        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']

        if file.filename == "":
            return jsonify({'error': 'No selected file'}), 400

        if file.filename.endswith(('.xls', '.xlsx')):
            filepath = os.path.join(UPLOAD_FOLDER, 'uploaded_temporary_data.xls')
            file.save(filepath)
            df = pd.read_excel(file)
        else:
            return jsonify({'error': 'Unsupported file format'}), 400

        average = df.Temperature.mean()

    return render_template('index.html', prenom=first_name, nom=last_name, vandaag=today, average=average)

@app.route('/plot')
def decay_plot():

    filepath = os.path.join(UPLOAD_FOLDER, 'uploaded_temporary_data.xls')
    df = pd.read_excel(filepath)

    plt.figure()
    plt.plot(df.Date, df.Temperature, label='Temperature')
    plt.plot(df.Date, df.Pressure, label='Pressure')
    plt.xlabel('Date')
    plt.ylabel('Temperature / Pressure')
    plt.title('Pressure Decay Test Plot')
    plt.legend()

    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)

    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
