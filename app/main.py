
from fastapi import FastAPI
import uvicorn
from settings import UCGFilterSettings

app_settings = UCGFilterSettings().app_settings
app = FastAPI()


@app.api_route('/')
def index():
    return {'text': 'text'}


if __name__ == '__main__':
    uvicorn.run(app, port=app_settings['port'], host=app_settings['host'])
