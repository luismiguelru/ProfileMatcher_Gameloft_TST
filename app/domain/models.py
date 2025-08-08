from sqlalchemy import JSON, Column, DateTime, Float, Integer, String
from sqlalchemy.orm import declarative_base

BaseModel = declarative_base()

class PlayerProfile(BaseModel):
    __tablename__ = "player_profiles"

    player_id = Column(String, primary_key=True, index=True)
    credential = Column(String, nullable=False)
    created = Column(DateTime(timezone=True), nullable=False)
    modified = Column(DateTime(timezone=True), nullable=False)
    last_session = Column(DateTime(timezone=True), nullable=False)
    total_spent = Column(Float, default=0.0)
    total_refund = Column(Float, default=0.0)
    total_transactions = Column(Integer, default=0)
    last_purchase = Column(DateTime(timezone=True), nullable=False)
    active_campaigns = Column(JSON, default=list)
    devices = Column(JSON, default=list)
    level = Column(Integer, default=1)
    xp = Column(Integer, default=0)
    total_playtime = Column(Integer, default=0)
    country = Column(String, default="")
    language = Column(String, default="")
    birthdate = Column(DateTime(timezone=True), nullable=False)
    gender = Column(String, default="")
    inventory = Column(JSON, default=dict)
    clan = Column(JSON, default=dict)
    customfield = Column(String, name="_customfield")
