from fastapi import FastAPI, Depends
from .router import scraping, auth
from .oauth2 import get_current_active_user
from .schemas import User  # assuming User is defined in schemas.py
from .schemas import settings 

app = FastAPI()

app.include_router(scraping.router)
app.include_router(auth.router)

# Protected route that depends on the current active user (token validation)
@app.get("/", tags=['Root'])
async def root(current_user: dict  = Depends(get_current_active_user)):
    return {"message": f"Hello, {current_user['full_name']}!"}
