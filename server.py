import requests # req s lib
from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db
import crud
from jinja2 import StrictUndefined
from datetime import datetime, date, time
import os

app = Flask(__name__)
app.secret_key = 'dev'
app.jinja_env.undefined = StrictUndefined


stocks=['Aapl','AMZN','NFLX','AMC','ASMB','BAR','BCM','EIRL','FYT','HCIC','OSCR','QELL','PYT','QLV','RACE','RADA','SAF','SAB']


@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')


@app.route('/stocks')
def get_stocks():
    
    stocks = request.args.get("stock")
    stocks=crud.get_stocks()

    return render_template('stocks.html',stocks=stocks) 


@app.route('/favorites')# to do put user_id in session instead try that out 
def favorites():
    """Shows favorite stocks for a logged in user"""

    favorites = crud.get_favorites(session['user_id'])# key in session as attributes as user_id which is string 
    

    return render_template('favorites.html', favorites=favorites)
    
@app.route('/deletefavorites',methods =['GET','POST'])
def delete_favorites():

    if request.method == 'POST': # if it is delete the favorites from database

        db.session.delete(favorites)
        db.session.commit()
        return redirect('/')
    else:
        return redirect('/')


@app.route('/make_favorite', methods =['GET', 'POST'])
def make_favorite():# rendering a page
    if request.method == 'POST':
        stock_symbol = request.form.get('stock_symbol')
        user_id = session['user_id']

        crud.make_favorite(user_id, stock_symbol)

        return redirect('/favorites')
    else: 
        stocks = request.args.get("stock")
        stocks=crud.get_stocks()

        return render_template('make_favorite.html',stocks=stocks)





@app.route('/login',methods =["POST"])
def log_in():# old user is trying to login and sign wld be new 
    #log_in = crud.get_login
    email = request.form.get('login-email')
    user = crud.get_user_by_email(email)
    print(email)
    print(user)
    if user and user.password == request.form.get("login-password"):# if i find u or not ,if user will be true exists and otherway F
        session["user_id"] = user.user_id #it has coloumn and we need to get value of it
        
        flash("User Logged In")
        return redirect('/stocks')
    else :
        
        return redirect('/')


    
    # check email matches email n database and password n form and check if both match then add it to session based on adding to session and get link to stks

# route (logout)

@app.route('/logout')
def log_out():#clear the session
    if 'user_id' in session :

       # session.clear(['user_id'])
        del session['user_id']

    return redirect('/')

# sign up with Post method renders ur email,passwrd,name and user 
@app.route('/signup',methods=['POST'])
def sign_up():
    email=request.form.get('register-email')
    password=request.form.get('register-password')
    name=request.form.get('name')
    user=crud.create_user(email,password,name)


    return redirect('/')

# used Get method so that i can go on sign up html page 
@app.route('/signupform',methods=['GET'])
def signform():
    return render_template('/signup.html')


    

# @app.route('/users')
# def all_users():
#     """View all users."""

#     users = crud.get_users()
#     print (users)
#     return render_template('all_users.html', users=users)




@app.route('/users', methods=['POST'])
def register_user():
    """Create a new user."""

    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)
    if user:
        flash('Cannot create an account with that email. Try again.')
    else:       
        crud.create_user(email, password)
        flash('Account created! Please log in.')

    return redirect('/')



@app.route('/show_searchpage')# two routes need one is to display and one is to handle it 
def search_page():
   return render_template('searchpage.html')

@app.route('/handle_search')
def handle_search():
    search_term = request.args.get('search_term')#it matches the search page in html file #in python it has variable is using 
    search_term = search_term.upper()
    stock = crud.get_stock_by_symbol(search_term)
    # we should check that stk is not none if it s none error HHAHA!!,
    
    
    
    url="https://www.alphavantage.co/query"#endpoint
    
    payload ={'function':'TIME_SERIES_DAILY','symbol':stock.stock_symbol,'apikey': os.environ.get("TICKETMASTER_KEY")}#making dic
    #param=apikey,stocks,func,o/psize
    print(payload)
    response = requests.get(url,params=payload) #it is getting from lib not from flask
    # print(response.url)
    # HTML MAKE SHOW _SEARCH RESULT AND THEN USE pass in render template with jinja to display that nicer for loop 
    data = response.json() #make a template displaying stock_price#user click on stock and they want to see current price
    # dates = sorted([date for date in data['Time Series (Daily)'].keys()])# return list 
    dates = []
    prices = []# prices r the object for seven
    print ('*********************')
    print(data)
    print('***************')
    for date in data['Time Series (Daily)'].keys():# data is dic .time series=keys for val,
        dates.append(date)

    for date in reversed(sorted(dates)[-7:]):# for sorted these dates by string int  last seven ,reverse it deceding order
        date_obj = datetime.strptime(date, "%Y-%m-%d")# turn into date obj as it was string ,day,mth,year formt
        prices.append((date_obj.strftime("%A, %B %d %Y"), data['Time Series (Daily)'][date]))# one tuple containg stk prices and date


    return render_template('/show_searchresult.html', stock=stock, prices=prices)#p=list of seven obj containing open and closing for seven pr
    
    

def select_stocks():
    return render_template('/getprice.html')

    






if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)