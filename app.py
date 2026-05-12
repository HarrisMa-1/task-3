from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def home():
    app_name = os.getenv("APP_NAME", "Render Flask App")
    return f"<h1>{app_name} UPDATED</h1>"

if __name__ == "__main__":
    app.run(debug=True)