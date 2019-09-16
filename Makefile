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

run:
	export FLASK_APP="app.factory:create_app()" && \
	export FLASK_DEBUG=true && \
	export FLASK_ENV=development && \
	flask run --host=0.0.0.0

test:
	set -e && coverage run tests/main.py

generate:
	export FLASK_APP="app.factory:create_app('production')" && \
	flask generate

generate-staging:
	export FLASK_APP="app.factory:create_app('staging')" && \
	flask generate
