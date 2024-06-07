from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

engine = create_engine('sqlite:///../../users.db', echo=True)

Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
