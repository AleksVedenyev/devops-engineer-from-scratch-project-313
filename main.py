from fastapi import FastAPI

app = FastAPI()


@app.get("/ping")
def main():
    return "pong"


if __name__ == "__main__":
    main()
