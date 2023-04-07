# Page Analyzer
[![Actions Status](https://github.com/round-cube/python-project-83/workflows/hexlet-check/badge.svg)](https://github.com/round-cube/python-project-83/actions)

🚀 Live Demo: https://python-project-83-production-bf73.up.railway.app/


## Screenshots

![Demo] (screenshots/out.gif)


## Requirements

- CPython: 3.11
- Docker (optional)


## Development setup

1. Clone repository via `git clone https://github.com/round-cube/python-project-83` and `cd` into new directory.
2. Run `make install` to install all required dependencies.
3. (*optional*) Start postgres via Docker with `make run-db`.
4. Set following environment variables:
- `DATABASE_URL`: `postgresql://janedoe:mypassword@localhost:5432/mydb` (or URL of running Postgres instance)
- `SECRET_KEY`: random secret key (could be generated via https://djecrety.ir/)
5. Run `make dev`.