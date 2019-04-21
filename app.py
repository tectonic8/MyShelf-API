import json
from flask import Flask, request
from db import db, User, Book, Course, User_Book_Association, Course_Book_Association

app = Flask(__name__)
db_filename = 'myshelf.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/')
def root():
    return 'Hello world!'

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
    course = Course.query.filter_by(title=course_name).first()
    if course is not None:
        books = course.serialize()['books']
        return json.dumps({'success':True, 'data':books}), 200
    else:
        return json.dumps({'success':False, 'error':'This course doesn\'t exist.'}), 404

@app.route('/api/books/user/<int:netid>/', methods=['GET'])
def get_books_by_seller(netid):
    """
    Returns a list of dictionary representations of all books being sold by the
    given user. Method takes a net ID. 
    """
    user = Course.query.filter_by(id=netid).first()
    if user is not None:
        books = user.serialize()['books']
        return json.dumps({'success':True, 'data':books}), 200
    else:
        return json.dumps({'success':False, 'error':'This user doesn\'t exist.'}), 404

@app.route('/api/books/book/<string:book_title>/', methods=['GET'])
def get_book_by_title(book_title):
    """
    Returns a dictionary representations of the book with the given title
    """
    book = Book.query.filter_by(title=book_title).first()
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

@app.route('/api/courses/', methods=['GET'])
def get_courses():
    """
    Returns a list of dictionary representations of all courses in the database.
    """
    courses = Course.query.all()
    res = {'success':True, 'data': [course.serialize() for course in courses]}
    return json.dumps(res), 200

@app.route('/api/courses/<string:title>/', methods=['GET'])
def get_course_by_title(title):
    """
    Returns a dictionary representations of the course with the given title. 
    """
    course = Course.query.filter_by(title=title).first()
    if course is not None:
        return json.dumps({'success':True, 'data':course.serialize()}), 200
    else:
        return json.dumps({'success':False, 'error':'This course doesn\'t exist.'}), 404

@app.route('/api/users/', methods=['POST'])
def create_user():
    """
    Takes a name and a net ID. Profile picture not implemented.
    """
    post_body = json.loads(request.data)
    user = User(name=post_body['name'], name=post_body.get('netid'))
    db.session.add(user)
    db.session.commit()
    res = {'success':True, 'data':user.serialize()}
    return json.dumps(res), 201

@app.route('/api/books/', methods=['POST'])
def add_book():
    """
    Takes a title, price, net ID (of seller), and course. Can also take a 
    condition and notes. 
    """
    with db.session.no_autoflush:
        post_body = json.loads(request.data)
        user = User.query.filter_by(netid=post_body['netid']).first()
        if user is None:
            return json.dumps({'success':False, 'error':'This user class does not exist.'}), 404
        course = Course.query.filter_by(title=post_body['course']).first()
        if course is None:
            # https://classes.cornell.edu/api/2.0/search/classes.json?roster=FA14&subject=MATH
            course = Course(title = post_body['course'], college="Arts and Sciences")
        book = Book(title=post_body['title'], price=post_body['price'], condition=post_body['condition'], notes=post_body['notes'])
        
        a1 = User_Book_Association()
        a1.user = user
        a1.books = book

        a2 = Course_Book_Association()
        a2.course = course 
        a2.books = book

        db.session.add(a1)
        db.session.add(a2)
        db.session.commit()
        res = {'success':True, 'data':book.serialize()}
        return json.dumps(res), 201

@app.route('/api/class/<int:book_id>/', methods=["DELETE"])
def remove_book_by_id(book_id):
    book = Book.query.filter_by(id=book_id).first()
    if book is not None:
        db.session.delete(book)
        db.session.commit()
        return json.dumps({'success':True, 'data':book.serialize()}), 200
    return json.dumps({'success':False, 'error':'This book doesn\'t exist.'}), 404



# @app.route('/api/classes/', methods=['GET'])
# def get_classes():
#     classes = Class.query.all()
#     res = {'success':True, 'data': [clas.serialize() for clas in classes]}
#     return json.dumps(res), 200

# @app.route('/api/classes/', methods=['POST'])
# def create_class():
#     post_body = json.loads(request.data)
#     clas = Class(code=post_body['code'], name=post_body.get('name'))
#     db.session.add(clas)
#     db.session.commit()
#     res = {'success':True, 'data':clas.serialize()}
#     return json.dumps(res), 201
    
# @app.route('/api/class/<int:class_id>/', methods=['GET'])
# def get_class(class_id):
#     clas = Class.query.filter_by(id=class_id).first()
#     if clas is not None:
#         return json.dumps({'success':True, 'data':clas.serialize()}), 200
#     else:
#         return json.dumps({'success':False, 'error':'This class doesn\'t exist.'}), 404

# @app.route('/api/class/<int:class_id>/', methods=["DELETE"])
# def delete_class(class_id):
#     clas = Class.query.filter_by(id=class_id).first()
#     if clas is not None:
#         db.session.delete(clas)
#         db.session.commit()
#         return json.dumps({'success':True, 'data':clas.serialize()}), 200
#     return json.dumps({'success':False, 'error':'This class doesn\'t exist.'}), 404

# @app.route('/api/users/', methods=['POST'])
# def create_user():
#     post_body = json.loads(request.data)
#     user = User(name=post_body['name'], netid=post_body.get('netid'))
#     db.session.add(user)
#     db.session.commit()
#     res = {'success':True, 'data':user.serialize()}
#     return json.dumps(res), 201

# @app.route('/api/user/<int:user_id>/', methods=['GET'])
# def get_user(user_id):
#     user = User.query.filter_by(id=user_id).first()
#     if user is not None:
#         return json.dumps({'success':True, 'data':user.serialize()}), 200
#     else:
#         return json.dumps({'success':False, 'error':'This user doesn\'t exist.'}), 404

# @app.route('/api/class/<int:class_id>/add/', methods=['POST'])
# def add_user_to_class(class_id):
#     with db.session.no_autoflush:
#         post_body = json.loads(request.data)
#         clas = Class.query.filter_by(id=class_id).first()
#         user = User.query.filter_by(id=post_body['user_id']).first()
#         if clas is not None and user is not None:
#             a = Association(extra_data = post_body['type'])
#             a.clas = clas
#             user.classes.append(a)
#             db.session.add(a)
#             db.session.commit()
#             res = {'success':True, 'data':clas.serialize()}
#             return json.dumps(res), 201
#         return json.dumps({'success':False, 'error':'This user and/or class doesn\'t exist.'}), 404

# @app.route('/api/class/<int:class_id>/assignment/', methods=['POST'])
# def add_assignment_to_class(class_id):
#     with db.session.no_autoflush:
#         if Class.query.filter_by(id=class_id).first() is not None:
#             post_body = json.loads(request.data)
#             assignment = Assignment(description=post_body['description'], due_date=post_body['due_date'], id=class_id)
#             db.session.add(assignment)
#             db.session.commit()
#             res = {'success':True, 'data':assignment.serialize()}
#             return json.dumps(res), 201
#         return json.dumps({'success':False, 'error':'This class doesn\'t exist.'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
