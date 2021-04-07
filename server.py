from flask import Flask
import crud


app = Flask(__name__)
app.secret_key = 'dev'





# Replace this with routes and view functions!


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)