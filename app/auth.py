# app/auth.py
import time
from typing import Dict, Any, Optional

import httpx
from fastapi import HTTPException, Request, status
from jose import jwt
from jose.exceptions import JWTError, ExpiredSignatureError, JWTClaimsError  # <-- FIX
from app.config import settings

# --------------------------------------------------------------------------------------
# Config
# --------------------------------------------------------------------------------------

_JWKS_CACHE: Dict[str, Any] = {"jwks": None, "ts": 0.0}
JWKS_TTL_SEC = 60 * 60  # 1 hour

VERIFY_AUD = getattr(settings, "SUPABASE_VERIFY_AUD", False)
EXPECTED_AUD: Optional[str] = getattr(settings, "SUPABASE_EXPECTED_AUD", None)
VERIFY_ISS = getattr(settings, "SUPABASE_VERIFY_ISS", False)
EXPECTED_ISS: Optional[str] = getattr(settings, "SUPABASE_EXPECTED_ISS", None)

SUPABASE_JWKS_URL: Optional[str] = getattr(settings, "SUPABASE_JWKS_URL", None)
SUPABASE_ANON_KEY: Optional[str] = getattr(settings, "SUPABASE_ANON_KEY", None)

# Keep this only if you still have any HS256 tokens around:
SUPABASE_JWT_SECRET: Optional[str] = getattr(settings, "SUPABASE_JWT_SECRET", None)

# --------------------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------------------

def _bearer_token_from_request(request: Request) -> str:
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    token = auth.split(" ", 1)[1].strip()
    if not token:
        raise HTTPException(status_code=401, detail="Empty bearer token")
    return token

async def _fetch_jwks() -> Dict[str, Any]:
    if not SUPABASE_JWKS_URL:
        raise HTTPException(status_code=500, detail="SUPABASE_JWKS_URL is not configured")

    headers: Dict[str, str] = {}
    if SUPABASE_ANON_KEY:
        headers["apikey"] = SUPABASE_ANON_KEY
        headers["Authorization"] = f"Bearer {SUPABASE_ANON_KEY}"

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(SUPABASE_JWKS_URL, headers=headers)
            resp.raise_for_status()
            data = resp.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Failed to fetch JWKS: {e.response.status_code} {e.response.text[:200]}",
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to fetch JWKS: {str(e)}")

    if not isinstance(data, dict) or "keys" not in data or not isinstance(data["keys"], list):
        raise HTTPException(status_code=502, detail="Malformed JWKS from provider")
    return data

async def get_jwks() -> Dict[str, Any]:
    now = time.time()
    if not _JWKS_CACHE["jwks"] or (now - _JWKS_CACHE["ts"]) > JWKS_TTL_SEC:
        _JWKS_CACHE["jwks"] = await _fetch_jwks()
        _JWKS_CACHE["ts"] = now
    return _JWKS_CACHE["jwks"]

def _pick_jwk_for_kid(jwks: Dict[str, Any], kid: str) -> Optional[Dict[str, Any]]:
    return next((k for k in jwks.get("keys", []) if k.get("kid") == kid), None)

def _verify_optional_claims(claims: Dict[str, Any]) -> None:
    if VERIFY_AUD:
        aud = claims.get("aud")
        if EXPECTED_AUD and aud != EXPECTED_AUD:
            raise HTTPException(status_code=401, detail=f"Invalid audience: {aud}")
    if VERIFY_ISS:
        iss = claims.get("iss")
        if EXPECTED_ISS and iss != EXPECTED_ISS:
            raise HTTPException(status_code=401, detail=f"Invalid issuer: {iss}")

def _extract_user_from_claims(claims: Dict[str, Any]) -> Dict[str, Any]:
    user_id = claims.get("sub") or claims.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Token missing 'sub' claim")
    email = claims.get("email")
    return {"user_id": user_id, "email": email, "claims": claims}

# ----- decoders -----

async def _decode_es256(token: str, kid: Optional[str]) -> Dict[str, Any]:
    if not kid:
        raise HTTPException(status_code=401, detail="Token header missing 'kid'")
    jwks = await get_jwks()
    key = _pick_jwk_for_kid(jwks, kid)
    if not key:
        # force refresh once (rotation window)
        _JWKS_CACHE["jwks"] = None
        jwks = await get_jwks()
        key = _pick_jwk_for_kid(jwks, kid)
    if not key:
        raise HTTPException(status_code=401, detail="Matching ES256 JWK not found for token 'kid'")
    return jwt.decode(token, key, algorithms=["ES256"], options={"verify_aud": False})

def _decode_hs256(token: str) -> Dict[str, Any]:
    if not SUPABASE_JWT_SECRET:
        raise HTTPException(
            status_code=500,
            detail="SUPABASE_JWT_SECRET is not configured (required only for Legacy HS256 tokens).",
        )
    return jwt.decode(token, SUPABASE_JWT_SECRET, algorithms=["HS256"], options={"verify_aud": False})

# --------------------------------------------------------------------------------------
# Public dependency
# --------------------------------------------------------------------------------------

async def get_current_user(request: Request) -> Dict[str, Any]:
    token = _bearer_token_from_request(request)

    try:
        header = jwt.get_unverified_header(token)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token header: {str(e)}")

    alg = header.get("alg")
    kid = header.get("kid")

    try:
        if alg == "ES256":
            claims = await _decode_es256(token, kid)
        elif alg == "HS256":
            claims = _decode_hs256(token)
        else:
            raise HTTPException(status_code=401, detail=f"Unsupported token alg '{alg}'")
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except JWTClaimsError as e:
        raise HTTPException(status_code=401, detail=f"Invalid claims: {str(e)}")
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Signature/format error: {str(e)}")

    _verify_optional_claims(claims)
    return _extract_user_from_claims(claims)
