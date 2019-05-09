import redis
import os
import random
from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

def mysql_items():
    Base = declarative_base()

    class User(Base):
        __tablename__ = 'items'

        item_id = Column(String(4), primary_key=True)
        item_name = Column(String(20))
        item_type = Column(String(1))

    conn = create_engine('mysql+pymysql://root:980205@localhost:3306/Recommendation_system?charset=utf8')
    DBSession = sessionmaker(bind=conn)
    session = DBSession()
    return session, User

r = redis.Redis(host='localhost', port=6379, decode_responses=True)
ratingfile = os.path.join('user.dat')
session, User = mysql_items()
with open(ratingfile, 'r') as file:
    for i, line in enumerate(file):
        user, items, rating = line.split('::')
        if session.query(User.item_type).filter_by(item_id=items).all()[0][0] == '0':
            r.rpush("da", line)
            print("The %d push success"% i)
        elif session.query(User.item_type).filter_by(item_id=items).all()[0][0] == '1':
            r.rpush("ta", line)
            print("The %d push success" % i)


def createdata():
    with open('user.dat','w') as file:
        for i in range(1,6001):
            for j in range(30):
                file.write(str(i)+"::"+str(random.randint(1, 100))+"::"+str(random.randint(1, 5))+"\n")


# print(session.query(User.item_type).filter_by(item_id='2').all()[0][0])
# # session.commit()
# session.close()



