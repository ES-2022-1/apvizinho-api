from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.todo_list.services.todo_list_service import TodoListService


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


def get_todo_list_service(db: Session = Depends(get_db)):
    return TodoListService(db)
