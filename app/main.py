
from fastapi import FastAPI
from modules import container_service
import uvicorn
from settings import UGCFilterSettings


app_settings = UGCFilterSettings().app_settings
app = FastAPI()


@app.api_route('/')
def index():
    return {'text': 'text'}


@app.post('/recognize', status_code=200)
def recognize(source: str, prefix: str) -> str:
    try:
        message = container_service._recongize_service.recognize_ugc(
            source, prefix)
        code = 200
    except Exception as ex:
        message = ex
        code = 400
    return {'code': code, 'message': message}


if __name__ == '__main__':
    uvicorn.run(app, port=app_settings['port'], host=app_settings['host'])
