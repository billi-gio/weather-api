# weather-api  !!! REPLACE ME WITH AN ACTUAL README !!!


# Requirements
You should have a development environment set up with:

* poetry
* Docker 

# Install
```bash
poetry env use 3.11                                   # only if you want to use a specific version

export PYPI_USERNAME=oauth2accesstoken # only needed for building in the docker locally
export PYPI_PASSWORD=$(gcloud auth print-access-token)  # https://revolut.atlassian.net/wiki/spaces/BD/pages/2549849529/Python+GCP+Artifact+Registry for instructions

poetry install
```

Don't forget check into repo the `poetry.lock` file.

# Testing
Sets of test are defined:

- `tests/unit` unit tests
- `tests/functional` functional tests (with dependencies on things like db, etc.)

# Convenience scripts
The Makefile in this project contains convenience scripts to help your day-to-day coding. See below:

Start the app inside docker:
```bash
make start
```

Start the app outside the docker:
```bash
python weather_api/app.py
```

To run app outside the docker you need to modify DB network in docker-compose to match the app config.

We do not recommend running the application inside in the docker container. 
There is no much benefit (All devs use macbooks, we don't use binary dependencies, all app runs in GKE). 
The problems are: flaky build and caching, higher CPU usage when watching the files and problem with debugging (you have to use remote debugger).

Formatting and verification (`revolut-lint`):
```bash
make fmt verify
```

Run tests:
```bash
make tests
```

**Check current migration:**

If you run your app inside the docker locally, you need to execute then in the container.
```bash
make db-migration-state
```

Migrate the database to `latest` revision:
```bash
make db-up
```

Migrate the database to base revision:
```bash
make db-down
```

Review migration history
```bash
make db-migration-history
```

