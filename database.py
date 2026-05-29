from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "postgresql://postgres:Om%4012s3@localhost/taskdb"

engine = create_engine(DATABASE_URL)

sessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

def get_db():
    db: Session = sessionLocal()
    try:
        yield db
    finally:
        db.close()