from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.jwt_handler import create_access_token

router = APIRouter()

fake_user = {"username": "admin", "password": "admin"}

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != fake_user["username"] or form_data.password != fake_user["password"]:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(data={"sub": fake_user["username"]})
    return {"access_token": token, "token_type": "bearer"}
