# SupportService

SupportService is a simple application built in flask, that can be used to demonstrate the use of feature flags in action. All of the source code can be downloaded from github and run locally your machine. The following are instructions on how to install the application and how to configure it so you can run the demo environment on your local machinge. 

Please refer to the [wiki](https://github.com/launchdarkly/SupportService/wiki) for 
more information on specific feature flags and use cases. 

## Installation 

### Requirements 

* [Docker](https://www.docker.com/)
* [docker-compose](https://docs.docker.com/compose/)

### Instructions 

* Clone the repo locally `git clone https://github.com/manuelPartida/SupportService.git`
* Copy `.env.example` to `.env` and fill in the correct values
    ```
    export DATABASE_URL=postgresql://supportService:supportService@db/supportService
    export LD_CLIENT_KEY=$YOUR_SDK_KEY
    export LD_FRONTEND_KEY=$YOUR_FRONTEND_ID
    ```
* Source the environment variables `source .env`
* Start up the stack with `docker-compose up`

The app should now be running on localhost:5000 

## Running in Production 

**Note: this section only applies to LaunchDarkly employees.**

There is a production instance of this application running for every 
environment that is defined in the `support-service` project in our demo 
environment.

If you need your own environment simply make a new environment inside of this 
project. This will trigger a deployment via CircleCI that will provision a 
new instance on AWS Lightsail. 

After a few minutes will be available at `$YOUR_ENVIRONMENT_KEY.ldsolutions.tk`.

### Updating in Production 

Every time that there is a commit to the master branch of this repo, a deployment 
runs via CircleCI to update all existing instances on AWS LightSail to the latest
version of master.