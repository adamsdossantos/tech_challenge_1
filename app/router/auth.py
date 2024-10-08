from fastapi import Depends, status, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from .. import oauth2
from ..schemas import Token, ActiveUser

router = APIRouter(
    prefix="/login",
    tags=["Login"]
)

# Login route that provides a JWT if credentials are correct
@router.post("/", response_model=Token,summary="Acesso ao usuario ", description="Acesso ao API via JWT token" )
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = oauth2.authenticate_user(oauth2.fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Token expiration time
    access_token_expires = timedelta(minutes=oauth2.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Create access token
    access_token = oauth2.create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

# Route to get the current user's info (protected route)
@router.get("/users/me", response_model=ActiveUser, summary="Detalhes do usuário")
async def read_users_me(current_user: dict = Depends(oauth2.get_current_active_user)):
    return current_user
