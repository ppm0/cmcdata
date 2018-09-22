from sqlalchemy import Column, String, Numeric, BigInteger, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class GlobalTokenHistory(Base):
    __tablename__ = 'gth'
    gth_id = Column(BigInteger, primary_key=True)
    ts = Column(DateTime())
    token = Column(String(10))
    token_id = Column(String(50))
    price_btc = Column(Numeric(30, 8))
    price_usd = Column(Numeric(30, 8))
    volume_24h_usd = Column(Numeric(30, 8))