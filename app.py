from flask import Flask, render_template, request, jsonify
import os
import re
import datetime
# import the repository file (db.py)?? or is db a flask library -- I think it's a library
import db
from models import Book

app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     return 'Hello World!'


# Insert the seed data from db.py only if there's no file already called 'books.db'
if not os.path.isfile('books.db'):
    db.connect()


@app.route("/")
def index():
    # render_template is a Flask method for returning html and other markup formats using Python template engine Jinja2
    # draws from a templates folder in the file structure (this is where I'll put the compiled code after building the vue front-end)
    return render_template("index.html")

# This checks if sign-in email is a valid email


def isValid(email):
    regex = re.compile(
        r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(regex, email):
        return True
    else:
        return False

# request from flask is the object that contains all the request data; must be imported

# must import jsonify for formatting request data


@app.route("/request", methods=['POST'])
def postRequest():
    req_data = request.get_json()
    email = req_data['email']

    # check if user is logged in and email is valid
    if not isValid(email):
        return jsonify({
            'status': '422',
            'res': 'failure',
            'error': 'Invalid email format. Please enter a valid email address'
        })
    # check if book is already in library
    title = req_data['title']
    bks = [b.serialize() for b in db.view()]
    for b in bks:
        if b['title'] == title:
            return jsonify({
                # 'error': '',
                'res': f'Error! Book with title {title} is already in the database!',
                'status': '404'
            })
# serialize is converting data objects into forms that can be stored
    bk = Book(db.getNewId(), True, title, datetime.datetime.now())
    print('new book: ', bk.serialize())

    return jsonify({
        # 'error': '',
        'res': bk.serialize(),
        'status': '200',
        'msg': 'Success creating a new book!'
    })

# NOTE yay! Post request done, but don't forget to stop and start your server to respin "flask run"


@app.route('/request', methods=['GET'])
def getRequest():
    content_type = request.headers.get('Content-Type')
    bks = [b.serialize() for b in db.view()]
    if (content_type == 'application/json'):
        json = request.json
        for b in bks:
            if b['id'] == int(json['id']):
                return jsonify({
                    # 'error': '',
                    'res': b,
                    'status': '200',
                    'msg': 'Success getting all books in library!'
                })
        return jsonify({
            'error': f"Error! Book with id '{json['id']} not found!",
            'res': '',
            'status': '404'
        })
    else:
        return jsonify({
            # 'error': '',
            'res': bks,
            'status': '200',
            'msg': 'Success getting all books in library!',
            'no_of_books': len(bks)
        })


@app.route('/request/<id>', methods=['GET'])
def getRequestId(id):
    req_args = request.view_args
    print('req_args: ', req_args)
    bks = [b.serialize() for b in db.view()]
    if req_args:
        for b in bks:
            if b['id'] == int(req_args['id']):
                return jsonify({
                    # 'error': '',
                    'res': b,
                    'status': '200',
                    'msg': 'Success getting book by ID!'
                })

            return jsonify({
                'error': f"Error! Book with id '{req_args['id']}' was not found",
                'res': '',
                'status': '404'
            })
    else:
        return jsonify({
            # 'error': '',
            'res': bks,
            'status': '200',
            'msg': 'Success getting book by ID',
            'no_of_books': len(bks)
        })


if __name__ == '__main__':
    app.run()
