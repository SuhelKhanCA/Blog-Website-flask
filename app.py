from flask import Flask, render_template_string, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
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

templates = {
    'index': '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Home</title>
        </head>
        <body>
            <h1>Welcome to the Home Page</h1>
            <nav>
                <a href="/">Home</a> |
                <a href="/about">About</a> |
                <a href="/contact">Contact</a> |
                <a href="/post">Post</a> |
                <a href="/contacts">View Contacts</a>
            </nav>
        </body>
        </html>
    ''',
    'about': '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>About</title>
        </head>
        <body>
            <h1>About Us</h1>
            <nav>
                <a href="/">Home</a> |
                <a href="/about">About</a> |
                <a href="/contact">Contact</a> |
                <a href="/post">Post</a> |
                <a href="/contacts">View Contacts</a>
            </nav>
        </body>
        </html>
    ''',
    'contact': '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Contact</title>
        </head>
        <body>
            <h1>Contact Us</h1>
            <form method="POST" action="/contact">
                <label for="name">Name:</label><br>
                <input type="text" id="name" name="name" required><br>
                <label for="email">Email:</label><br>
                <input type="email" id="email" name="email" required><br>
                <label for="phone">Phone:</label><br>
                <input type="text" id="phone" name="phone" required><br>
                <label for="message">Message:</label><br>
                <textarea id="message" name="message" required></textarea><br>
                <input type="submit" value="Submit">
            </form>
            <nav>
                <a href="/">Home</a> |
                <a href="/about">About</a> |
                <a href="/contact">Contact</a> |
                <a href="/post">Post</a> |
                <a href="/contacts">View Contacts</a>
            </nav>
        </body>
        </html>
    ''',
    'post': '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Post</title>
        </head>
        <body>
            <h1>Post Page</h1>
            <nav>
                <a href="/">Home</a> |
                <a href="/about">About</a> |
                <a href="/contact">Contact</a> |
                <a href="/post">Post</a> |
                <a href="/contacts">View Contacts</a>
            </nav>
        </body>
        </html>
    ''',
    'contacts': '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Contact Submissions</title>
        </head>
        <body>
            <h1>Contact Submissions</h1>
            <table border="1">
                <tr>
                    <th>S.No</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Phone</th>
                    <th>Message</th>
                </tr>
                {% for contact in contacts %}
                <tr>
                    <td>{{ contact.sno }}</td>
                    <td>{{ contact.name }}</td>
                    <td>{{ contact.email }}</td>
                    <td>{{ contact.phone_num }}</td>
                    <td>{{ contact.msg }}</td>
                </tr>
                {% endfor %}
            </table>
            <nav>
                <a href="/">Home</a> |
                <a href="/about">About</a> |
                <a href="/contact">Contact</a> |
                <a href="/post">Post</a> |
                <a href="/contacts">View Contacts</a>
            </nav>
        </body>
        </html>
    '''
}

@app.route("/")
def home():
    return render_template_string(templates['index'])


@app.route("/about")
def about():
    return render_template_string(templates['about'])


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        entry = Contacts(name=name, phone_num=phone, msg=message, email=email)
        db.session.add(entry)
        db.session.commit()
      
    return render_template_string(templates['contact'])

@app.route("/post")
def post():
    return render_template_string(templates['post'])

@app.route("/contacts")
def view_contacts():
    all_contacts = Contacts.query.all()
    return render_template_string(templates['contacts'], contacts=all_contacts)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)