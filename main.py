from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def login():
    return {'data':'d'}