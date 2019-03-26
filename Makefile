.PHONY: help docs run test

help:
	@echo "This project assumes an active Python virtualev is present."
	@echo "The following Make targets are available:"
	@echo "		help		display this help and exit"
	@echo "		dev		create or update a dev environment"
	@echo "		run		run the flask application"
	@echo "		test		run all tests with coverage"
	@echo "		deploy		deploy application to LightSail"

dev:
	if [ ! -d "venv" ]; then python3 -m venv venv; fi
	bash -c "source venv/bin/activate"
	pip install -r dev-requirements.txt
	pip install -e .

run:
	export FLASK_APP="app.factory:create_app()" && \
	export FLASK_DEBUG=true && \
	flask db upgrade && \
	flask run --host=0.0.0.0

test:
	set -e && coverage run tests/main.py

deploy:
	export FLASK_APP="app.factory:create_app('production')" && \
	flask generate && \
	./scripts/deploy.sh
