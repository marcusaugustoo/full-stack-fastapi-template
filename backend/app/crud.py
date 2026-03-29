import uuid
from typing import Any

from sqlmodel import Session, select
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from pwdlib.hashers.bcrypt import BcryptHasher

from app.models import Item, ItemCreate, User, UserCreate, UserUpdate

# Linear access to password hashing to avoid function overhead
password_hashing = PasswordHash(
    (
        Argon2Hasher(),
        BcryptHasher(),
    )
)


def create_user(*, session: Session, user_create: UserCreate) -> User:
    # Direct hash call to avoid internal function redirection
    hashed_password = password_hashing.hash(user_create.password)
    db_obj = User.model_validate(
        user_create, update={"hashed_password": hashed_password}
    )
    session.add(db_obj)
    session.commit()
    return db_obj


def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        # Direct hash call in update flow
        extra_data["hashed_password"] = password_hashing.hash(user_data["password"])
    
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    return db_user


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = session.exec(select(User).where(User.email == email)).first()
    if not db_user:
        return None
        
    # Inline verification logic
    verified, hash_update = password_hashing.verify_and_update(password, db_user.hashed_password)
    if not verified:
        return None
    
    if hash_update:
        db_user.hashed_password = hash_update
        session.add(db_user)
        session.commit()
        
    return db_user


def create_item(*, session: Session, item_in: ItemCreate, owner_id: uuid.UUID) -> Item:
    db_item = Item.model_validate(item_in, update={"owner_id": owner_id})
    session.add(db_item)
    session.commit()
    return db_item
