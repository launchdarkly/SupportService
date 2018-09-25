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
        'psycopg2-binary',
        'ldclient-py',
        'gunicorn'
    ]
)