import happy.preprocess as hp
import happy.algorithm as ha
import happy.ensemble as he


item_point= hp.td_spark("myrewards_new_product").select("item_id", "item_level")

#custbase
cust = hp.td_spark("myrewards_new_custbase")

#redeem most popular
redeem_most = hp.td_spark("myrewards_new_att").select("customer_id" ,"item_id","cnt")

#ALS user
ALS_exp = hp.td_spark("myrewards_new_exp").select("customer_id" ,"item_id","cnt")	

#ALS user points
ALS_exp_points = hp.td_spark("myrewards_new_exp").select("customer_id" ,"item_id","cnt","bonus_points_Level")

#credit card record
credit = hp.td_spark("myrewards_new_cctxn")


#read custbase
custbase = hp.custbase(cust)	
print custbase

#segment by zorder
myreward_algo = hp.zorder('myreward_algo.csv',custbase)
print myreward_algo
 
#read redeem most product
origin_att = hp.origin_att(redeem_most)
print (origin_att) 

#read credit card record
TXN = hp.TXN(credit)
print (TXN) 

#add prediction Y
origin_att_y = ha.merge_product(TXN , origin_att,'inner')
print origin_att_y

#add all user file
final_train = ha.final_data(custbase , origin_att_y , 'inner')
print final_train
 
#record used column
final_col = ha.record(final_train)
print final_col 
 
 
#training data
xgb_best = ha.xgb_train(final_train)
print xgb_best



#all user
final_all = ha.final_data(custbase , TXN , 'left')
print final_all
 
#Xgb filter
xgb_filter_item ,dct = ha.xgb_filter_all(final_all, final_col, final_train,item_point, xgb_best)
print xgb_filter_item ,dct

#Als train model
final_model , customer_list , item_list =  ha.als_process(ALS_exp)
print customer_list

#Als used broadcast
broad_CustIds, broad_ItemIds, broad_ItemLevels, bCust, broad_UserLevels = ha.als_mapping(ALS_exp_points, customer_list, item_list, dct)

#Als filter	
als_filter_item = ha.als_filter_all(final_model , 200)

#ensemble top20
ensemble_item = he.ensemble(als_filter_item, xgb_filter_item)
print ensemble_item

#final_recommended_products
final_people_item = he.combine_algo(ensemble_item, redeem_most)
print final_people_item.head()

