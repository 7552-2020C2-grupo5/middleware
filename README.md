# BookBNB Middleware API

### Heroku deploy

- heroku login
- git remote add heroku https://git.heroku.com/middlewarebookbnb.git
- git push heroku master

### Local deploy

- `pip install -r requirements.txt`
- `gunicorn -w 2 --bind 0.0.0.0:<port> "bookbnb_middleware.app:create_app()"`

### Commits

- pip install pre-commit
- pre-commit install
- commit
