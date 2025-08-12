import bcrypt
from flask_jwt_extended import create_access_token
from ..models import User
from ..extensions import db

def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()

def check_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())

def create_user(email: str, password: str) -> User:
    user = User(email=email, password_hash=hash_password(password))
    db.session.add(user)
    db.session.commit()
    return user

def authenticate(email: str, password: str) -> str | None:
    user = User.query.filter_by(email=email).first()
    if user and check_password(password, user.password_hash):
        return create_access_token(
            identity=str(user.id),
            additional_claims={"email": user.email}
        )
    return None
