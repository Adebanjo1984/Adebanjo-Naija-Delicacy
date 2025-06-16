from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
db = SQLAlchemy(app)

# --- Database Tables ---

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(200))
    role = db.Column(db.String(50), default='customer')

class FoodItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    category = db.Column(db.String(100))
    price = db.Column(db.Float)
    image_url = db.Column(db.String(200))
    available = db.Column(db.Boolean, default=True)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.String(50), default='open')

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))
    food_item_id = db.Column(db.Integer, db.ForeignKey('food_item.id'))
    quantity = db.Column(db.Integer)
    price_at_order_time = db.Column(db.Float)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    payment_method = db.Column(db.String(50))
    payment_status = db.Column(db.String(50))
    transaction_reference = db.Column(db.String(100))

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    message = db.Column(db.Text)
    status = db.Column(db.String(50), default='unread')

class SupportTicket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    issue = db.Column(db.Text)
    status = db.Column(db.String(50), default='open')

@app.route('/')
def home():
    food_items = FoodItem.query.all()
    return render_template('home.html', food_items=food_items)

if __name__ == '__main__':
    if not os.path.exists('database.db'):
        db.create_all()
    app.run(debug=True)
