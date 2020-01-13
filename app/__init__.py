import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from config import Config


app = Flask(__name__)
app.config.from_object(Config)

# db
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# login
login = LoginManager(app)
login.login_view = 'login'

# mail
mail = Mail(app)
# python -m smtpd -n -c DebuggingServer localhost:8025
# export MAIL_SERVER=localhost
# export MAIL_PORT=8025
# --- or use gmail
# export MAIL_SERVER=smtp.googlemail.com
# export MAIL_PORT=587
# export MAIL_USE_TLS=1
# export MAIL_USERNAME=<your-gmail-username>
# export MAIL_PASSWORD=<your-gmail-password>

# css/js
bootstrap = Bootstrap(app)

# time
moment = Moment(app)


def email_logger():
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr=f'no-reply@{app.config["MAIL_SERVER"]}',
            toaddrs=app.config['ADMINS'],
            subject='Microblog Failure',
            credentials=auth,
            secure=secure,
        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


def file_logger():
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(
        logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:(lineno)d]'
        )
    )
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)


if not app.debug:
    # email ERROR level issues
    email_logger()
    # file logger for INFO+ issues
    file_logger()

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')


from app import routes, models, errors
