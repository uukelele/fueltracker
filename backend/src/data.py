import httpx
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import hashlib, binascii, json, math, os
import pandas as pd
from io import BytesIO
import time
import redis.asyncio as redis

from . import models

URL = "https://www.fuel-finder.service.gov.uk/internal/v1.0.2/csv/generate-presigned-url"
SECRET = "8762dae892591b98df04f6badb39550ded3aec52e1227f816367af8d3064ba22"

REDIS_URL = os.getenv('REDIS_URL')
client = redis.from_url(REDIS_URL)

CACHE_KEY = 'fuel'
CACHE_TTL = 60 * 60 * 6 # 6 hours

def decrypt(enc):
    key = hashlib.sha256(SECRET.encode()).digest()

    iv = binascii.unhexlify(enc["iv"])
    ciphertext = binascii.unhexlify(enc["nxhex"])

    cipher = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
        backend=default_backend()
    )
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    unpadded = unpadder.update(decrypted) + unpadder.finalize()

    return json.loads(unpadded.decode("utf-8"))

def nest_dict(flat):
    root = {}
    for key, value in flat.items():
        parts = key.split(".")
        d = root
        for p in parts[:-1]:
            d = d.setdefault(p, {})
        d[parts[-1]] = value
    return root

def clean_nans(obj):
    if isinstance(obj, float) and math.isnan(obj):
        return None
    if isinstance(obj, dict):
        return {k: clean_nans(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [clean_nans(v) for v in obj]
    return obj

async def generate_presigned_url(client: httpx.AsyncClient | None) -> models.APIResponse:
    if not client: client = httpx.AsyncClient()
    res = await client.get(URL)
    res.raise_for_status()
    return models.APIResponse.model_validate(decrypt(res.json()))

async def fetch_all_data() -> list[models.ForecourtRecord]:
    async with httpx.AsyncClient() as client:
        data = await generate_presigned_url(client=client)
        res2 = await client.get(data.data.redirectUrl)
        res2.raise_for_status()

        df = pd.read_csv(BytesIO(res2.content))

    rows = [clean_nans(nest_dict(row)) for row in df.to_dict(orient='records')]

    return [models.ForecourtRecord(**row) for row in rows]

async def fetch_data() -> list[models.ForecourtRecord]:
    cached = await client.get(CACHE_KEY)
    if cached: return [models.ForecourtRecord(**row) for row in json.loads(cached)]
   
    data = await fetch_all_data()
    await client.set(CACHE_KEY, json.dumps([model.model_dump(mode='json') for model in data]), ex=CACHE_TTL)

    return data