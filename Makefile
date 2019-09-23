.PHONY: help docs run test

help:
	@echo "This project assumes an active Python virtualev is present."
	@echo "The following Make targets are available:"
	@echo "		help		display this help and exit"
	@echo "		dev		create or update a dev environment"
	@echo "		run		run the flask application"
	@echo "		test		run all tests with coverage"
	@echo "		generate	generate production config files"

dev:
	if [ ! -d "venv" ]; then python3 -m venv venv; fi
	bash -c "source venv/bin/activate"
	pip3 install -r dev-requirements.txt
	pip3 install -e .

# Not using flask run due to socket error for local debugging and reloading
# https://stackoverflow.com/questions/53522052/flask-app-valueerror-signal-only-works-in-main-thread
run:
	export FLASK_APP="app.factory:SubdomainDispatcher('localhost','default')" &&\
	export FLASK_DEBUG=true && \
	export FLASK_ENV=development && \
	python3 app/factory.py --host=localhost

test:
	set -e && TESTING=true coverage run tests/main.py

generate:
	j2 app/cli/templates/docker-compose.prod.jinja > docker-compose.prod.yml

.PHONY: dev-container
dev-container:
	docker build -f Dockerfile.dev -t supportservice:latest .
