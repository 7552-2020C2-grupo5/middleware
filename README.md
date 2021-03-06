# BookBNB Middleware API


### Dependencies

To install all dependencies first install python3-pip. Then run:

```console
pip install -r requirements.txt
```

### Local deploy

To deploy locally, on middleware root directory run:

```console
gunicorn -w 2 --bind 0.0.0.0:<port> "bookbnb_middleware.app:create_app()"
```

### Heroku deploy

```console
heroku login
git remote add heroku https://git.heroku.com/middlewarebookbnb.git
git push heroku master
```

### Commits

Install pre-commit

```console
pip install pre-commit
pre-commit install
```
