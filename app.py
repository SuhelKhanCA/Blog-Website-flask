from flask import Flask, render_template, request, json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

local_server = True
with open('config.json', 'r') as c:
    params = json.load(c)["params"]
app = Flask(__name__)
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']
    
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12))
    
    def __repr__(self):
        return self.name


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        entry = Contacts(name=name, phone_num=phone, date=datetime.now(), msg=message, email=email)
        db.session.add(entry)
        db.session.commit()
      
    return render_template('contact.html')

@app.route("/post")
def post():
    return render_template('post.html')

@app.route("/contacts")
def view_contacts():
    all_contacts = Contacts.query.all()
    return render_template('contacts.html', contacts=all_contacts)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)