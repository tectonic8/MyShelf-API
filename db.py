from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User_Book_Association(db.Model):
    __tablename__ = 'user-book-association'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True)
    extra_data = db.Column(db.String(50))
    user = db.relationship("User", back_populates="books")
    books = db.relationship("Book", back_populates="seller")
    
    def __init__(self, **kwargs):
        self.extra_data = kwargs.get('extra_data', '')

class Course_Book_Association(db.Model):
    __tablename__ = 'course-book-association'
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True)
    extra_data = db.Column(db.String(50))
    course = db.relationship("Course", back_populates="books")
    books = db.relationship("Book", back_populates="courses")
    
    def __init__(self, **kwargs):
        self.extra_data = kwargs.get('extra_data', '')

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    netid = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String, nullable =False)
    pfp = db.Column(db.String, nullable =True)
    books = db.relationship("User_Book_Association", back_populates="user")
    
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.netid = kwargs.get('netid', '')
        self.pfp = kwargs.get('pfp', None)

    def serialize(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'netid' : self.netid,
            'pfp' : self.pfp,
            'books' : [book.book_id for book in self.books]
        }

class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    price = db.Column(db.String, nullable =False)
    condition = db.Column(db.String, nullable=False)
    notes = db.Column(db.String(300), nullable=False)
    image = db.Column(db.String, nullable =True)
    seller = db.relationship("User_Book_Association", back_populates='books')
    courses = db.relationship("Course_Book_Association", back_populates='books')

    
    def __init__(self, **kwargs):
        self.title = kwargs.get('title', 'Untitled')
        self.price = kwargs.get('price', '0.00')
        self.condition = kwargs.get('condition', '')
        self.notes = kwargs.get('notes', '')

    def serialize(self):
        courses = []
        for course in self.courses:
                courses.append((Course.query.filter_by(id=course.course_id).first()).title)
        return {
            'id' : self.id,
            'title' : self.title,
            'courses' : courses,
            'price' : self.price, 
            'condition': self.condition, 
            'image' : self.image,
            'notes' : self.notes,
            'seller' : self.seller.serialize()
        }

class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    college = db.Column(db.String, nullable=False)
    books = db.relationship("User_Book_Association", back_populates='course')

    def __init__(self, **kwargs):
        self.title = kwargs.get('title', '')
        self.college = kwargs.get('college', '')

    def serialize(self):
        return {
            'id' : self.id,
            'title' : self.title,
            'college' : self.college,
            'books' : [book.book_id for book in self.books]
        }