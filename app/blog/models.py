from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base


class Blog(Base):
    __tablename__ = "blog"

    id = Column(Integer, primary_key=True)
    title = Column(String(30))
    description = Column(String)
    published = Column(Boolean)
    user_id = Column(Integer, ForeignKey("user.id"))
    creator = relationship("User", back_populates="blogs")
    comment_id = Column(Integer, ForeignKey("comment.id"))