
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from schemas.user import UserCreate, UserResponse
from services.user_service import UserService
from database.database import get_db
from core.security import get_current_user


router = APIRouter(prefix="/users", tags=["Users"])
user_service = UserService()


@router.post("/", response_model=UserResponse,
             status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return user_service.create_user(
            db, user.name, user.email, user.password
        )
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error))


@router.get("/", response_model=list[UserResponse])
def get_users(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return user_service.get_users(db)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user = user_service.get_user(db, user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    try:
        updated_user = user_service.update_user(
            db, user_id, user.name, user.email, user.password
        )
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error))

    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return updated_user


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    deleted = user_service.delete_user(db, user_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User deleted successfully"}
