.PHONY: fmt style verify test
fmt:
	isort .
	black .

check:
	mypy -p weather_api
	pylint weather_api --rcfile=.pylintrc

style:
	isort --check --diff .
	black --check --diff .
	mypy -p weather_api
	pylint weather_api --rcfile=.pylintrc --fail-under=8.5

verify: style test

start:
	python weather_api/app.py

test:
	pytest tests/
