from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base
from comment.models import Comment


class User(Base):

    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    email = Column(String(30), unique=True)
    password = Column(String)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    blogs = relationship("Blog", back_populates="creator")
