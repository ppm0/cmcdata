from sqlalchemy import Column, String, Numeric, BigInteger, DateTime, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class GlobalTokenHistory(Base):
    __tablename__ = 'gth'
    gth_id = Column(BigInteger, primary_key=True, autoincrement=True)
    ts = Column(DateTime(), nullable = False)
    tid = Column(Integer, ForeignKey('token.token_id'), nullable = False)
    price_btc = Column(Numeric(30, 8))
    price_usd = Column(Numeric(30, 8))
    volume_24h_usd = Column(Numeric(30, 8))


class Token(Base):
    __tablename__ = 'token'
    token_id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String(50), unique=True, nullable=False)
    code = Column(String(10))
