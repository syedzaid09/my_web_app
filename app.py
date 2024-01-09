from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

def user_login(username, password):
    # You can replace this with your actual user validation logic
    return True

def vendor_login(username, password):
    # You can replace this with your actual vendor validation logic
    return True

def admin_login(username, password):
    # You can replace this with your actual admin validation logic
    return True

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return "Registration successful!"
    return render_template('register.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        choice = request.form.get('choice')
        username = request.form.get('username')
        password = request.form.get('password')

        if choice == '1' and user_login(username, password):
            return f"Welcome, {username} (User)"
        elif choice == '2' and vendor_login(username, password):
            return f"Welcome, {username} (Vendor)"
        elif choice == '3' and admin_login(username, password):
            return f"Welcome, {username} (Admin)"
        else:
            return "Invalid credentials."

    return render_template('index.html')

@app.route('/dashboard/<username>')
def dashboard(username):
    user = users.get(username)
    if user:
        return render_template('dashboard.html', username=username)
    else:
        return "User not found", 404
    
@app.route('/products')
def products():
    sample_products = ['Product A', 'Product B', 'Product C']
    return render_template('products.html', products=sample_products)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # SQLite database
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def _repr_(self):
        return f"User('{self.username}')"

# Create the database
db.create_all()

@app.route('/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == "_main_":
    app.run(debug=True)
