from fastapi import FastAPI
from  fastapi_users import fastapi_users
from src.api.routers import all_routers

app = FastAPI(title="Student Tests App")

for router in all_routers:
    app.include_router(router)


