from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User_Listing_Association(db.Model):
    __tablename__ = 'user-listing-association'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    listing_id = db.Column(db.Integer, db.ForeignKey('listing.id'), primary_key=True)
    extra_data = db.Column(db.String(50))
    user = db.relationship("User", back_populates="listings")
    listings = db.relationship("Listing", back_populates="seller") #back_populates = 'user' for symmetry?
    
    def __init__(self, **kwargs):
        self.extra_data = kwargs.get('extra_data', '')

class Book_Listing_Association(db.Model):
    __tablename__ = 'book-listing-association'
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True)
    listing_id = db.Column(db.Integer, db.ForeignKey('listing.id'), primary_key=True)
    extra_data = db.Column(db.String(50))
    book = db.relationship("Book", back_populates="listings")
    listings = db.relationship("Listing", back_populates="book")
    
    def __init__(self, **kwargs):
        self.extra_data = kwargs.get('extra_data', '')

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    netid = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)
    pfp = db.Column(db.String, nullable=True)
    listings = db.relationship("User_Listing_Association", back_populates="user")
    
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
            'listings' : [listing.listing_id for listing in self.listings]
        }

class Listing(db.Model):
    __tablename__ = 'listing'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    price = db.Column(db.String, nullable =False)
    course = db.Column(db.String, nullable=False)
    condition = db.Column(db.String, nullable=False)
    notes = db.Column(db.String(300), nullable=False)
    image = db.Column(db.String, nullable =True)
    seller = db.relationship("User_Listing_Association", back_populates='listings')
    book =  db.relationship("Book_Listing_Association", back_populates="listings")
    
    def __init__(self, **kwargs):
        self.title = kwargs.get('title', 'Untitled')
        self.price = kwargs.get('price', '0.00')
        self.course = kwargs.get('course', '')
        self.condition = kwargs.get('condition', '')
        self.notes = kwargs.get('notes', '')
        self.image = kwargs.get('image', None)

    def serialize(self):
        return {
            'id' : self.id,
            'title' : self.title,
            'price' : self.price, 
            'condition': self.condition, 
            'notes' : self.notes,
            'image' : self.image,
            'course' : self.course,
            'seller' : self.seller[0].user_id, 
            'book' : self.book[0].book_id
        }

class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    course = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable =True)
    listings = db.relationship("Book_Listing_Association", back_populates='book')
    
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
            'listings' : [listing.listing_id for listing in self.listings]
        } 