# -*- coding: utf-8 -*-
"""
Created on 2019-03-04
@author: YiChen
"""
import sys
import random
import math
import redis
from time import strftime, localtime
import time
from operator import itemgetter
from collections import defaultdict
random.seed(0)


class ItemBasedCF(object):

    def __init__(self):
        self.trainset = {}  # 存储训练集

        self.n_sim_items = 20  # 定义相似物品数20
        self.n_rec_items = 10  # 定义推荐物品数10

        self.items_sim_mat = {}  # 存储物品相似矩阵
        self.items_popular = {}
        self.items_count = 0

        print('相似物品数 = %d' % self.n_sim_items, file=sys.stderr)
        print('推荐物品数 = %d' % self.n_rec_items, file=sys.stderr)

    @staticmethod
    def load_data(classification):
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        for index, line in enumerate(r.lrange(classification, 0, -1)):
            yield line.strip('\r\n')

    def generate_dataset(self):
        trainset_len = 0
        if int(strftime('H', localtime(time.time()))) < 10:
            data = self.load_data('breakfast')
        elif int(strftime('H', localtime(time.time()))) > 10:
            data = self.load_data('dinner')
        for line in data:
            user, items, rating = line.split('::')
            self.trainset.setdefault(user, {})
            self.trainset[user][items] = int(rating)
            trainset_len += 1

    def calc_items_sim(self):
        # 记录物品被选购过的次数，从而反映出物品的流行度
        print('计算物品数量和流行程度…', file=sys.stderr)
        # 计算物品的流行度 实质是一个物品被多少用户操作过（即选购，并有评分） 以下数据虚构
        # {'914': 23, '3408': 12, '2355': 4, '1197': 12, '2804': 31, '594': 12  .....}
        for user, items in self.trainset.items():
            for item in items:
                # 计算物品流行度
                if item not in self.items_popular:
                    # 如果物品第一次出现 则置为0 加入到字典中。
                    self.items_popular[item] = 0
                self.items_popular[item] += 1

        print('计算物品数量和流行度成功', file=sys.stderr)

        # 计算总共被选购过的物品数
        self.items_count = len(self.items_popular)

        print('总计物品数量 = %d' % self.items_count, file=sys.stderr)

        # 根据用户使用习惯 构建物品相似度
        itemsim_mat = self.items_sim_mat

        print('建立用户矩阵倒排表...', file=sys.stderr)

        # {'914': defaultdict( <class 'int'>, {'3408': 1, '2355': 1  , '1197': 1, '2804': 1, '594': 1, '919': 1})}
        for user, items in self.trainset.items():
            for i1 in items:
                itemsim_mat.setdefault(i1, defaultdict(int))
                for i2 in items:
                    if i1 == i2:
                        continue
                    itemsim_mat[i1][i2] += 1

        print('建立用户矩阵倒排表成功', file=sys.stderr)
        print('计算商品相似读矩阵...', file=sys.stderr)

        simfactor_count = 0
        PRINT_STEP = 2000000

        # 计算用户相似度矩阵
        # 先取得特定用户
        for i1, related_items in itemsim_mat.items():
            for i2, count in related_items.items():
                # 以下公式为 两个a,b物品共同被喜欢的用户数/ 根号下（喜欢物品a的用户数 乘 喜欢物品b的用户数）
                itemsim_mat[i1][i2] = count / math.sqrt(
                    self.items_popular[i1] * self.items_popular[i2])
                simfactor_count += 1
                if simfactor_count % PRINT_STEP == 0:
                    print('计算物品相似度因素(%d)' % simfactor_count, file=sys.stderr)

        print('计算物品相似度矩阵成功', file=sys.stderr)
        print('总计相似因素数量 = %d' % simfactor_count, file=sys.stderr)
    # 找到K个相似物品 并推荐N个物品

    def recommend(self, user):

        K = self.n_sim_items
        N = self.n_rec_items
        rank = {}
        watched_items = self.trainset[user]

        for item, rating in watched_items.items():
            # 对于用户选购的每个物品 都找出其相似度最高的前K个物品
            for related_items, similarity_factor in sorted(self.items_sim_mat[item].items(), key=itemgetter(1), reverse=True)[:K]:
                if related_items in watched_items:
                    continue
                rank.setdefault(related_items, 0)
                # 假如评分权重，
                rank[related_items] += similarity_factor * rating
        # 返回综合评分最高的N个物品
        return sorted(rank.items(), key=itemgetter(1), reverse=True)[:N]
    # 计算准确率，召回率，覆盖率，流行度

    def evaluate(self):
        ''' print evaluation result: precision, recall, coverage and popularity '''
        print('Evaluation start...', file=sys.stderr)

        N = self.n_rec_items
        #  varables for precision and recall
        hit = 0
        rec_count = 0
        test_count = 0
        # varables for coverage
        all_rec_items = set()
        # varables for popularity
        popular_sum = 0

        for i, user in enumerate(self.trainset):
            if i % 500 == 0:
                print ('recommended for %d users' % i, file=sys.stderr)
            test_items = self.testset.get(user, {})
            rec_items = self.recommend(user)
            for item, _ in rec_items:
                if item in test_items:
                    hit += 1
                all_rec_items.add(item)
                popular_sum += math.log(1 + self.items_popular[item])
            rec_count += N
            test_count += len(test_items)
        # 准确率 = 推荐中的物品/总推荐的物品
        precision = hit / (1.0 * rec_count)
        # 召回率 = 推荐中的物品/测试集中所有物品数目
        recall = hit / (1.0 * test_count)
        coverage = len(all_rec_items) / (1.0 * self.items_count)
        popularity = popular_sum / (1.0 * rec_count)

        print ('precision=%.4f\trecall=%.4f\tcoverage=%.4f\tpopularity=%.4f' %
               (precision, recall, coverage, popularity), file=sys.stderr)


def use(user):
    itemcf = ItemBasedCF()
    itemcf.generate_dataset()
    itemcf.calc_items_sim()
    r_list = itemcf.recommend(user)
    f_list = []
    for index in r_list:
        f_list.append(str(index[0]))
    result = '::'.join(f_list)
    print(result)
    # itemcf.evaluate()
    return result




