# SupportService

SupportService is a simple application built in flask, that can be used to demonstrate the use of feature flags in action. All of the source code can be downloaded from github and run locally your machine. The following are instructions on how to install the application and how to configure it so you can run the demo environment on your local machinge. As of now, there are 2 primary feature flags that can be used to show functionality on the site.

## Installation 

### Requirements 

* Python 3 
* The `virtualenv` package (`pip install virtualenv`)
* PostgreSQL Database called 'supportService'

### Instructions 

* Clone the repo locally `git clone https://github.com/manuelPartida/SupportService.git`
* Create a python virtual environment `virtualenv -p python3 venv`
* Activate the virtual environment `source venv/bin/activate`
* Copy `.env.example` to `.env` and fill in the correct values
    * `export DATABASE_URL='postgresql://localhost/supportService'`
    * `export LD_CLIENT_KEY=$YOUR_SDK_KEY`
* Source the environment variables `source .env`
* Upgrade database to latest version `flask db upgrade`
* Start the app with `flask run`

The app should now be running on localhost:5000 