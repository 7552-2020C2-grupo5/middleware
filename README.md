# BookBNB Middleware API 

### Heroku deploy

- heroku login
- git remote add heroku https://git.heroku.com/middlewarebookbnb.git
- git push heroku master

### Local deploy

- `pip install -r requirements`
- `gunicorn -w 2 --bind 0.0.0.0:<puerto> "bookbnb_middleware.app:create_app()"`

### Commits

- pip install pre-commit
- pre-commit install
- commit
