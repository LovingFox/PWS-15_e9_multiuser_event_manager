release: flask db init
release: flask db migrate -m "first migration"
release: flask db upgrade
web: gunicorn events:app
