# Blog Website using Flask

A simple blog website built with Flask. This project includes features for displaying blog posts, handling user contact submissions, and sending email notifications via Gmail's SMTP server.

**NOTE** : Planning to use this blog website as my upcoming tech blogs.

## Table of Contents

- [Blog Website using Flask](#blog-website-using-flask)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Technologies Used](#technologies-used)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Usage](#usage)
  - [Project Structure](#project-structure)
  - [Routes](#routes)
  - [Screenshots](#screenshots)
    - [Home Page](#home-page)
    - [About Page](#about-page)
    - [Contact Page](#contact-page)
    - [Post Page](#post-page)
    - [Admin Dashboard](#admin-dashboard)
    - [Contacts View](#contacts-view)
  - [Contributing](#contributing)
  - [License](#license)
  - [Acknowledgements](#acknowledgements)

## Features

- **Home Page**: Displays the main content of the blog.
- **About Page**: Provides information about the blog.
- **Contact Page**: Allows users to submit their contact details and message. On submission, the contact information is saved in the database and an email notification is sent.
- **Post Page**: Displays individual blog posts.
- **Contacts View**: Admin view to list all contact submissions.

## Technologies Used

- **Backend**: [Flask](https://flask.palletsprojects.com/), [Flask-Mail](https://pythonhosted.org/Flask-Mail/), [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
- **Database**: SQLite (configured via SQLAlchemy)
- **Frontend**: HTML, CSS
- **Other**: JSON configuration, Gmail SMTP for sending emails

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/SuhelKhanCA/Blog-Website-flask.git
   cd Blog-Website-flask
   ```

2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

## Configuration

1. **Create the Configuration File**

In the root directory, create a file named config.json with the following structure:

```json
{
  "params": {
    "gmail_username": "your-email@gmail.com",
    "gmail_password": "your-email-password",
    "local_uri": "sqlite:///your-local-database.db",
    "prod_uri": "your-production-database-uri"
  }
}
```

**_Replace the placeholder values with your actual Gmail credentials and database URIs._**

2. **Initialize the Database**

- Open a Python shell and execute:

```python
from app import db
db.create_all()
```

- This command creates the necessary tables (e.g., the Contacts table) in your database.

## Usage

- **Home Page**: Visit `http://127.0.0.1:5000/` to view the homepage.
- **About Page**: Visit `http://127.0.0.1:5000/about` for information about the blog.
- **Contact Page**: Visit `http://127.0.0.1:5000/contact` to submit your contact details and message.
- **Post Page**: Visit `http://127.0.0.1:5000/post` to view a blog post.
- **Contacts View**: Visit `http://127.0.0.1:5000/contacts` to see all submitted contacts (typically for administrative purposes).

## Project Structure

```text
Blog-Website-flask/
├── .idea/                # IDE configuration files (if applicable)
├── __pycache__/          # Cached Python files
├── instance/             # Instance folder for configurations (if used)
├── static/               # Static files (CSS, JavaScript, images)
├── templates/            # HTML templates
│   ├── index.html        # Home page template
│   ├── about.html        # About page template
│   ├── contact.html      # Contact page template
│   ├── post.html         # Blog post template
│   ├── dashboard.html    # Admin dashboard template
│   ├── get_contacts.html # Contacts listing template
│   └── login.html        # Login page template
├── .gitignore            # Specifies files to ignore in Git
├── app.py                # Main Flask application file
├── config.json           # Configuration file (create this file as shown above)
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

## Routes

- `/`: Home page (renders `index.html`)
- `/about`: About page (renders `about.html`)
- `/contact`: Contact page (handles GET and POST requests)
  - On POST, it saves the submitted contact information into the database and sends an email notification.
- `/post/<string:post_slug>`: Displays a blog post (renders `post.html`)
- `/dashboard`: Admin dashboard (renders `dashboard.html`)
- `/create_post`: Create a new blog post (renders `create_post.html`)
- `/edit/<string:sno>`: Edit an existing blog post (renders `edit.html`)
- `/delete/<string:sno>`: Delete a blog post
- `/get_contacts`: Lists all contact submissions (renders `get_contacts.html`)
- `/uploader`: Handles image uploads
- `/logout`: Logs out the user

## Screenshots

Here are some screenshots of the running website:

### Home Page

![Home Page](snapshot/home1.png)
![Home Page](snapshot/home2.png)

### About Page

![About Page](snapshot/about1.png)
![About Page](snapshot/about2.png)

### Contact Page

![Contact Page](snapshot/conatctme.png)
![Contact Page](snapshot/conatctme2.png)

### Post Page

![Post Page](snapshot/posts.png)

### Admin Dashboard

![Admin Dashboard](snapshot/dashboard.png)

### Contacts View

![Contacts View](snapshot/getcon.png)

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request with any improvements or bug fixes. For major changes, consider opening an issue first to discuss your proposed changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements

- Bootstrap
- Flask Documentation
- Flask-Mail Documentation
- Flask-SQLAlchemy Documentation
