from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.auth.jwt_handler import create_access_token
from app.auth.utils import verify_password
from app.models import User

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint to login and obtain a JWT token
@router.post("/token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),  # OAuth2 form for username and password
    db: Session = Depends(get_db)  # Database session dependency
):
    """
    Login endpoint to authenticate a user and issue a JWT token.

    - **username**: The username of the user.
    - **password**: The password of the user.

    Returns a JWT token if the credentials are valid.
    """
    # Check if the user exists and verify the password
    user = db.query(User).filter(User.username == form_data.username).first()

    if user is None or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Generate a JWT token for the authenticated user
    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
