from model import connect_to_db
import unittest # name of module that will import module refer to module .name as test case like random.choice 
from server import app # just app we need we dont need another func from server 

class FlaskTests(unittest.TestCase):
# test case s class n unitmodule and then we r inhertg from that class 
# all of methods we define n inside flask class r able to refer to methods that testcase wld have by using self i.e. obj orinetn  

    def setUp(self):# self is instance of self object i.e. test case 
        """Stuff to do before every test."""
      

        self.client = app.test_client()
        app.config['TESTING'] = True
        connect_to_db(app, "postgresql:///testdb")

    

    def test_some_flask_route(self):
        """Some non-database test..."""
        # checking for response =200

        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)# it is n http req is successful
        self.assertIn(b'<h1>Welcome to the Stock-Market!</h1>', result.data)# getting from result data 


    def test_signup(self):
        """Test login page."""
        #login email and login password

        result = self.client.post("/login",
                                data={"login-email": "russell00@williams.biz", "login-password": "F!s1n1VuLs"},
                                follow_redirects=True)
        self.assertIn(b"All Stocks", result.data) 

        

    def test_login(self):
        """Test login page."""
        #login email and login password

        result = self.client.post("/login",
                            data={"login-email": "russell00@williams.biz", "login-password": "F!s1n1VuLs"},
                            follow_redirects=True)
        self.assertIn(b"All Stocks", result.data)

    

# def test_logout(self):
#     result = self.client.get('/logout')
#     self.assertEqual(result.status_code, 200)# redirect is 300 is good .# 400 is browser and inspect n console,
#     self.assertIn(b'<h1>All Stocks</h1>', result.data)#   client side # 500 in server.py


    def test_logout(self):
        

        # Check response code
        response = self.client.get('/logout')
        self.assertEqual(response.status_code, 302)

        # Check 'Log out' in response
        self.assertTrue('Log out', response.data)


    # # def set_up(self):
    # #     result =self.client.get()
    def test_favorites(self):
        """Test login page. login email and login password"""
       # 
       

        self.client.post("/login",
                data={"login-email": "russell00@williams.biz", "login-password": "F!s1n1VuLs"},
                follow_redirects=False)
        
# 
        result = self.client.get('/make_favorite')
        self.assertEqual(result.status_code,200 )# it is n http req is successful
        self.assertIn(b'<a href="/">Go back to Home</a>', result.data)

    def test_makefavorites(self):

        self.client.post("/login",
                data={"login-email": "russell00@williams.biz", "login-password": "F!s1n1VuLs"},
                follow_redirects=False)

        result = self.client.post("/make_favorite",
                            data={"stock_symbol": "AAC", "user_id":1},
                            follow_redirects=True)
        self.assertIn(b"AAC", result.data) 

  

if __name__ == '__main__':
    
    unittest.main()