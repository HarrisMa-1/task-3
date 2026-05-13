from flask import Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

# Render compatibility fix
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

@app.route("/", methods=["GET", "POST"])
def home():
    with app.app_context():
        db.create_all()

    if request.method == "POST":
        note_text = request.form["content"]

        new_note = Note(content=note_text)

        db.session.add(new_note)
        db.session.commit()

        return redirect("/")

    notes = Note.query.all()

    html = """
    <h1>Student Notes App</h1>

    <form method="POST">
        <input type="text" name="content" placeholder="Enter note" required>
        <button type="submit">Add Note</button>
    </form>

    <hr>
    """

    for note in notes:
        html += f"""
        <p>
            {note.content}
            <a href='/delete/{note.id}'>Delete</a>
        </p>
        """



    return html

@app.route("/delete/<int:id>")
def delete(id):

    note = Note.query.get(id)

    if note:
        db.session.delete(note)
        db.session.commit()

    return redirect("/")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)