from setuptools import setup, find_packages

setup(
    name='SupportService',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-sqlalchemy',
        'flask-migrate',
        'flask-login',
        'flask-bootstrap',
        'flask-wtf',
        'flask-caching',
        'flask-fixtures',
        'psycopg2',
        'redis',
        'ldclient-py',
        'gunicorn',
        'boto3',
        'circleci==1.1.3',
        'faker',
        'click',
        'click-log'
    ]
)