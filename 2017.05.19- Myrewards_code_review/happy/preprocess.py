# coding: utf-8
from __future__ import unicode_literals
from __future__ import division

import os
import jaydebeapi as jdbc
import pandas as pd
import numpy as np
import logging
import itertools

from math import sqrt
from collections import defaultdict, OrderedDict
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from pyspark import SparkContext
from pyspark.sql import HiveContext, DataFrameWriter
from pyspark.sql.functions import lit
from pyspark.sql.functions import col 

sc = SparkContext()
hc = HiveContext(sc)
sqlContext = HiveContext(sc)

#connect


def td_spark(table):
	HOST = "88.8.98.214"
	DB = "fh_temp"
	USER = "i0ac30az"
	PWD = "WWWhelp0#"
	CONNECT_URL = "jdbc:teradata://{}/TMODE=TERA,CLIENT_CHARSET=WINDOWS-950,DATABASE={},USER={},PASSWORD={}" \
		.format(HOST, DB, USER, PWD)
	JDBC = "jdbc"    
	DRIVER = "driver"
	DB_DRIVER = "com.teradata.jdbc.TeraDriver"
	URL = "url"
	TABLE = "dbtable"
	
	return sqlContext.read \
        .format(JDBC) \
        .option(DRIVER, DB_DRIVER) \
        .option(URL, CONNECT_URL) \
        .option(TABLE, table) \
        .load()


#database

#custbase
def custbase(data):
	custbase = data.toPandas()
	custbase.columns = ['customer_id','bonus_points','bonus_points_level','gender','consumption_level',\
                    'education','year_salary','utilization_rate','place','age']
	custbase.loc[:,"customer_id"] = custbase.loc[:,"customer_id"].apply(lambda x: str(x).strip())
	return custbase
	
def zorder_eachdata(data, bin_len = 3):
    data_len = len(data)
    zbin = [0] * data_len * bin_len
    
    ## integer to binary
    for i in range(data_len):
        bin = format(int(data[i]), "0" + str(bin_len) + "b")
        for j in range(bin_len):
            zbin[i + j * data_len] = int(bin[j])
    
    ## binary to integer
    zbin_len = len(zbin)
    zvalue = 0
    for i in range(zbin_len):
        zvalue += zbin[i] * (2 ** ((zbin_len - 1) - i))
        
    return zvalue

def zorder_dataset(data):
    ## normalization
    scaler = preprocessing.StandardScaler().fit(data)
    data_scale = scaler.transform(data)
    
    ## convert -4 ~ 3 to 0 ~ 7
    data_scale[data_scale < -3] = -4
    data_scale[data_scale >= 3] = 3
    data_scale = np.floor(data_scale) + 4
    
    z = []
    for i in range(data_scale.shape[0]):
        z.append(zorder_eachdata(data_scale[i, ]))
    
    return np.array(z)

def zorder_sampling(data, zorder, cluster_num=2):
    ## data sorted by z-order value
    data_sort = data[zorder.argsort()]
    
    ## cluster_dict will save sampling data
    cluster_dict = {}
    for i in range(cluster_num):
        remainder = [j % cluster_num for j in range(data_sort.shape[0])]
        position = np.where(map(lambda x: x == i, remainder))
        print position
        cluster_dict[i] = data_sort.iloc[position]
    
    return cluster_dict

def zorder_process(data_a, data_b, zorder):
    ## data sorted by z-order value
    zsampling = zorder_sampling(data_a, zorder, 10)
    #ensemble = pd.concat([zsampling[0],zsampling[1],zsampling[2],zsampling[3],zsampling[4],zsampling[5],zsampling[6],\
    #      zsampling[7],zsampling[8]])
    ensemble = pd.concat([zsampling[zsample] for zsample in range(9)])
    randomsample = zsampling[9]                 
    ensemble['algo'] = 'ens' 
    randomsample['algo'] = 'popular' 
    ensemble = ensemble.drop(ensemble.columns[1:-1],axis=1)
    randomsample = randomsample.drop(randomsample.columns[1:-1],axis=1)
    total_algo = pd.concat([data_b,ensemble, randomsample])
    total_algo.to_csv('myreward_algo.csv', encoding='utf-8', index=False)
    
    return total_algo
	
# calculate z-order value and write csv
def zorder(csv, data):	
	def pre_zorder(csv, data):
		df = None
	
		if os.path.exists(csv):
			df = pd.read_csv(csv)
		else:
			df = pd.DataFrame(columns=['customer_id', 'algo'])
			zorder_wanted = ['bonus_points','bonus_points_level','gender','consumption_level','education','age']
			zorder = zorder_dataset(data.ix[:,zorder_wanted].values)
			df = zorder_process(data.ix, df, zorder)
			
		return df
		
	def second_zorder(df, csv, data):
	## calculate z-order value
		if data['customer_id'][~data['customer_id'].isin(list(df['customer_id'].values))].any() !=0:
				zorder_wanted = ['bonus_points','bonus_points_level','gender','consumption_level','education','age']
				zorder = zorder_dataset(data.ix[:,zorder_wanted][~data['customer_id'].isin(list(df['customer_id'].values))].values)
				df = zorder_process(data.ix, df, zorder)
		else :
			pass	
		
		return df	
	
	myreward_algo = pre_zorder(csv, data)
	myreward_algo = second_zorder(myreward_algo, csv, data)
		
	return myreward_algo
	
	
		
#origin_att	
def origin_att(data):
	origin_att = data.toPandas()
	origin_att.columns = ['customer_id','item_id','cnt']
	origin_att.loc[:,"customer_id"] = origin_att.loc[:,"customer_id"].apply(lambda x: str(x).strip())
	origin_att = origin_att.groupby(['customer_id','item_id']).sum().reset_index().groupby('customer_id').head(1)
	origin_att = origin_att.drop(['cnt'],axis=1)

	return origin_att
	
#TXN pivot
def TXN(data):
	TXN = data.groupBy('customer_id').pivot('Consumption_Category').count().na.fill(0)
	TXN = TXN.toPandas()
	
	return TXN