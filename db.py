from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

################# Change serializations. 

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    netid = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)
    pfp = db.Column(db.String, nullable=False)
    listings = db.relationship("Listing", back_populates='user', cascade="delete, delete-orphan")
    
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.netid = kwargs.get('netid', '')
        self.pfp = kwargs.get('pfp', '')

    def serialize(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'netid' : self.netid,
            'pfp' : self.pfp,
            'listings' : [listing.id for listing in self.listings]
        }

class Listing(db.Model):
    __tablename__ = 'listing'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    price = db.Column(db.String, nullable =False)
    course = db.Column(db.String, nullable=False)
    condition = db.Column(db.String, nullable=False)
    notes = db.Column(db.String(300), nullable=False)
    image = db.Column(db.String, nullable =False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates='listings', cascade="save-update")
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    book = db.relationship("Book", back_populates='listings', cascade="save-update")
    
    def __init__(self, **kwargs):
        self.title = kwargs.get('title', 'Untitled')
        self.price = kwargs.get('price', '0.00')
        self.course = kwargs.get('course', '')
        self.condition = kwargs.get('condition', '')
        self.notes = kwargs.get('notes', '')
        self.image = kwargs.get('image', '')

        self.user = kwargs.get('user')
        self.book = kwargs.get('book')

    def serialize(self):
        return {
            'id' : self.id,
            'title' : self.title,
            'price' : self.price, 
            'condition': self.condition, 
            'notes' : self.notes,
            'image' : self.image,
            'course' : self.course,
            'seller' : self.user.id,
            'book' : self.book.id
        }

class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    course = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable =False)
    listings = db.relationship("Listing", back_populates='book', cascade="delete, delete-orphan")
    
    def __init__(self, **kwargs):
        self.title = kwargs.get('title', '')
        self.course = kwargs.get('course', '')
        self.image = kwargs.get('image', '')

    def serialize(self):
        return {
            'id' : self.id,
            'title' : self.title,
            'course' : self.course,
            'image' : self.image,
            'listings' : [listing.id for listing in self.listings]
        } 