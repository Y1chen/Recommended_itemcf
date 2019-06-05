# from sqlalchemy import create_engine, Column, String, Integer, Float
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
#
#
# def mysql_items():
#     Base = declarative_base()
#
#     class User(Base):
#         __tablename__ = 'foods'
#
#         food_id = Column(Integer, primary_key=True)
#         name = Column(String(255))
#         sales = Column(Integer)
#         grade = Column(Float(10, 1))
#         price = Column(Float(10, 2))
#         type = Column(Integer)
#         type_name = Column(String(255))
#         count = Column(Integer)
#         icon = Column(String(255))
#
#     conn = create_engine('mysql+pymysql://root:123456@39.107.74.157:7520/findu?charset=utf8')
#     DBSession = sessionmaker(bind=conn)
#     session = DBSession()
#     return session, User
#
#
# session, User = mysql_items()
# result = session.query(User.type).filter(User.food_id=="1").one()[0]
# print(type(result))
# print(result)
# import random
# import string
# def phone_num(num):
#     all_phone_nums=set()
#     num_start = ['134', '135', '136', '137', '138', '139', '150', '151', '152', '158', '159', '157', '182', '187', '188',
#            '147', '130', '131', '132', '155', '156', '185', '186', '133', '153', '180', '189']
#     for i in range(num):
#         start = random.choice(num_start)
#         end = ''.join(random.sample(string.digits,8))
#         res = start+end+'\n'
#         all_phone_nums.add(res)
#     with open('phone_num.txt','w',encoding='utf-8') as fw:
#         fw.writelines(all_phone_nums)
# phone_num(1000)

# items = list(map(str, [x for x in range(2, 23) if (x != 15 and x != 17)]))
# print(items)
import os

ratingfile = os.path.join('rating_test.dat')
phone = set()
with open(ratingfile, 'r') as file:
    for i, line in enumerate(file):
        user, items, rating = line.split('::')
        phone.add(user+'\n')
with open('D:\WorkSpace\Python\Recommended_itemcf\phone_num.dat', 'a') as f:
    f.writelines(phone)

