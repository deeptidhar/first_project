
from flask_sqlalchemy import SQLAlchemy 
#import crud
db = SQLAlchemy()

class User(db.Model):
    """A user."""


    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True) # create a form in which i should have name ,email and password
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'

class Stock(db.Model):
    """A stocktable."""

    __tablename__ = 'stocks'

    stock_symbol = db.Column(db.String, primary_key=True,unique=True)
    companyname = db.Column(db.String)

    
    def __repr__(self):
        return f'<symbol={self.stock_symbol} companyname={self.companyname}>'

class Favorite(db.Model):
    """A userfavorite table."""

    __tablename__ = 'favorites'

    user_favorite_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id= db.Column(db.Integer, db.ForeignKey('users.user_id'))
    stock_symbol = db.Column(db.String, db.ForeignKey('stocks.stock_symbol'))

    def __repr__(self):
        return f'<user_id={self.user_id} stock_symbol ={self.stock_symbol}>'

    stock = db.relationship('Stock', backref='favorites')
    user = db.relationship('User', backref='favorites')




def connect_to_db(app, db_uri='postgresql:///analyzing-stocks', echo=False):
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_ECHO'] = echo
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = app
    db.init_app(app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app

    #app = Flask(__name__)
    connect_to_db(app)

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    
    