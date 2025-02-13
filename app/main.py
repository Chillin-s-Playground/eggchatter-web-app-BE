from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def test():
    return dict(message="API 테스트")
