# SupportService

[![CircleCI](https://circleci.com/gh/launchdarkly/SupportService.svg?style=shield)](https://circleci.com/gh/launchdarkly/SupportService)

SupportService is a simple application built in flask, that can be used to demonstrate the use of feature flags in action. All of the source code can be downloaded from github and run locally your machine. The following are instructions on how to install the application and how to configure it so you can run the demo environment on your local machinge.

Please refer to the [wiki](https://github.com/launchdarkly/SupportService/wiki) for
more information on specific feature flags and use cases.

## Installation

### Requirements

* Python 3
* pip

### Instructions

* Clone the repo locally `git clone https://github.com/launchdarkly/SupportService.git`
* Copy `.env.example` to `.env` and fill in the correct values:

        export LD_CLIENT_KEY=$YOUR_SDK_KEY
        export LD_FRONTEND_KEY=$YOUR_FRONTEND_ID

* Run `make dev` to create a virtualenv and install all dependencies.
* Run `make run` to start the application

The app should now be running on [localhost:5000](http://localhost:5000). You
should be able to log in with the username `test@tester.com` and password `test`.


## Running in Production

**Note: this section only applies to LaunchDarkly employees.**

There is a production instance of this application running for every
environment that is defined in the `support-service` project in our demo
environment.

If you need your own environment simply make a new environment inside of this
project. This will trigger a deployment via CircleCI that will provision a
new instance on AWS Lightsail.

After a few minutes will be available at `$YOUR_ENVIRONMENT_KEY.ldsolutions.org`.

### Updating in Production

Every time that there is a commit to the master branch of this repo, a deployment
runs via CircleCI to update all existing instances on AWS LightSail to the latest
version of master.

## Simulator
There is a selenium based "simulator" that lives under the `webdriver` directory.
This is used to provide a steady stream of activities against all current demo
sites so that the insights graphs for various feature flags are populated.

Right now it runs every hour via a CircleCI job. You can see the use pattern in
the `.circle/config.yml` file under the `simulate` job.

### Running it Locally

1. Go to the webdriver directory: `cd tests/webdriver`
2. Compile the maven project: `mvn compile assembly:single`
3. Start the simulator with: `java -jar target/webdriver-1.0-SNAPSHOT-jar-with-dependencies.jar`
