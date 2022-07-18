from fastapi import Depends
from sqlalchemy.orm import Session

from app.announcement.services.address_service import AddressService
from app.announcement.services.announcement_service import AnnouncementService
from app.announcement.services.vacancy_service import VacancyService
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
    comment_service=Depends(get_comment_service),
):
    return UserService(db, review_service=review_service, comment_service=comment_service)
