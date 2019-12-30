from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Salt'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Chattanooga.',
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The movie was so cool!',
        },
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)
