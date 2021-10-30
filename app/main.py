
from fastapi import FastAPI
from modules import container_service
import uvicorn
from settings import UCGFilterSettings


app_settings = UCGFilterSettings().app_settings
app = FastAPI()


@app.api_route('/')
def index():
    return {'text': 'text'}


@app.post('/recognize', status_code=200)
def recognize(source: str, prefix: str) -> str:
    message = container_service._recongize_service.recognize_video(source, prefix)
    return {'code': 200, 'message': message}


if __name__ == '__main__':
    uvicorn.run(app, port=app_settings['port'], host=app_settings['host'])
