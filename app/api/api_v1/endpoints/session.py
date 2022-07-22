from fastapi import APIRouter, Depends

import app.api.deps as deps
from app.auth.schemas.auth import SessionCreate, Tokens
from app.auth.services.auth_service import AuthService
from app.common.exceptions import (
    AuthException,
    AuthExceptionHTTPException,
    RecordNotFoundException,
    RecordNotFoundHTTPException,
)

router = APIRouter()


@router.post("/", response_model=Tokens)
def session(session_create: SessionCreate, service: AuthService = Depends(deps.get_auth_service)):
    try:
        return service.create_tokens(session_create=session_create)
    except RecordNotFoundException:
        raise RecordNotFoundHTTPException(
            detail=f"User with email {session_create.email} not found"
        )
    except AuthException as ae:
        raise AuthExceptionHTTPException(detail=ae.detail)
