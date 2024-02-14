from sqlalchemy import create_engine,inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# PostgreSQL connection URL
SQLALCHEMY_DATABASE_URL = "postgresql://myuser:mypassword@postgres/mydatabase"
#DATABASE_URL = "sqlite:///./test.db"
# Create the database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base = declarative_base()
Base.metadata.create_all(bind=engine)
# Create a session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    if "users" not in table_names or "tasks" not in table_names:
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully")
    else:
        print("Tables already exist")

