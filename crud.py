from model import db, User, Favorite, Stock, connect_to_db

def create_user(name, email, password):
    """Create and return a new user."""

    user = User(name=name, email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user

def get_users():
    return User.query.all()

def get_user_by_id(user_id):
    return User.query.get(user_id)

def make_stock(stock_symbol,companyname):
    stock= Stock(stock_symbol=stock_symbol,companyname=companyname)

    db.session.add(stock) 
    db.session.commit()
    return stock

def get_stock():
    return Stock.query.all()

def favorite(user_id,stock_symbol):
    new_favorite =Favorite(user_id=user_id,stock_symbol=stock_symbol)
    # i have to put first my stocktable and create users from usertable then do fav #add some database n ur temrinal createtestuser
    db.session.add(new_favorite)
    db.session.commit()
    return new_favorite
    

    

def get_favorite():
    return Favorite.query.all()



if __name__ == '__main__':
    from server import app
    connect_to_db(app)