from turtle import title
from passlib.context import CryptContext

pwd_context = CryptContext(
                schemes=["bcrypt"],
                deprecated="auto"
            )

def hash(password: str):
    try:
        return pwd_context.hash(password)
    except Exception as e:
        print(f"Error occured: {e}")

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def parse_mark_data(data):
    """
        Do correct parsing input string 8|note into 3 different cases:
        1) Input "8|some notes" -> mark = 8, note = 'some notes'
        2) Input "|some notes" -> mark = '', note = 'some notes'
        3) Input "8" -> mark = '8', note = ''
    """

    mark, separator, note = data.partition('|')
    
    mark = mark.strip()
    note = note.strip()
    
    return mark, note
