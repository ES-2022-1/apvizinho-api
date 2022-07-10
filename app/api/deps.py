from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.local.services.local_service import LocalService
from app.local.services.address_service import AddressService
from app.local.services.room_service import RoomService


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


def get_local_service(db: Session = Depends(get_db)):
    return LocalService(db)

def get_address_service(db: Session = Depends(get_db)):
    return AddressService(db)

def get_room_service(db: Session = Depends(get_db)):
    return RoomService(db)
