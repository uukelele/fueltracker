from ephaptic import Ephaptic
from ephaptic.ext.fastapi import Router
from fastapi import FastAPI

import os

app = FastAPI(root_path='/api')

ephaptic = Ephaptic.from_app(app, path='/_ws', redis_url=os.getenv('REDIS_URL'))

api = Router(ephaptic, prefix='/v1')

@api.get('/')
async def index():
    return {"status": "ok"}