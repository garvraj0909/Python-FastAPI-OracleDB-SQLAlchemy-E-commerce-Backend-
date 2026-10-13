
from sqlalchemy.orm import Session

from models.user import User
from core.security import hash_password


class UserService:

    def create_user(
        self,
        db: Session,
        name: str,
        email: str,
        password: str
    ):
        existing_user = db.query(User).filter(
            User.email == email
        ).first()

        if existing_user:
            raise ValueError("Email is already registered")

        user = User(
            name=name,
            email=email,
            password=hash_password(password)
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    def get_users(self, db: Session):
        return db.query(User).all()

    def get_user(self, db: Session, user_id: int):
        return db.query(User).filter(
            User.id == user_id
        ).first()

    def update_user(
        self,
        db: Session,
        user_id: int,
        name: str,
        email: str,
        password: str
    ):
        user = self.get_user(db, user_id)

        if user is None:
            return None

        existing_user = db.query(User).filter(
            User.email == email,
            User.id != user_id
        ).first()

        if existing_user:
            raise ValueError("Email is already registered")

        user.name = name
        user.email = email
        user.password = hash_password(password)

        db.commit()
        db.refresh(user)

        return user

    def delete_user(self, db: Session, user_id: int):
        user = self.get_user(db, user_id)

        if user is None:
            return False

        db.delete(user)
        db.commit()

        return True
