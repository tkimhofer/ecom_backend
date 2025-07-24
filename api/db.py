from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://user:pass@db:5432/shopmate")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    from api.models import Base, Order, RawOrder  # make sure Base is imported
    from api.test.test_data import placeDummyData, place_dummy_into_raw      # wherever you store it

    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()

    # try:

    if not db.query(RawOrder).first():

        place_dummy_into_raw()

        print("Seeding database with dummy data...")
    else:
        print("DB already seeded, skipping dummy data.")

    # finally:
    db.close()