from sqlalchemy import inspect
from app.models.user_model import metadata

def create_tables(engine):
    metadata.create_all(bind=engine)

# Session manager
from contextlib import contextmanager

@contextmanager
def get_session(session_factory):
    session = session_factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()