from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# プロジェクトルートの data.db を使用
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./oms.db")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# DBセッションを取得するための依存性注入用関数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
