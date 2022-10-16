from datetime import datetime
import uuid
from .. import schemas, model
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from ..database import get_db
from application.oauth2 import require_user

router = APIRouter()

@router.get('/users', response_model=schemas.LoginSchema)
def listUsers(db: Session = Depends(get_db), pageNum: int = 1, pageSize: int = 10):
    skip = (pageNum - 1) * pageSize

    results = db.query(model.User).group_by(model.User.id).all()

    return {"status": "success", "results": len(results)}