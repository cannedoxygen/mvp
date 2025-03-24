import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base

# Create test database engine
TEST_DATABASE_URL = "sqlite:///./test_baseball_betting.db"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    """
    Create a new database session for a test function
    Rolls back changes after each test
    """
    # Create all tables in the test database
    Base.metadata.create_all(bind=engine)
    
    # Create a new database session
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        # Close the session and remove all data
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="session")
def test_app():
    """
    Fixture for creating a test application instance
    """
    from app.main import create_application
    return create_application()