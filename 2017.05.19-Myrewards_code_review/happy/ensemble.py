# coding: utf-8
from __future__ import unicode_literals
from __future__ import division

import os
import pandas as pd
import numpy as np
import logging
import itertools


from collections import defaultdict, OrderedDictndardScaler

# ensemble
def ensemble(data_a, data_b):
    als_prod = data_a.set_index('customer_id').T.to_dict('list')

    poi_cust_prod = {}
    for people_id, items in als_prod.items():
        key = len(items[0])
        poi_cust_prod.setdefault(people_id, [])
        poi_cust_prod[people_id].extend(zip(items[0], list(reversed(range(key)))))

    poi_dnew_fin = {}
    for people_id, items in data_b.items():
        key = len(items)
        poi_dnew_fin.setdefault(people_id, [])
        poi_dnew_fin[people_id].extend(zip(items, list(reversed(range(key)))))

    d = defaultdict(list)
    for a, b in poi_dnew_fin.items() + poi_cust_prod.items():
        d[a].extend(b)

    AA = {}
    for people, items in d.items():
        result = {}
        # AA[people]=result
        for i, s in items:
            result.setdefault(i, 0)
            result[i] += s
        AA[people] = result

    ensemble_prod = {}
    for people, items in AA.items():
        ensemble_prod.setdefault(people, []).append(
            [k for k, v in sorted(items.items(), key=lambda x: x[1], reverse=True)][:20])

    return ensemble_prod


# merge Algo
def combine_algo(data, a):
    final_people_prod = pd.DataFrame.from_dict(data, orient='index')
    final_people_prod = final_people_prod.drop(final_people_prod.columns[1:], axis=1)
    final_people_prod.reset_index(inplace=True)
    final_people_prod = final_people_prod.rename(columns={'index': 'customer_id', 0: 'ens_recommended_products'})
    final_people_prod["customer_id"] = final_people_prod["customer_id"].apply(lambda x: str(x).strip())
    final_people_prod = pd.merge(final_people_prod, myreward_algo, how='left', on='customer_id')

    popular = a.toPandas()
    row = popular.groupby('item_id').sum().reset_index().sort_values(['cnt'], ascending=[False])[:20]['item_id']. \
        apply(lambda x: str(x)).values
    EE = OrderedDict()
    for i in range(len(final_people_prod['customer_id'])):
        name = final_people_prod['customer_id'].iloc[i]
        EE.setdefault(name, []).append(row)

    popular = pd.DataFrame.from_dict(EE, orient='index')
    popular = popular.drop(popular.columns[1:], axis=1)
    popular.reset_index(inplace=True)
    popular = popular.rename(columns={'index': 'customer_id', 0: 'popular_recommended_products'})
    popular["customer_id"] = popular["customer_id"].apply(lambda x: str(x).strip())
    final_people_prod = pd.merge(final_people_prod, popular, how='left', on='customer_id')

    final_people_prod['final_recommended_products'] = final_people_prod['ens_recommended_products'].copy()
    final_people_prod.loc[final_people_prod['algo'] != 'ens', 'final_recommended_products'] = final_people_prod[
        'popular_recommended_products']

    rec = pd.DataFrame([list(x) for x in final_people_prod['final_recommended_products']])
    final_people_prod = pd.concat([final_people_prod['customer_id'], rec], axis=1)
    final_people_prod = final_people_prod.sort_values(['customer_id'])
    final_people_prod.to_csv('final_people_prod.csv', encoding='utf-8', index=False)
    return final_people_prod

# final_people_prod.to_csv('final_people_prod.csv',encoding='utf-8',index=False)






