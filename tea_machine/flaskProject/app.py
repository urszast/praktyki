from flask import Flask, render_template, request
import requests

app = Flask(__name__)
app_url = "http://localhost:8000"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/zaparzenie', methods=['GET', 'POST'])
def zaparzenie():
    rodzaj = request.form['rodzaj']
    response = requests.get(f"{app_url}/tea/zaparzenie/{rodzaj}")
    wynik = response.json().get("wynik_czynnosci")
    return render_template('wynik.html', wynik=wynik)


@app.route('/sprawdzenie', methods=['POST'])
def sprawdzenie():
    rodzaj = request.form['rodzaj']
    response = requests.get(f"{app_url}/tea/sprawdzenie/{rodzaj}")
    wynik = response.json().get("wynik_czynnosci")
    return render_template('wynik.html', wynik=wynik)


@app.route('/dodanie', methods=['POST'])
def dodanie():
    rodzaj = request.form['rodzaj']
    ilosc = request.form['ilosc']
    response = requests.get(f"{app_url}/tea/dodanie/{rodzaj}/{ilosc}")
    wynik = response.json().get("wynik_czynnosci")
    return render_template('wynik.html', wynik=wynik)


if __name__ == '__main__':
    app.run(debug=True)
