from fastapi import APIRouter

from api.v1.endpoints.auth import router as auth_v1_router
from api.v1.endpoints.user import router as user_v1_router

routers = APIRouter(prefix="/v1")


router_list = [user_v1_router, auth_v1_router]

for router in router_list:
    routers.include_router(router)
