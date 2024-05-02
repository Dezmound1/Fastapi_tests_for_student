from fastapi import FastAPI
from  fastapi_users import fastapi_users
from api.routers import all_routers

app = FastAPI(title="Student Tests App")

for router in all_routers:
    app.include_router(router)



# app.include_router(
#     fastapi_users.get_auth_router(auth_backend),
#     prefix="/auth",
#     tags=["Auth"],
# )

# app.include_router(
#     fastapi_users.get_register_router(UserRead, UserCreate),
#     prefix="/auth",
#     tags=["Auth"],
# )
