import redis
import os
import random
from sqlalchemy import create_engine, Column, String, Integer, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import string

def mysql_items():
    Base = declarative_base()

    class Food(Base):
        __tablename__ = 'foods'

        food_id = Column(Integer, primary_key=True)
        name = Column(String(255))
        sales = Column(Integer)
        grade = Column(Float(10, 1))
        price = Column(Float(10, 2))
        type = Column(Integer)
        type_name = Column(String(255))
        count = Column(Integer)
        icon = Column(String(255))

    conn = create_engine('mysql+pymysql://root:123456@39.107.74.157:7520/findu?charset=utf8')
    DBSession = sessionmaker(bind=conn)
    session = DBSession()
    return session, Food


pool = redis.ConnectionPool(host='39.105.170.59', port=6379, password='Xxmy.980205', decode_responses=True)
r = redis.Redis(connection_pool=pool)
ratingfile = os.path.join('rating_test.dat')
session, Food = mysql_items()
with open(ratingfile, 'r') as file:
    for i, line in enumerate(file):
        user, items, rating = line.split('::')
        if session.query(Food.type).filter(Food.food_id == items).one()[0] == 2:
            r.rpush("breakfast", line)
        elif session.query(Food.type).filter(Food.food_id == items).one()[0] == 4 or \
                session.query(Food.type).filter(Food.food_id == items).one()[0] == 3:
            r.rpush("dinner", line)
            print("The %d push success" % i)

def phone_num(num):
    all_phone_nums=set()
    num_start = ['134', '135', '136', '137', '138', '139', '150', '151', '152', '158', '159', '157', '182', '187', '188',
           '147', '130', '131', '132', '155', '156', '185', '186', '133', '153', '180', '189']
    for i in range(num):
        start = random.choice(num_start)
        end = ''.join(random.sample(string.digits,8))
        res = start+end
        all_phone_nums.add(res)
    return all_phone_nums


def createdata():
    phone = phone_num(2000)
    items = list(map(str, [x for x in range(2, 23) if (x != 15 and x != 17 and x != 8)]))
    with open('rating_test.dat', 'w') as file:
        for i in phone:
            for j in range(random.randint(5, 10)):
                file.write(str(i)+"::"+str(random.choice(items))+"::"+str(random.randint(1, 5))+"\n")

# createdata()
# print(session.query(User.item_type).filter_by(item_id='2').all()[0][0])
# # session.commit()
# session.close()



