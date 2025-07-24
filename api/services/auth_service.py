import hmac
import hashlib
import base64
from typing import Optional
from datetime import datetime, timedelta
import os

from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/token")  # token endpoint

class AuthService:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret')  # default fallback
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60
    WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', 'dev-secret')

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ─── PASSWORD ─────────────────────────────
    @classmethod
    def hash_password(cls, password: str) -> str:
        return cls.pwd_context.hash(password)

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return cls.pwd_context.verify(plain_password, hashed_password)

    # ─── JWT ──────────────────────────────────
    @classmethod
    def create_access_token(cls, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=cls.ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)

    @classmethod
    def get_current_user(cls, token: str = Depends(oauth2_scheme)) -> dict:
        try:
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
            user_id: str = payload.get("sub")
            if user_id is None:
                raise HTTPException(status_code=401, detail="Invalid token: missing user ID")
            return {"user_id": user_id}
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

    # ─── WEBHOOK VERIFICATION ─────────────────
    @classmethod
    async def verify_webhook(cls, request: Request) -> None:
        """
        Verifies that the webhook request comes from a trusted source
        using HMAC-SHA256 with a shared secret.
        """
        body = await request.body()
        hmac_header = request.headers.get("X-Shopify-Hmac-Sha256")

        if not hmac_header:
            raise HTTPException(status_code=400, detail="Missing HMAC header")

        digest = hmac.new(cls.WEBHOOK_SECRET.encode(), body, hashlib.sha256).digest()
        computed_hmac = base64.b64encode(digest).decode()

        if not hmac.compare_digest(computed_hmac, hmac_header):
            raise HTTPException(status_code=401, detail="Invalid webhook signature")
