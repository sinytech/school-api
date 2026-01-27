from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    try:
        return pwd_context.hash(password)
    except Exception as e:
        print(f"Error occured: {e}")

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
