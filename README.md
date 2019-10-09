# SupportService

[![CircleCI](https://circleci.com/gh/launchdarkly/SupportService.svg?style=shield)](https://circleci.com/gh/launchdarkly/SupportService)

SupportService is a simple application built in flask, that can be used to
demonstrate the use of feature flags in action. All of the source code can be
downloaded from GitHub and run locally your machine. The following are
instructions on how to install the application and how to configure it so you
can run the demo environment on your local machine.

Please refer to the [wiki](https://github.com/launchdarkly/SupportService/wiki)
for more information on specific feature flags and use cases.

## Installation

### Initial setup

- Clone the repo locally `git clone https://github.com/launchdarkly/SupportService.git`
- Copy `.env.example` to `.env` and fill in the correct values, without quotes:

        LD_CLIENT_KEY=$YOUR_SDK_KEY
        LD_FRONTEND_KEY=$YOUR_FRONTEND_ID
        LD_API_KEY=$YOUR_LD_API_KEY (obtained from <https://app.launchdarkly.com/settings/authorization>)
        DD_API_KEY=$DATADOG_API_KEY (use the dev API key in the .env.example file)

### Option 1: Run in Docker

- Ensure that you have [Docker](https://docs.docker.com/install/) installed
- Run `docker-compose up --build`

### Option 2: Run locally in a virtualenv

- Ensure that you have [`python3`](https://www.python.org/downloads/) and
  [PostgreSQL](https://www.postgresql.org/download/) installed
- Run `make dev` to create a virtualenv and install all dependencies.
- Run `make run` to start the application

### Logging in

The app should now be running on [your-LD-env.localhost:5000](http://<YOUR-LD-ENV>.localhost:5000). You should be able to log
in with the username `test@tester.com` and password `test`. Alternatively,
register a new user - it won't send you any email.

## Contributing

### Git Commits

Each commit should be a coherent whole that implements one idea completely and
correctly. No commit should ever break the code, even if another commit "fixes
it" later.

Good commit messages make this project easier to maintain, and unlock the power
of tools like `git revert`, `log`, and `blame`.

A good commit message:

- Has a subject line that summarizes the change.
- Uses the imperative mood in the subject line. It should fit the form "If
  applied, this commit will ".
- Provides context on what and why (instead of how) in the body.
- Uses the form `<Area>: <Title>` in the subject line. The title should be
  capitalized, but not end with a period.
- Limits the subject line to 50 characters.
- Wraps the body at 72 characters.

See
[https://chris.beams.io/posts/git-commit/](https://chris.beams.io/posts/git-commit/)
for more information.

## Running in Production

**Note: this section only applies to LaunchDarkly employees.**

There is a production instance of this application running for every environment
that is defined in the `support-service` project in our demo environment.

If you need your own environment simply make a new environment inside of this
project. This will trigger a deployment via CircleCI that will provision a new
instance on AWS Lightsail.

After a few minutes will be available at
`$YOUR_ENVIRONMENT_KEY.ldsolutions.org`.

### Updating in Production

Every time that there is a commit to the master branch of this repo, a
deployment runs via CircleCI to update all existing instances on AWS LightSail
to the latest version of master.

## Simulator

There is a selenium based "simulator" that lives under the `webdriver`
directory. This is used to provide a steady stream of activities against all
current demo sites so that the insights graphs for various feature flags are
populated.

Right now it runs every hour via a CircleCI job. You can see the use pattern in
the `.circle/config.yml` file under the `simulate` job.

### Running it Locally

1. Go to the webdriver directory: `cd tests/webdriver`
2. Compile the maven project: `mvn compile assembly:single`
3. Start the simulator with: `java -jar target/webdriver-1.0-SNAPSHOT-jar-with-dependencies.jar`
