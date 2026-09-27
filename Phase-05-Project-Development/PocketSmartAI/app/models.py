from datetime import datetime, timezone
from sqlalchemy import String, Text, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

def now(): return datetime.now(timezone.utc)
class User(Base):
    __tablename__="users"; id:Mapped[int]=mapped_column(Integer,primary_key=True); email:Mapped[str]=mapped_column(String(255),unique=True,index=True); password_hash:Mapped[str]=mapped_column(String(255)); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now); recommendations=relationship("Recommendation",back_populates="user",cascade="all, delete-orphan")
class Recommendation(Base):
    __tablename__="recommendations"; id:Mapped[int]=mapped_column(Integer,primary_key=True); user_id:Mapped[int]=mapped_column(ForeignKey("users.id"),index=True); planner_type:Mapped[str]=mapped_column(String(30)); request_json:Mapped[str]=mapped_column(Text); result_json:Mapped[str]=mapped_column(Text); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now); user=relationship("User",back_populates="recommendations")
