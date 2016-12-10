from tbay_sql import *


if __name__ == "__main__":
    beyonce = User("bknowls", "uhohuho")
    jayz = User("scarter", "lemonade")
    kanye = User("kwest", "ilovekanye")

    
    baseball = beyonce.createAuction("Baseball", "An MLB official, Rawlings baseball.")
    jayz.createBid(5.00, baseball)
    kanye.createBid(7.50, baseball)


    
    topBidId = session.query(Item.topBid_id).filter(Item.id == baseball.id).first()
    topBidderId = session.query(Bid.bidder_id).filter(Bid.id == topBidId).first() 
    topBidderName = session.query(User.name).filter(User.id == topBidderId).first() 
    print(topBidderName)