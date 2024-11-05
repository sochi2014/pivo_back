from app.database import SessionLocal


def get_db():
    """
    Yields a database session from the SessionLocal class.
    Ensures the session is closed after the request is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
