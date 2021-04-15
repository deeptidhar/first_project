import os
import csv
import crud
import model
import server
import requests 
import random
from faker import Faker 


os.system('dropdb analyzing-stocks')
os.system('createdb analyzing-stocks')

model.connect_to_db(server.app)
model.db.create_all()

faker = Faker()

for _ in range(20):
    email = faker.email()
    password= faker.password()
    name = faker.name()
    print(email,password,name)
    crud.create_user(email, password, name)



with open('listing_status.csv', 'r') as read_obj:
#res = requests.get(url, params=params)
#decoded = res.content.decode('utf-8')
    csv_read = csv.reader(read_obj, delimiter=',', skipinitialspace=True)
    SymbolList = []
    for row in csv_read:
        if row[0] not in SymbolList:
            SymbolList.append(row[0])
            crud.make_stock(row[0],row[1])

# want to write new fun that will add fav records
# make a list called users,
# second list ten stk symbols just pick twenty 
# we would getting users to write query
# loop thorugh all users and call make fav frm crud.py
#userid ,and to pick stck use random choice fun of from ur list of ten 

def add_favorite():
    users = model.User.query.all()

    favorite_stocks=['AMZN','NFLX','AMC','ASMB','BAR','BCM','EIRL','FYT','HCIC','OSCR','QELL','PYT','QLV','RACE','RADA','SAF','SAB']


    for element in users:
        random_stock = random.choice(favorite_stocks)
        new_favoriteitem =model.Favorite(user_id = element.user_id, stock_symbol = random_stock)

        model.db.session.add(new_favoriteitem)
        model.db.session.commit()
        print(new_favoriteitem)

add_favorite()


def get_stocks():
    stocks = model.Stock.query.all()


get_stocks()

        

        
        
        
    








    




