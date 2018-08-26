import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    VERSION = '1.0.2'
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess-this'
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') 
    #SQLALCHEMY_DATABASE_URI = 'sqlite://' + os.path.join(basedir,'data.sqlite') 
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')


