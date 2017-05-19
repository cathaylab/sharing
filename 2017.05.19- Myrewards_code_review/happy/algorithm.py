# coding: utf-8
from __future__ import unicode_literals
from __future__ import division

import os
import pandas as pd
import numpy as np
import xgboost as xgb
import re
import pickle
import json
import logging
import itertools

from math import sqrt
from collections import defaultdict, OrderedDict
from xgboost import XGBClassifier
from sklearn import preprocessing
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler

from pyspark.mllib.recommendation import ALS, MatrixFactorizationModel, Rating




def merge_product(data_a, data_b, method):
    merge = pd.merge(data_a, data_b, how=method, on='customer_id')
    return merge


def final_data(data_a, data_b, method):
    # merge TXN
    origin_new = pd.merge(data_a, data_b, on = 'customer_id', how = method)
    origin_new = origin_new.reindex_axis(sorted(origin_new.columns), axis=1)
    origin_new = pd.concat([origin_new.ix[:, 10:], origin_new.ix[:, :10]], axis=1)
    origin_new['year_salary'] = origin_new['year_salary'].replace([np.nan, 0], \
                                                                  origin_new['year_salary'][
                                                                      origin_new['year_salary'] > 0].median())
    origin_new['utilization_rate'] = origin_new['utilization_rate'].replace([np.nan], \
                                                                        origin_new['utilization_rate']\
                                                                            [origin_new['utilization_rate'] >= 0].median())
    origin_new.loc[(origin_new['age'] < 18) & (origin_new['age'] > 90), "age"] = origin_new['age'][
        (origin_new['age'] >= 18) & (origin_new['age'] <= 90)].median()
    origin_new = origin_new.fillna(0)
    for i in ['place', 'gender', 'education']:
        origin_new[i] = origin_new[i].astype('category')

    # feature combination
    tmp_ss = StandardScaler()
    origin_new['norm_age'] = tmp_ss.fit_transform(origin_new['age'].values.reshape(-1, 1))
    origin_new['gas_age'] = origin_new['gas_station'] + origin_new['age']
    origin_new['con_age'] = origin_new['consumption_level'] + origin_new['age']
    for i in ['norm_age', 'gas_age', 'con_age']:
        origin_new[i] = origin_new[i].apply(lambda x: int(round(x)))
    origin_new['place_age'] = origin_new['place'] + origin_new['norm_age'].map(lambda x: str(x))
    origin_new['place_age'] = origin_new['place_age'].astype('category')
    origin_new = origin_new.drop(['consumption_level', 'place', 'norm_age', 'gas_station'], axis=1)

    categorical = ['gender', 'education', 'place_age']
    not_categorical = [x for x in origin_new.columns if x not in categorical]
    final = pd.concat([origin_new[not_categorical], pd.get_dummies(origin_new[categorical])], axis=1)
    return final


def record(data):
    ref_final = data.drop(['item_id'], axis=1)
    final_col = list(ref_final.columns)
    return final_col


# xgboost
def xgb_train(data):
    le = LabelEncoder()
    X = data.drop(['customer_id', 'item_id', 'bonus_points', 'bonus_points_level'], axis=1)
    y = data.loc[:, ['item_id']].apply(le.fit_transform)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    num_class = len(data['item_id'].unique())
    xgb_params = {
        'seed': 0,
        'num_class': num_class,
        'colsample_bytree': 0.3085,
        'silent': 1,
        'subsample': 0.7,
        'learning_rate': 0.01,
        'objective': 'multi:softprob',
        'max_depth': 7,
        'num_parallel_tree': 1,
        'min_child_weight': 4.2922,
        'eval_metric': 'mlogloss',
        'eta': 0.1,
        'gamma': 0.5290,
        'subsample': 0.9930,
        'max_delta_step': 0,
        'booster': 'gbtree',
        'nrounds': 1001
    }
    xg_train = xgb.DMatrix(X_train, y_train)
    xg_test = xgb.DMatrix(X_test, label=y_test)

    xgb_cv_res = xgb.cv(xgb_params, xg_train, num_boost_round=2001, nfold=4, seed=0, stratified=False, \
                        early_stopping_rounds=25, verbose_eval=50, show_stdv=True)

    best_nrounds = xgb_cv_res.shape[0] - 1
    xgb_best = xgb.train(xgb_params, xg_train, best_nrounds)
    return xgb_best


