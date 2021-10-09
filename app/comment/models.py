from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base


class Comment(Base):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True)
    description = Column(String)
    blog_id = relationship("Blog", backref="comment")

    user_id = Column(Integer, ForeignKey("user.id"))
