
from sqlalchemy import Column, Integer, String, Sequence
from database.database import Base


user_id_seq = Sequence("users_id_seq")


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        user_id_seq,
        primary_key=True,
        server_default=user_id_seq.next_value()
    )
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
