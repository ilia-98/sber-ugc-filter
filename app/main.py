
from fastapi import FastAPI


app = FastAPI()


@app.api_route('/')
def index():
    return {'text': 'text'}
