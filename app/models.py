from sqlalchemy import Column, Integer, String, Numeric, Date
from datetime import date
from .database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    amount = Column(Numeric(10,2))
    category = Column(String(50))
    description = Column(String(200))
    date = Column(Date, default=date.today)
    status = Column(String(20), default="pending") 