from functools import wraps
from flask import redirect, render_template, request, url_for, session, flash
from datetime import datetime
from werkzeug.utils import secure_filename

# Import from Config.py
from config import db
from config import app
from config import params

# Database import db.py
from db import Posts
from db import Contacts
import os


def login_required(f):
    """
    Decorator to ensure that the user is logged in.

    Args:
        f (function): The function to be decorated.

    Returns:
        function: The decorated function.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user or admin is logged in
        if 'user' not in session:
            flash("You need to log in to access this page.", "warning")
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def home():
    """
    Home route for the blog website. Displays a list of blog posts with pagination.

    Returns:
        str: Rendered HTML template for the home page.
    """
    posts = Posts.query.filter_by().all()[0:params['no_of_posts']]
    return render_template('index.html', params=params, posts=posts)

@app.route("/posts")
def posts():
    """
    Route to display a brief overview of all blog posts.

    Returns:
        str: Rendered HTML template for the posts page.
    """
    posts = Posts.query.filter_by().all()
    return render_template('posts.html', params=params, posts=posts)

@app.route("/post/<string:post_slug>", methods=['GET'])
def post(post_slug):
    """
    Route to display a specific blog post based on its slug.

    Args:
        post_slug (str): The slug of the post to be displayed.

    Returns:
        str: Rendered HTML template for the specific post.
    """
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html', params=params, post=post)

@app.route("/about")
def about():
    """
    Route to display the about page.

    Returns:
        str: Rendered HTML template for the about page.
    """
    return render_template('about.html', params=params)

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    """
    Route to handle contact form submissions and display the contact page.

    Returns:
        str: Rendered HTML template for the contact page.
    """
    if request.method == 'POST':
        flash("Thanks for contacting us! We'll get back to you soon!", "success")
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contacts(name=name, phone_num=phone, msg=message, date=datetime.now(), email=email)
        db.session.add(entry)
        db.session.commit()
    return render_template('contact.html', params=params)

@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    """
    Route to display the admin dashboard and handle login form submissions.

    Returns:
        str: Rendered HTML template for the dashboard or login page.
    """
    posts = Posts.query.all()
    # Convert date strings to datetime objects
    for post in posts:
        post.date = datetime.strptime(post.date, '%Y-%m-%d %H:%M:%S.%f')
    if 'user' in session and session['user'] == params['admin_email']:
        return render_template('dashboard.html', params=params, posts=posts)
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if password == params['admin_password'] and email == params['admin_email']:
            session['user'] = email
            flash("Login successful!", "success")
            return render_template('dashboard.html', params=params, posts=posts)
        else:
            flash("Please enter correct email and password", "danger")
    return render_template('login.html', params=params)

@login_required
@app.route('/create_post', methods=['POST', 'GET'])
def create_post():
    """
    Route to create a new blog post.

    Returns:
        str: Rendered HTML template for the create post page.
    """
    if request.method == 'POST':
        title = request.form['title']
        tline = request.form['tline']
        slug = request.form['slug']
        content = request.form['content']
        p_img = request.form['img']

        new_post = Posts(title=title, content=content, slug=slug, tagline=tline, date=datetime.now(), img_file=p_img)
        db.session.add(new_post)
        db.session.commit()
        
        return redirect(url_for('dashboard'))
    return render_template('create_post.html', params=params)

@login_required
@app.route('/edit/<string:sno>', methods=['POST', 'GET'])
def edit(sno):
    """
    Route to edit an existing blog post.

    Args:
        sno (str): The serial number of the post to be edited.

    Returns:
        str: Rendered HTML template for the edit post page.
    """
    post = Posts.query.filter_by(sno=sno).first()
    if request.method == 'POST':
        title = request.form['title']
        tline = request.form['tline']
        slug = request.form['slug']
        content = request.form['content']
        p_img = request.form['img']

        post.title = title
        post.slug = slug
        post.tagline = tline
        post.content = content
        post.date = datetime.now()
        post.img_file = p_img

        db.session.commit()
        flash("Post is edited successfully", "success")
        return redirect(url_for('dashboard'))
    return render_template('edit.html', params=params, sno=sno, post=post)

@app.route('/delete/<string:sno>')
def delete(sno):
    """
    Route to delete a blog post.

    Args:
        sno (str): The serial number of the post to be deleted.

    Returns:
        str: Redirect to the dashboard page.
    """
    flash('Post deleted!', 'warning')
    Posts.query.filter_by(sno=sno).delete()
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route("/get_contacts")
def get_contacts():
    """
    Route to display all contacts.

    Returns:
        str: Rendered HTML template for the contacts page.
    """
    if 'user' in session and session['user'] == params['admin_email']:
        contacts = Contacts.query.all()
        # Convert date strings to datetime objects
        for contact in contacts:
            contact.date = datetime.strptime(contact.date, '%Y-%m-%d %H:%M:%S.%f')
        return render_template("get_contacts.html", contacts=contacts, params=params)
    return redirect(url_for('dashboard'))

@app.route('/uploader', methods=['GET', 'POST'])
def upload_img():
    """
    Route to handle image uploads.

    Returns:
        str: Success message after uploading the image.
    """
    if 'user' in session and session['user'] == params['admin_email']:
        if request.method == 'POST':
            f = request.files['img_file']  # Corrected access to request.files
            f.save(os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(f.filename)))
            flash("Uploaded successfully", "success")
            return redirect(url_for('dashboard'))
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    """
    Route to log out the user and clear the session.

    Returns:
        str: Rendered HTML template for the login page.
    """
    session.clear()
    flash('You have been logged out successfully!', 'success')
    return render_template('login.html', params=params)

if __name__ == "__main__":
    app.run(debug=True)

