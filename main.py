import os

import sentry_sdk
from fastapi import FastAPI

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    traces_sample_rate=1.0,
)


app = FastAPI()


@app.get("/ping")
def main():
    return "pong"


if __name__ == "__main__":
    main()
