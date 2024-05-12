from typing import Any, Dict, Union, Tuple

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm

from fastapi_users import BaseUserManager, exceptions, models, schemas
from fastapi_users.router.common import ErrorCode, ErrorModel
from fastapi_users.authentication.strategy import Strategy

from src.schema.auth import UserCreate, UserRead
from src.service.manager import UserManager, get_user_manager
from src.utils.user_config import JWTStrategy, authenticator
from src.utils.user_config import auth_backend

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

OpenAPIResponseType = Dict[Union[int, str], Dict[str, Any]]
logout_responses: OpenAPIResponseType = {
    **{
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user."
        }
    },
    **auth_backend.transport.get_openapi_logout_responses_success(),
}
login_responses: OpenAPIResponseType = {
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorModel,
            "content": {
                "application/json": {
                    "examples": {
                        ErrorCode.LOGIN_BAD_CREDENTIALS: {
                            "summary": "Bad credentials or the user is inactive.",
                            "value": {"detail": ErrorCode.LOGIN_BAD_CREDENTIALS},
                        },
                        ErrorCode.LOGIN_USER_NOT_VERIFIED: {
                            "summary": "The user is not verified.",
                            "value": {"detail": ErrorCode.LOGIN_USER_NOT_VERIFIED},
                        },
                    }
                }
            },
        },
        **auth_backend.transport.get_openapi_login_responses_success(),
    }
requires_verification: bool = False

@router.post(
        "/register",
        response_model=UserRead,
        status_code=status.HTTP_201_CREATED,
        name="register:register",
        responses={
            status.HTTP_400_BAD_REQUEST: {
                "model": ErrorModel,
                "content": {
                    "application/json": {
                        "examples": {
                            ErrorCode.REGISTER_USER_ALREADY_EXISTS: {
                                "summary": "A user with this email already exists.",
                                "value": {
                                    "detail": ErrorCode.REGISTER_USER_ALREADY_EXISTS
                                },
                            },
                            ErrorCode.REGISTER_INVALID_PASSWORD: {
                                "summary": "Password validation failed.",
                                "value": {
                                    "detail": {
                                        "code": ErrorCode.REGISTER_INVALID_PASSWORD,
                                        "reason": "Password should be"
                                        "at least 3 characters",
                                    }
                                },
                            },
                        }
                    }
                },
            },
        },
    )
async def register(
    request: Request,
    user_create: UserCreate,
    user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
):
    try:
        created_user = await user_manager.create(
            user_create, safe=True, request=request
        )
    except exceptions.UserAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.REGISTER_USER_ALREADY_EXISTS,
        )
    except exceptions.InvalidPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.REGISTER_INVALID_PASSWORD,
                "reason": e.reason,
            },
        )

    return schemas.model_validate(UserRead, created_user)

@router.post(
        "/login",
        name=f"auth:{auth_backend.name}.login",
        responses= login_responses
    )
async def login(
    request: Request,
    credentials: OAuth2PasswordRequestForm = Depends(),
    user_manager: UserManager[models.UP, models.ID] = Depends(get_user_manager),
    strategy: JWTStrategy[models.UP, models.ID] = Depends(auth_backend.get_strategy),
):
    user = await user_manager.authenticate(credentials)

    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.LOGIN_BAD_CREDENTIALS,
        )
    if requires_verification and not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.LOGIN_USER_NOT_VERIFIED,
        )
    response = await auth_backend.login(strategy, user)
    await user_manager.on_after_login(user, request, response)
    return response

get_current_user_token = authenticator.current_user_token(
    active=True, verified=requires_verification
)

@router.post(
    "/logout", name=f"auth:{auth_backend.name}.logout", 
    responses=logout_responses
)
async def logout(
    user_token: Tuple[models.UP, str] = Depends(get_current_user_token),
    strategy: Strategy[models.UP, models.ID] = Depends(auth_backend.get_strategy),
):
    user, token = user_token(active=True, verified=requires_verification)
    return await auth_backend.logout(strategy, user, token)
