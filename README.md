# Cars API (FastApi)

[![Maintainability](https://api.codeclimate.com/v1/badges/c5b1881834bfb4edd645/maintainability)](https://codeclimate.com/github/sergkim13/cargo-cars-API/maintainability)
[![Linters check](https://github.com/sergkim13/cargo-cars-API/actions/workflows/linters_check.yml/badge.svg)](https://github.com/sergkim13/cargo-cars-API/actions/workflows/linters_check.yml)
[![Test Coverage](https://api.codeclimate.com/v1/badges/c5b1881834bfb4edd645/test_coverage)](https://codeclimate.com/github/sergkim13/cargo-cars-API/test_coverage)

### Description:
Cars API allows you to get information about cargos. See docs at http://0.0.0.0:8000/docs after starting app.
Made with:
- FastAPI,
- PostgreSQL,
- SQLAlchemy 2.0,
- Pydantic,
- Alembic,
- Docker,
- Redis.

### Requirements:
1. MacOS (prefer) / Linux / Windows10
2. `Docker`
3. `Make` utily for MacOS, Linux.

### Install:
1. Clone repository: https://github.com/sergkim13/cargo-cars-API
2. Create `.env` and fill it up according to `.env.example`.
3. Type `make compose` for running application in docker container. App will be running at http://0.0.0.0:8000. Type `make stop` to stop app container.
4. Type `make compose-test` for running tests in docker container. Type `make stop-test` to stop app container.
5. For checking `pre-commit hooks` you need `Poetry` and install dependencies:
    - `make install` to install dependencies to your virtual environment.
    - `make hooks`
