# weather-api
Get weather forecast and save results to the database

## Requirements
You should have a development environment set up with:

* poetry
* python3.11

## Install
```bash
poetry env use 3.11                                   # only if you want to use a specific version
poetry install
```

Don't forget check into repo the `poetry.lock` file.

## Testing
Sets of test are defined:

- `tests/unit` unit tests
- `tests/functional` functional tests (with dependencies on things like db, etc.)

## Convenience scripts
The Makefile in this project contains convenience scripts to help your day-to-day coding. See below:

Start the app:
```bash
make start
```
or
```bash
python weather_api/app.py
```

```bash
make fmt verify
```

Run tests:
```bash
make tests
```