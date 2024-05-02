from fastapi_users import FastAPIUsers
from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy
from fastapi_users.authentication import Authenticator

from service.manager import get_user_manager
from model.auth import User
from conf import SECRET_AUTH

cookie_transport = CookieTransport(cookie_name="users_cookie", cookie_max_age=3600)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET_AUTH, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

authenticator = Authenticator([auth_backend], get_user_manager)

current_user = fastapi_users.current_user()