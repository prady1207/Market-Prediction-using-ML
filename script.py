import pandas as pd
import numpy as np
import matplotlib as mlp
import seaborn as sb
import yfinance as yf
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# Configuring the SQLite database file path

db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Initialize the database
db = SQLAlchemy(app)

# Define a Database Model (Table)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

@app.route("/")
def home():
    # Fetch all users from the database
    users = User.query.all()
    if not users:
        return "Connected to SQLite! Database is empty. Go to /add/yourname to add data."
    
    user_list = ", ".join([user.username for user in users])
    return f"Users in database: {user_list}"

# Temporary route to add a user to the database
@app.route("/add/<name>")
def add_user(name):
    try:
        new_user = User(username=name)
        db.session.add(new_user)
        db.session.commit()
        return f"Successfully added {name}! Go back to home page to see list."
    except Exception as e:
        db.session.rollback()
        return f"Error: User might already exist or {str(e)}"

if __name__ == "__main__":
    # Create the database tables automatically before launching
    with app.app_context():
        db.create_all()
    app.run(debug=True)



# # Getting the info for apple stock price
# apple = yf.Ticker("AAPL")


# # Get historical market data for 1 year
# hist = apple.history(period="1y")

# print(hist.head())

# # Getting company info
# print(apple.info)