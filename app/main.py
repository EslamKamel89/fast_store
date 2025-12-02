from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.db.session import engine


@asynccontextmanager
async def lifespan(app:FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(lambda _:None)
        print('app started successfully')
        yield
        print('app stopped successfully')
        
def create_app():
    app = FastAPI(title=settings.APP_NAME , lifespan=lifespan)
    @app.get('health')
    async def health():
        return {'status':'ok'}
    return app
app = create_app()