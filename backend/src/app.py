from ephaptic import Ephaptic
from ephaptic.ext.fastapi import Router
from fastapi import FastAPI

import os

from . import data, models

app = FastAPI(root_path='/api')

REDIS_URL = os.getenv('REDIS_URL')

ephaptic = Ephaptic.from_app(app, path='/_ws', redis_url=REDIS_URL)

api = Router(ephaptic, prefix='/v1')

@api.get('/records')
async def records() -> list[models.ForecourtRecord]:
    return await data.fetch_data()

app.include_router(api)