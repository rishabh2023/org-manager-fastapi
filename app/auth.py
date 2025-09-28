import time, httpx
from fastapi import Depends, HTTPException, Request, status
from jose import jwt
from app.config import settings

_jwks_cache = {"keys": None, "ts": 0}
JWKS_TTL = 60 * 60  # 1h

async def get_jwks():
    now = time.time()
    if not _jwks_cache["keys"] or now - _jwks_cache["ts"] > JWKS_TTL:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(settings.SUPABASE_JWKS_URL)
            resp.raise_for_status()
            _jwks_cache["keys"] = resp.json()
            _jwks_cache["ts"] = now
    return _jwks_cache["keys"]

async def get_current_user(request: Request):
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    token = auth.split(" ", 1)[1]
    jwks = await get_jwks()

    try:
        payload = jwt.decode(token, jwks, algorithms=["RS256"], options={"verify_aud": False})
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

    user_id = payload.get("sub")
    email = payload.get("email")
    if not user_id:
        raise HTTPException(status_code=401, detail="Token missing sub")

    return {"user_id": user_id, "email": email, "claims": payload}
