from sqlalchemy.sql.expression import text
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import TIMESTAMP, Boolean, Integer, String

from .database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, nullable=False, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default='True')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()"))
