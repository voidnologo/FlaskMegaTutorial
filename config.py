import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'my_secret_key')
