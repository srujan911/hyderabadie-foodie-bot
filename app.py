# app.py (Simplified Version)

from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Web server is running. The main chatbot logic is in bot.py."

if __name__ == '__main__':
    app.run(debug=True)