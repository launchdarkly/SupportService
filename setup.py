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
        'psycopg2-binary',
        'redis',
        'ldclient-py',
        'gunicorn',
        'boto3',
        'circleci',
        'faker'
    ]
)