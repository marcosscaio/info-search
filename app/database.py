from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session

DATABASE_URL = "sqlite:///./searches.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class SearchEntry(Base):
    __tablename__ = "searches"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    price = Column(String)
    search_count = Column(Integer, default=1)

Base.metadata.create_all(bind=engine)