def xgb_filter_all(data_a, column, data_b, data_c, xgb_algorithm):
    ginal = data_a[column]
    le = LabelEncoder()
    X_everybody = ginal.drop(['customer_id', 'bonus_points', 'bonus_points_level'], axis=1)
    y = data_b.loc[:, ['item_id']].apply(le.fit_transform)
    xg_all = xgb.DMatrix(X_everybody)
    pred = xgb_algorithm.predict(xg_all)

    ginal_item = le.inverse_transform(np.argsort(np.array(pred), axis=1)[:, ::-1])
    data_a['recommended_products'] = ginal_item.tolist()
    retain = ['customer_id', 'bonus_points_level', 'recommended_products']
    merge_people = data_a.drop([x for x in data_a.columns if x not in retain], axis=1)
    origin_product = merge_people['recommended_products'].tolist()

    ip = data_c.toPandas()
    ip.columns = ['item_id', 'item_points_level']
    dct = dict(zip(ip['item_id'], ip['item_points_level']))
    xgb_filter_item = OrderedDict()
    for i in range(len(origin_product)):
        name = merge_people['customer_id'].iloc[i]
        for j in origin_product[i]:
            if dct.get(j) <= merge_people['bonus_points_level'][merge_people.index[i]]:
                xgb_filter_item.setdefault(name, []).append(j)

    return xgb_filter_item, dct


def als_process(data):
    # ALS
    als_people = data.groupBy('customer_id', 'item_id').agg({"cnt": "sum"}).withColumnRenamed("sum(cnt)", "cnt_x")
    als_people_sum = als_people.groupBy('customer_id').agg({"cnt_x": "sum"}).withColumnRenamed("sum(cnt_x)", "cnt_y")
    als_people = als_people.join(als_people_sum, "customer_id", "inner") \
        .withColumn("cnt", col("cnt_x") / col("cnt_y")).drop('cnt_x', 'cnt_y')
    als_people = als_people.toPandas()
    customer_list = dict(enumerate(set(als_people['customer_id'].tolist())))
    customer_list = {v: k for k, v in customer_list.iteritems()}
    item_list = dict(enumerate(set(als_people['item_id'].tolist())))
    item_list = {v: k for k, v in item_list.iteritems()}

    als_people.loc[:, 'customer_id'] = als_people.loc[:, 'customer_id'].map(customer_list)
    als_people.loc[:, 'item_id'] = als_people.loc[:, 'item_id'].map(item_list)

    reward_data = sqlContext.createDataFrame(als_people).rdd
    als_data = reward_data.map(lambda x: Rating(int(x[0]), (int(x[1])), float(x[2])))
    train, validation, test = als_data.randomSplit([0.6, 0.2, 0.2], 1234)
    validation_input = validation.map(lambda x: (x[0], x[1]))
    test_input = test.map(lambda x: (x[0], x[1]))
    best_rank = 12
    best_lambda = 0.1
    best_iteration = 10
    seed = 5L

    final_model = ALS.trainImplicit(als_data, best_rank, seed=seed, \
                                    iterations=best_iteration, lambda_=best_lambda)
    return final_model, customer_list, item_list


# item
def als_mapping(data_a, list_a, list_b, diction):
    # global broad_CustIds, broad_ItemIds, broad_ItemLevels, bCust

    broad_CustIds = None
    broad_ItemIds = None
    broad_ItemLevels = None
    bCust = None
    broad_UserLevels = None

    customerId_dict = {v: k for k, v in list_a.items()}
    itemId_dict = {v: k for k, v in list_b.items()}

    bCust = sc.broadcast(list_a)
    broad_ItemLevels = sc.broadcast(diction)
    broad_ItemIds = sc.broadcast(itemId_dict)
    broad_CustIds = sc.broadcast(customerId_dict)

    user_level_map = data_a.select("customer_id", "bonus_points_Level").rdd \
        .map(lambda row: (bCust.value[row["customer_id"]], row["bonus_points_Level"])) \
        .collectAsMap()
    broad_UserLevels = sc.broadcast(user_level_map)
    return (broad_CustIds, broad_ItemIds, broad_ItemLevels, bCust, broad_UserLevels)


def filter_prod_by_level(data):
    # global broad_CustIds ,broad_ItemIds ,broad_ItemLevels ,broad_UserLevels
    user, ratings = data
    prods = []
    for rating in ratings:
        # user
        user_name = broad_CustIds.value[rating.user]  # 49967 -> A1234444
        user_level = broad_UserLevels.value[rating.user]  # 49967 -> 3
        # item
        item_name = broad_ItemIds.value[rating.product]  # 73 -> A_3567XX
        item_level = broad_ItemLevels.value[item_name]  # A_3567X -> 3
        if item_level <= user_level:
            prods.append(item_name)
    return (user_name, prods)


def als_filter_all(model, count_item=200):
    #	global broad_CustIds ,broad_ItemIds ,broad_ItemLevels ,bCust
    ALS_people = model.recommendProductsForUsers(count_item). \
        map(filter_prod_by_level)
    ALS_people = ALS_people.toDF(["customer_id", "items"]).toPandas()
    return ALS_people
