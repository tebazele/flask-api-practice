from flask import Flask, render_template
import os
# import the repository file (db.py)
import db
app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     return 'Hello World!'

# if __name__ == '__main__':
#     app.run()

# Insert the seed data from db.py only if there's no file already called 'books.db'
if not os.path.isfile('books.db'):
    db.connect()


@app.route("/")
def index():
    # render_template is a Flask method for returning html and other markup formats using Python template engine Jinja2
    # draws from a templates folder in the file structure (this is where I'll put the compiled code after building the vue front-end)
    return render_template("index.html")
