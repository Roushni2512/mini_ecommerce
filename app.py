from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key' # Change this in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database_v2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    # category removed as per user request, kept in DB schema optionally but unused logic

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    
    product = db.relationship('Product')

class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    
    product = db.relationship('Product')

# Routes
@app.route('/')
def home():
    query = request.args.get('q')
    if query:
        products = Product.query.filter(Product.name.ilike(f'%{query}%')).all()
    else:
        products = Product.query.all()
    
    return render_template('home.html', products=products, search_query=query)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['is_admin'] = user.is_admin
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
            
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/cart')
def cart():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    cart_items = CartItem.query.filter_by(user_id=session['user_id']).all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/wishlist')
def wishlist():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    wishlist_items = Wishlist.query.filter_by(user_id=session['user_id']).all()
    return render_template('wishlist.html', wishlist_items=wishlist_items)

@app.route('/toggle_wishlist/<int:product_id>', methods=['POST'])
def toggle_wishlist(product_id):
    if 'user_id' not in session:
        return jsonify({'error': 'login_required'}), 401
    
    item = Wishlist.query.filter_by(user_id=session['user_id'], product_id=product_id).first()
    if item:
        db.session.delete(item)
        action = 'removed'
    else:
        new_item = Wishlist(user_id=session['user_id'], product_id=product_id)
        db.session.add(new_item)
        action = 'added'
    
    db.session.commit()
    return jsonify({'success': True, 'action': action})

@app.route('/add_to_cart/<int:product_id>', methods=['GET', 'POST'])
def add_to_cart(product_id):
    if 'user_id' not in session:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
             return jsonify({'error': 'login_required'}), 401
        return redirect(url_for('login'))
    
    existing_item = CartItem.query.filter_by(user_id=session['user_id'], product_id=product_id).first()
    if existing_item:
        existing_item.quantity += 1
    else:
        new_item = CartItem(user_id=session['user_id'], product_id=product_id)
        db.session.add(new_item)
    
    db.session.commit()

    # Calculate new cart count
    items = CartItem.query.filter_by(user_id=session['user_id']).all()
    count = sum(item.quantity for item in items)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True, 'cart_count': count, 'message': 'Added to cart!'})

    flash('Added to cart!', 'success')
    return redirect(url_for('home'))

@app.route('/update_quantity/<int:item_id>/<action>')
def update_quantity(item_id, action):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    item = CartItem.query.get(item_id)
    if item and item.user_id == session['user_id']:
        if action == 'increase':
            item.quantity += 1
        elif action == 'decrease':
            item.quantity -= 1
            
        if item.quantity <= 0:
            db.session.delete(item)
        
        db.session.commit()
    
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<int:item_id>')
def remove_from_cart(item_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    item = CartItem.query.get(item_id)
    if item and item.user_id == session['user_id']:
        db.session.delete(item)
        db.session.commit()
    
    return redirect(url_for('cart'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        image_url = request.form['image_url']
        
        new_product = Product(name=name, price=price, image_url=image_url)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('admin'))
        
    products = Product.query.all()
    return render_template('admin.html', products=products)

@app.route('/delete_product/<int:product_id>')
def delete_product(product_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('home'))
        
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
    
    return redirect(url_for('admin'))

@app.context_processor
def inject_cart_count():
    if 'user_id' in session:
        # Calculate total quantity of items
        items = CartItem.query.filter_by(user_id=session['user_id']).all()
        count = sum(item.quantity for item in items)
        return dict(cart_count=count)
    return dict(cart_count=0)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Create admin if not exists
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', password=generate_password_hash('admin', method='pbkdf2:sha256'), is_admin=True)
            db.session.add(admin)
            db.session.commit()
            
    app.run(debug=True)
