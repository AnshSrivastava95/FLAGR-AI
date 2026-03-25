from sqlalchemy import Column,Integer,String,Float,DateTime
from datetime import datetime 
from database import Base

class FraudScore(Base):
    __tablename__="fraud_scores"
    
    id = Column(Integer, primary_key=True, index=True)

    symbol = Column(String, index=True)

    company = Column(String)

    m_score = Column(Float)

    risk = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)