from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Projekt- und Aufgabenmanagementsystem</h1><p>Die Anwendung läuft erfolgreich.</p>"

if __name__ == "__main__":
    app.run(debug=True)