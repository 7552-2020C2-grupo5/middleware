# BookBNB Middleware API


### Dependencies

To install all dependencies first install python3-pip. Then run:
`pip install -r requirements.txt`

### Local deploy

To deploy locally, on middleware root directory run:

- `gunicorn -w 2 --bind 0.0.0.0:<port> "bookbnb_middleware.app:create_app()"`

### Heroku deploy

- heroku login
- git remote add heroku https://git.heroku.com/middlewarebookbnb.git
- git push heroku master

### Commits

- pip install pre-commit
- pre-commit install
- commit
