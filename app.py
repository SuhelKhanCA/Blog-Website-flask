from flask import redirect, render_template, request, url_for
from datetime import datetime

# Import from Config.py
from config import db
from config import app
from config import params
from config import mail

# Database import db.py
from db import Posts
from db import Contacts


@app.route("/")
def home():
    '''
    This is the home/index route for Home page of 
    blogs that shows some of blogs with pagiantion.
    '''

    posts = Posts.query.filter_by().all()[0:params['no_of_posts']]
    return render_template('index.html', params=params, posts=posts)

@app.route("/posts")
def posts():
    '''
    This routes show brief of all the posts
    '''

    posts = Posts.query.filter_by().all()
    return render_template('posts.html', params=params, posts=posts)


@app.route("/post/<string:post_slug>", methods=['GET'])
def post(post_slug):
    '''
    This routes take a slug and fetch a particular post
    '''

    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html', params=params, post=post)

@app.route("/about")
def about():
    '''
    This page is suppose to create an
    '''
    return render_template('about.html', params=params)


@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    '''
    This route saves the contacts information from contacts page and save it to database. The new is to implement for SMTP server.
    '''

    if(request.method=='POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contacts(name=name, phone_num = phone, msg = message, date= datetime.now(),email = email )
        db.session.add(entry)
        db.session.commit()

        '''The below code show some Auth Error'''
        # mail.send_message('New message from ' + name,
        #                   sender=email,
        #                   recipients = [params['gmail_username']],
        #                   body = message + "\n" + phone
        #                   )

    return render_template('contact.html', params=params)

@app.route("/dashboard", methods = ['GET', 'POST'])
def dashboard():
    '''
    This is Admin -  Need to be built
    '''
    posts = Posts.query.all()[0: params['no_of_posts']]
  
    if request.method=='POST':
        #Redirect to Admin panel
        email = request.form.get('email')
        password = request.form.get('password')

        if password == params['admin_password'] and email == params['admin_email']:
            return render_template('dashboard.html', params=params, posts=posts)
    else:
        return render_template('login.html', params=params)

@app.route('/create_post', methods=['POST', 'GET'])
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_post = Posts(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()
        
        return redirect(url_for('dashboard'))
    return render_template('create_post.html')

if __name__ == "__main__":
    app.run(debug=True)

