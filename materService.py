from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

app = Flask(__name__)
app.secret_key = "your_secret_key"  
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:asdfgh@192.168.3.188/blank_2103'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    address = db.Column(db.String(200))

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/admin', methods=['POST'])
def admin():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter(func.lower(User.username) == func.lower(username)).first()
    if user and user.password == password:
        session['username'] = username  
        return render_template('home.html')
    else:
        return redirect(url_for('login'))
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/customer/list')
def customer_list():
    customers = Customer.query.all()
    return render_template('blank.html', customers=customers)


@app.route('/list', methods=['POST'])
def list():
    dct_request = request.json
    if dct_request['type'] == 'customer':
        customers = Customer.query.all()
        return render_template('customer_list.html', customers=customers)
    elif dct_request['type'] == 'invoice':
        invoices = Invoice.query.all()
        return render_template('invoice_list.html', invoices=invoices)
    
    
@app.route('/create', methods=['POST'])
def create_data():
    import pdb;pdb.set_trace()
    dct_request = request.json
    if dct_request['type'] == 'customer':
        customers = Customer.query.all()
        return render_template('customer_list.html', customers=customers)
    elif dct_request['type'] == 'invoice':
        invoices = Invoice.query.all()
        return render_template('invoice_list.html', invoices=invoices)
    

@app.route('/customer/create', methods=['GET', 'POST'])
def create_customer():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        new_customer = Customer(name=name, phone=phone, email=email, address=address)
        db.session.add(new_customer)
        db.session.commit()
        return redirect(url_for('customer_list'))
    return render_template('customer_create.html')

@app.route('/customer/edit/<int:customer_id>', methods=['GET', 'POST'])
def edit_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    if request.method == 'POST':
        customer.name = request.form['name']
        customer.phone = request.form['phone']
        customer.email = request.form['email']
        customer.address = request.form['address']
        db.session.commit()
        return redirect(url_for('customer_list'))
    return render_template('customer_edit.html', customer=customer)

@app.route('/invoice/edit/<int:invoice_id>', methods=['GET', 'POST'])
def edit_invoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    if request.method == 'POST':
        invoice.customer_id = request.form['customer_id']
        invoice.date = request.form['date']
        invoice.amount = request.form['amount']
        invoice.status = request.form['status']
        db.session.commit()
        return redirect(url_for('invoice_list'))
    customers = Customer.query.all()
    return render_template('invoice_edit.html', invoice=invoice, customers=customers)


@app.route('/invoice/list')
def invoice_list():
    invoices = Invoice.query.all()
    return render_template('blank2.html', invoices=invoices)

@app.route('/invoice/create', methods=['GET', 'POST'])
def create_invoice():
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        date = request.form['date']
        amount = request.form['amount']
        status = request.form['status']
        new_invoice = Invoice(customer_id=customer_id, date=date, amount=amount, status=status)
        db.session.add(new_invoice)
        db.session.commit()
        return redirect(url_for('invoice_list'))
    customers = Customer.query.all()
    return render_template('invoice_create.html', customers=customers)

@app.route('/logout')
def logout():
    session.pop('username', None) 
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=60000, debug=True)
