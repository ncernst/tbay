from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship

engine = create_engine('postgresql://ubuntu:thinkful@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)
    description = Column(String)
    start_time = Column(DateTime, default = datetime.utcnow)
    
    auctioner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topBid_id = Column(Integer, ForeignKey("bids.id"), nullable=False)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)
    password = Column(String, nullable = False)
    
    userBids = relationship("Bid", backref="bidder")
    listedItems = relationship("Item", backref="auctioner")

class Bid(Base):
    __tablename__ = "bids"
    
    id = Column(Integer, primary_key = True)
    price = Column(Float, nullable = False)

    bidder_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    item = relationship("Item", uselist=False, backref="bid")

Base.metadata.create_all(engine)