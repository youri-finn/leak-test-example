from flask import Flask, render_template
from datetime import date

app = Flask(__name__)

@app.route('/')
def home():
    first_name = 'Youri'
    last_name = 'Penders'
    today = date.today()
    return render_template('index.html', prenom = first_name, nom = last_name, vandaag = today)

if __name__ == '__main__':
    app.run(port=8080)
