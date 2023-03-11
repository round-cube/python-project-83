PORT ?= 8000

install:
	poetry install
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app
dev:
	poetry run flask --app page_analyzer:app --debug run
lint:
	poetry run flake8 page_analyzer
run-db:
	docker run -p 5432:5432 \
			   -e POSTGRES_USER=janedoe \
			   -e POSTGRES_PASSWORD=mypassword \
			   -e POSTGRES_DB=mydb \
			   -v ${PWD}/database.sql:/docker-entrypoint-initdb.d/database.sql \
			   postgres:15.2
connect-db:
	psql ${DATABASE_URL}