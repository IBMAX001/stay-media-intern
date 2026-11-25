from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class InternDB(Base):
    __tablename__ = "interns"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    role: Mapped[str] = mapped_column(String(100))
