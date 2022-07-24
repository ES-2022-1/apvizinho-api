from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.announcement.services.address_service import AddressService
from app.announcement.services.announcement_service import AnnouncementService
from app.announcement.services.vacancy_service import VacancyService
from app.auth.services.auth_service import AuthService
from app.common.exceptions import AuthExceptionHTTPException
from app.db.database import SessionLocal
from app.user.services.comment_service import CommentService
from app.user.services.review_service import ReviewService
from app.user.services.user_service import UserService


def get_db():
    db = SessionLocal()
    try:
        yield db
    except:  # noqa: E722
        db.rollback()
        raise
    else:
        if db.is_active:
            db.commit()
    finally:
        db.close()


def get_address_service(db: Session = Depends(get_db)):
    return AddressService(db)


def get_vacancy_service(db: Session = Depends(get_db)):
    return VacancyService(db)


def get_announcement_service(
    db: Session = Depends(get_db),
    address_service: AddressService = Depends(get_address_service),
    vacancy_service: VacancyService = Depends(get_vacancy_service),
):
    return AnnouncementService(db, address_service=address_service, vacancy_service=vacancy_service)


def get_review_service(db: Session = Depends(get_db)):
    return ReviewService(db)


def get_comment_service(db: Session = Depends(get_db)):
    return CommentService(db)


def get_user_service(
    db: Session = Depends(get_db),
    review_service=Depends(get_review_service),
):
    return UserService(db, review_service=review_service)


def get_auth_service(user_service: UserService = Depends(get_user_service)):
    return AuthService(user_service=user_service)


security = HTTPBearer()


def hass_access(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service),
):
    if credentials:
        if not credentials.scheme == "Bearer":
            raise AuthExceptionHTTPException(
                status_code=403, detail="Invalid authentication scheme."
            )
        if not auth_service.auth(token=credentials.credentials):
            raise AuthExceptionHTTPException(
                status_code=403, detail="Invalid token or expired token."
            )
        return credentials.credentials
    else:
        raise AuthExceptionHTTPException(status_code=403, detail="Invalid authorization code.")
