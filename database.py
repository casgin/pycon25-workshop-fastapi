from sqlalchemy import create_engine, DateTime, func, String, Integer, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

# SQLite URL; file-based DB in project root
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Create engine with future flag for SQLAlchemy 2.0 compatibility
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    future=True
)
# Session factory
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

# Declarative base for 2.0
class Base(DeclarativeBase):
    pass

class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Record identifier"
    )
    title: Mapped[str] = mapped_column(
        String(250),
        nullable=False,
        comment="Message title"
    )
    category: Mapped[str] = mapped_column(
        String(250),
        nullable=False,
        comment="Message category"
    )
    image: Mapped[str | None] = mapped_column(
        String(250),
        nullable=True,
        comment="File name for associated message image"
    )
    text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="Message text content"
    )
    created_at: Mapped[func.now()] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
        comment="When the message was created"
    )
    updated_at: Mapped[func.now()] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="When the message was last updated"
    )
    deleted_at: Mapped[DateTime | None] = mapped_column(
        DateTime,
        nullable=True,
        comment="Soft-delete timestamp; message hidden if set"
    )

# Dependency for FastAPI routes
def get_db():
    with SessionLocal() as session:
        yield session