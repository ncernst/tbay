from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Boolean
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
    topBidPrice = Column(Float, default = 0.00)
    topBid_id = Column(Integer, default = None)

    auctioner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    auctionerRelationship = relationship("User", foreign_keys=[auctioner_id])

    
    def submitBid(self, bid):
        accepted = False
        if bid.price > self.topBidPrice:
            self.topBidPrice = bid.price
            self.topBid_id = bid.id
            accepted = True
            session.commit()
        return accepted
        
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)
    password = Column(String, nullable = False)
    
    userBids = relationship("Bid", backref="bidder")
    listedItems = relationship("Item", backref="auctioner")

    def __init__(self, Name, Password):
        self.name = Name
        self.password = Password
        session.add(self)
        session.commit()
    
    def createAuction(self, itemName, itemDescription):
        newItem = Item()
        newItem.name = itemName
        newItem.description = itemDescription
        newItem.auctioner_id = self.id
        session.add(newItem)
        session.commit()
        return newItem
    
    def createBid(self, amount, item):
        newBid = Bid()
        newBid.price = amount
        newBid.bidder_id = self.id
        session.add(newBid)
        session.commit()
        
        newBid.bidAccepted = item.submitBid(newBid)


class Bid(Base):
    __tablename__ = "bids"
    
    id = Column(Integer, primary_key = True)
    price = Column(Float, nullable = False)
    bidAccepted = Column(Boolean, nullable = False, default = False)
    bidder_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
Base.metadata.create_all(engine)