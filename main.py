from fastapi import FastAPI
from routers import user, organization

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Multi-Tenant FastAPI API"}

app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(organization.router, prefix="/organizations", tags=["Organizations"])
