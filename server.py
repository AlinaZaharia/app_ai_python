from flask import Flask
from flask import request
from main import returneaza_raspuns_final
from flask_cors import CORS

app = Flask(__name__)

CORS(app)
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/intrebare', methods=['POST'])
def adreseaza_intrebare():
    print(request.json['key'])
    print(request.json['titlu'])
    intrebare = request.json['key']
    titlu = request.json['titlu']
    raspuns_final = returneaza_raspuns_final(intrebare, titlu)
    # print(raspuns_final)
    return raspuns_final


