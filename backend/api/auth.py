import os

from datetime import datetime, timedelta, timezone

from fastapi import (
    APIRouter,
    HTTPException,
    status,
    Request,
    Response,
    Depends,
)

from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# =========================================================
# CONFIG
# =========================================================

SECRET_KEY = os.getenv(
    "JARVIS_SECRET_KEY",
    "change-this-secret-in-production"
)

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24


# =========================================================
# PASSWORD HASHING
# =========================================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# =========================================================
# REQUEST SCHEMA
# =========================================================

class LoginRequest(BaseModel):

    username: str
    password: str


# =========================================================
# AUTH HELPERS
# =========================================================

def create_access_token(username: str):

    expire = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    payload = {
        "sub": username,
        "exp": expire
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def get_current_user(request: Request):

    token = request.cookies.get("jarvis_token")

    if not token:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required."
        )

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token."
            )

        return username

    except JWTError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token."
        )

# =========================================================
# CURRENT USER
# =========================================================

@router.get("/me")
def get_me(
    user: str = Depends(get_current_user)
):
    return {
        "username": user
    }

# =========================================================
# LOGIN
# =========================================================

@router.post("/login")
def login(
    credentials: LoginRequest,
    response: Response
):

    correct_username = os.getenv(
        "JARVIS_USERNAME"
    )

    password_hash = os.getenv(
        "JARVIS_PASSWORD_HASH"
    )

    if not correct_username or not password_hash:

        raise HTTPException(
            status_code=500,
            detail="JARVIS authentication is not configured."
        )


    if credentials.username != correct_username:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password."
        )


    if not pwd_context.verify(
        credentials.password,
        password_hash
    ):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password."
        )


    token = create_access_token(
        credentials.username
    )


    response.set_cookie(
        key="jarvis_token",
        value=token,
        httponly=True,
        secure=os.getenv("COOKIE_SECURE", "false").lower() == "true",
        samesite="none",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/"
    )


    return {
        "message": "Login successful."
    }


# =========================================================
# LOGOUT
# =========================================================

@router.post("/logout")
def logout(response: Response):

    secure = os.getenv("COOKIE_SECURE","false").lower() == "true"

    response.delete_cookie(
        key="jarvis_token",
        path="/",
        secure=secure,
        httponly=True,
        samesite="none",
    )

    return {
        "message": "Logout successful."
    }