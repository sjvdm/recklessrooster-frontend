Recklessrooster.

Who is more prone to crime?

An ASGI-fastapi based website. Probably overkill, but wanted to stresstest fastapi.

Todo still:

- Unit tests
- CI/CD pipeline
- Security (JWT/Oauth)
- Logging
- Integration testing


## Local dev

Within your dir, activate the env, install requirements, and run a local instance:

```
. venv/bin/activate/
pip install -r requirements.txt
uvicorn app:app --reload
```

Access the webpage at: 
http://127.0.0.1:8000

Auto generated API docs at: 
https://127.0.0.1:8000/docs
https://localhost:8000/redoc



## Stress testing

On mac, use wrk:

```
brew install wrk
```

Run a stress test to your local site:

```
wrk -t12 -c400 -d30s http://127.0.0.1:8000/
```

-t12: Number of threads.
-c400: Number of open connections.
-d30s: Duration of the test (30 seconds).


## Deploying to GCP

Ensure app.yaml is correctly setup in your root dir.

Set to correct account and project:
```
gcloud config set account `ACCOUNT`
gcloud config set project recklessroosters
```

Deploy:
```
gcloud app deploy
```

See GCP/Cloud Build/History for details on building. Might also be useful for debugging.

You can stream logs:
```
gcloud app logs tail -s default
```