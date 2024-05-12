from src.api.auth import router as auth_router
from src.api.operation import router as operation_router

all_routers = [
    auth_router,
    operation_router,
]