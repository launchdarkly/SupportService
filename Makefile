.PHONY: help docs run test

help:
	@echo "This project assumes an active Python virtualev is present."
	@echo "The following Make targets are available:"
	@echo "		help		display this help and exit"
	@echo "		docs		create pydocs for all relevant modules"
	@echo "		run		run the flask application
	@echo "		test		run all tests with coverage"

docs:
	./scripts/make_docs

dev:
	./scripts/make_dev.sh

deploy:
	export FLASK_APP=run.py && \
	flask deploy
	
run:
	export FLASK_APP=run.py && \
	export FLASK_DEBUG=true && \
	flask db upgrade && \
	flask run --host=0.0.0.0

test:
	set -e && coverage run tests/main.py

update:
	zip -g LdLambda.zip LdLambda.py && \
	scripts/update_lambda.sh