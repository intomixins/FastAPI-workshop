from fastapi import FastAPI

from settings import settings

import uvicorn

app = FastAPI()


@app.get('/')
def root():
    return {'message': 'hello!'}


if __name__ == '__main__':
    uvicorn.run(
        'workshop.app:app',
        host=settings.server_host,
        port=settings.server_port,
        reload=True,
    )
