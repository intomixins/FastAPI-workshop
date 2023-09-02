from fastapi import FastAPI

from settings import settings

import uvicorn

from workshop.api import router

app = FastAPI()
app.include_router(router)


if __name__ == '__main__':
    uvicorn.run(
        'workshop.app:app',
        host=settings.server_host,
        port=settings.server_port,
        reload=True,
    )
