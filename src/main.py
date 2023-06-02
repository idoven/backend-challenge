from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from routers.user import router as user_router
from routers.ecg import router as ecg_router

app = FastAPI()
app.include_router(user_router, tags=["Login"], prefix="/user")
app.include_router(ecg_router, tags=["Data"], prefix="/ecg")


@app.get("/")
async def root():
    return {"message": "Welcome, for documentation go to /docs"}


@app.post("/token")
async def login():
    response = RedirectResponse(url='/user/token')
    return response
