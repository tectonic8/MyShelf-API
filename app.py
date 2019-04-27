import json
import os
from urllib.parse import unquote
from flask import Flask, request
from db import db, User, Book, Listing, User_Listing_Association, Book_Listing_Association

app = Flask(__name__)
db_filename = 'myshelf.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/')
def main():
    return "hi daniel"

@app.route('/api/books/', methods=['GET'])
def get_books():
    """
    Returns a list of dictionary representations of all books in the database.
    """
    books = Book.query.all()
    res = {'success':True, 'data': [book.serialize() for book in books]}
    return json.dumps(res), 200

@app.route('/api/books/course/<string:course_name>/', methods=['GET'])
def get_books_by_course(course_name):
    """
    Returns a list of dictionary representations of all books associated with 
    the given course. Method takes a course name, ex. CS3110.
    """
    course_name = unquote(course_name)
    books = Book.query.filter_by(course=course_name)
    return json.dumps({'success':True, 'data':[book.serialize() for book in books]}), 200

@app.route('/api/books/book/<string:book_title>/', methods=['GET'])
def get_book_by_title(book_title):
    """
    Returns a dictionary representations of the book with the given title
    """
    book_title = unquote(book_title)
    book = Book.query.filter_by(title=book_title).first()
    if book is not None:
        return json.dumps({'success':True, 'data':book.serialize()}), 200
    else:
        return json.dumps({'success':False, 'error':'This book doesn\'t exist.'}), 404

@app.route('/api/books/book/id/<int:book_id>/', methods=['GET'])
def get_book_by_id(book_id):
    """
    Returns a dictionary representations of the book with the given title
    """
    book = Book.query.filter_by(id=book_id).first()
    if book is not None:
        return json.dumps({'success':True, 'data':book.serialize()}), 200
    else:
        return json.dumps({'success':False, 'error':'This book doesn\'t exist.'}), 404

@app.route('/api/user/<string:netid>/', methods=['GET'])
def get_user_by_netid(netid):
    """
    Returns a dictionary representations of the user with the given net ID. 
    """
    user = User.query.filter_by(netid=netid).first()
    if user is not None:
        return json.dumps({'success':True, 'data':user.serialize()}), 200
    else:
        return json.dumps({'success':False, 'error':'This user doesn\'t exist.'}), 404

@app.route('/api/listing/<int:listing_id>/', methods=['GET'])
def get_listing_by_id(listing_id):
    """
    Returns a dictionary representations of the listing with the given id
    """
    listing = Listing.query.filter_by(id=listing_id).first()
    if listing is not None:
        return json.dumps({'success':True, 'data':listing.serialize()}), 200
    else:
        return json.dumps({'success':False, 'error':'This book doesn\'t exist.'}), 404

@app.route('/api/listings/user/<string:netid>/', methods=['GET'])
def get_listings_by_seller(netid):
    """
    Returns a list of dictionary representations of all listings by the
    given user. Method takes a net ID. 
    """
    user = User.query.filter_by(netid=netid).first()
    if user is not None:
        listings = user.serialize()['listings']
        return json.dumps({'success':True, 'data':[Listing.query.filter_by(id=listing_id).first().serialize() for listing_id in listings]}), 200
    else:
        return json.dumps({'success':False, 'error':'This user doesn\'t exist.'}), 404

@app.route('/api/users/', methods=['POST'])
def create_user():
    """
    Takes a name and a net ID. Profile picture not implemented.
    """
    post_body = json.loads(request.data)
    user = User(name=post_body['name'], netid=post_body.get('netid'), pfp=post_body.get('pfp', None))
    db.session.add(user)
    db.session.commit()
    res = {'success':True, 'data':user.serialize()}
    return json.dumps(res), 201

@app.route('/api/listings/', methods=['POST'])
def add_listing():
    """
    Takes a title, price, net ID (of seller), and course. Can also take a 
    condition and notes and image.
    """
    with db.session.no_autoflush:
        post_body = json.loads(request.data)
        user = User.query.filter_by(netid=post_body['netid']).first()
        if user is None:
            return json.dumps({'success':False, 'error':'This user does not exist.'}), 404
        book = Book.query.filter_by(title=post_body['title']).first()
        if book is None:
            book = Book(title=post_body['title'], course=post_body['course'], image=post_body.get('image', None))
        
        listing = Listing(title=post_body['title'], price=post_body['price'], course=post_body['course'], condition=post_body.get('condition', ''), notes=post_body.get('notes', ''), image=post_body.get('image', None))
        
        a1 = User_Listing_Association()
        a1.user = user
        a1.listings = listing

        a2 = Book_Listing_Association()
        a2.book = book 
        a2.listings = listing

        db.session.add(a1)
        db.session.add(a2)
        db.session.commit()
        res = {'success':True, 'data':listing.serialize()}
        return json.dumps(res), 201

@app.route('/api/listing/<int:listing_id>/', methods=["DELETE"])
def remove_listing_by_id(listing_id):
    listing = Listing.query.filter_by(id=listing_id).first()
    if listing is not None:
        a1 = User_Listing_Association.query.filter_by(listing_id=listing_id).first()
        a2 = Book_Listing_Association.query.filter_by(listing_id=listing_id).first()
        db.session.delete(a1)
        db.session.delete(a2)
        db.session.delete(listing)
        db.session.commit()
        return json.dumps({'success':True, 'data':listing.serialize()}), 200
    return json.dumps({'success':False, 'error':'This listing doesn\'t exist.'}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
