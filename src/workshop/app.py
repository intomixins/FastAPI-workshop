from fastapi import FastAPI

from settings import settings

import uvicorn

from workshop.api import router

tags_metadata = [
    {
        'name': 'auth',
        'description': 'Authorization and registration',
    },
    {
        'name': 'operations',
        'description': 'Work with operations',
    },
    {
        'name': 'reports',
        'description': 'Import and export of reports',
    },
]

app = FastAPI(
    title='WorkShop',
    description='App which helps you control you finances',
    version='1.0.0',
    openapi_tags=tags_metadata,
)
app.include_router(router)


if __name__ == '__main__':
    uvicorn.run(
        'workshop.app:app',
        host=settings.server_host,
        port=settings.server_port,
        reload=True,
    )
