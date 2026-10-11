# peer_lending_backend/src/security/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from peer_lending_backend.src.security.security import (
    verify_password, hash_password,
    create_access_token, create_refresh_token,
    decode_token
)
from peer_lending_backend.src.db.database import get_user_by_email, create_user
from peer_lending_backend.src.schemas.user import UserCreate, UserOut

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register", response_model=UserOut)
def register_user(payload: UserCreate):
    existing = get_user_by_email(payload.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(payload.password)
    user = create_user(payload.email, hashed_pw, payload.role)
    return user

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": user.email, "role": user.role})
    refresh_token = create_refresh_token({"sub": user.email})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh")
def refresh_token(refresh_token: str):
    payload = decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_access = create_access_token({"sub": payload["sub"]})
    return {"access_token": new_access}

@router.get("/me", response_model=UserOut)
def get_current_user(token: str = Depends()):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = get_user_by_email(payload["sub"])
    return user

@router.post("/logout")
def logout():
    # Stateless JWT logout pattern
    return {"message": "Logged out (client must delete tokens)"}
