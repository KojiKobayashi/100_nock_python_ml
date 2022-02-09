''' 71th nock '''
# %%
import os
from unicodedata import category

# os.chdir(os.path.join('本章', '8章'))
data_dir = 'data'
input_dir = os.path.join(data_dir, '0_input')
output_dir = os.path.join(data_dir, '1_input')
master_dir = os.path.join(data_dir, '99_master')
model_dir = 'models'
os.makedirs(input_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)
os.makedirs(master_dir, exist_ok=True)
os.makedirs(model_dir, exist_ok=True)

# %%
import pandas as pd

m_area_file = 'm_area.csv'
m_store_file = 'm_store.csv'
m_area = pd.read_csv(os.path.join(master_dir, m_area_file))
m_store = pd.read_csv(os.path.join(master_dir, m_store_file))

# %%
tg_ym = "202003"
target_file = "tbl_order_" + tg_ym + ".csv"
target_data = pd.read_csv(os.path.join(input_dir, target_file))

import datetime

max_date = pd.to_datetime(target_data["order_accept_date"]).max()
min_date = pd.to_datetime(target_data["order_accept_date"]).min()
max_str_date = max_date.strftime("%Y%m")
min_str_date = min_date.strftime("%Y%m")
if tg_ym == min_str_date and tg_ym == max_str_date:
    print("日付が一致しました")
else:
    raise Exception("日付が一致しません")


# %%
def calc_delta(t):
    t1, t2 = t
    delta = t2 - t1
    return delta.total_seconds()/60

#%%
order_data = target_data.loc[target_data['store_id'] != 999]
order_data = pd.merge(order_data, m_store, on='store_id', how='left')
store_data = order_data.groupby(['store_name']).count()[['order_id']]
store_data.columns = ['order']
store_data
# %%
def data_processing(order_data):
    order_data = order_data.loc[order_data['store_id'] != 999]
    order_data = pd.merge(order_data, m_store, on='store_id', how='left')
    order_data = pd.merge(order_data, m_area, on='area_cd', how='left')
    order_data.loc[order_data['takeout_flag'] == 0, 'takeout_name'] = 'デリバリー'
    order_data.loc[order_data['takeout_flag'] == 1, 'takeout_name'] = 'お持ち帰り'
    order_data.loc[order_data['status'] == 0, 'status_name'] = '受付'
    order_data.loc[order_data['status'] == 1, 'status_name'] = 'お支払済'
    order_data.loc[order_data['status'] == 2, 'status_name'] = 'お渡し済'
    order_data.loc[order_data['status'] == 9, 'status_name'] = 'キャンセル'

    order_data.loc[:, 'order_accept_datetime'] = \
        pd.to_datetime(order_data['order_accept_date'])
    order_data.loc[:, 'delivered_datetime'] = \
        pd.to_datetime(order_data['delivered_date'])
    order_data.loc[:, 'delta'] = \
        order_data[['order_accept_datetime', 'delivered_datetime']] \
        .apply(calc_delta, axis=1)

    order_data.loc[:, 'order_accept_hour'] = \
        order_data['order_accept_datetime'].dt.hour
    order_data.loc[:, 'order_accept_weekday'] = \
        order_data['order_accept_datetime'].dt.weekday
    order_data.loc[order_data['order_accept_weekday'] >= 5, 'weekday_info'] \
        = '休日'
    order_data.loc[order_data['order_accept_weekday'] < 5, 'weekday_info'] \
        = '平日'

    store_data = order_data.groupby(['store_name']).count()[['order_id']]
    store_f = order_data.loc[
        (order_data['status_name'] == 'お渡し済')
        | (order_data['status_name'] == 'お支払済')
        ].groupby(['store_name']).count()[['order_id']]
    store_c = order_data.loc[
        order_data['status_name'] == 'キャンセル'].groupby(
            ['store_name']).count()[['order_id']]
    #store_d = order_data.loc[order_data['takeout_name'] == 'デリバリー'].groupby(
    #    ['store_name']).count()[['order_id']]
    store_d = order_data.loc[order_data['takeout_name']=="デリバリー"].groupby(['store_name']).count()[['order_id']]

    store_t = order_data.loc[order_data['takeout_name'] == 'お持ち帰り'].groupby(
        ['store_name']).count()[['order_id']]
    store_weekday = order_data[order_data['weekday_info'] == '平日'].groupby(
        ['store_name']).count()[['order_id']]
    store_weekend = order_data[order_data['weekday_info'] == '休日'].groupby(
        ['store_name']).count()[['order_id']]

    times = order_data['order_accept_hour'].unique()
    store_time = []
    for time in times:
        tmp = order_data.loc[
            order_data['order_accept_hour'] == time
            ].groupby(['store_name']).count()[['order_id']]
        tmp.columns = [f'order_time_{time}']
        store_time.append(tmp)
    store_time = pd.concat(store_time, axis=1)   # 横に連結

    store_delta = order_data.loc[
        order_data['status_name'] != 'キャンセル'
        ].groupby(['store_name']).mean()[['delta']]

    store_data.columns = ['order']
    store_f.columns = ['order_fin']
    store_c.columns = ['order_cancel']
    store_d.columns = ['order_delivery']
    store_t.columns = ['order_takeout']
    store_weekday.columns = ['order_weekday']
    store_weekend.columns = ['order_weekend']
    store_delta.columns = ['order_avg']
    store_data = pd.concat([store_data, store_f, store_c, store_d, store_t, 
                        store_weekday, store_weekend, store_time, store_delta], axis=1)
    return store_data
# %%
store_data = data_processing(target_data)
store_data.reset_index(drop=False, inplace=True)
actual_data = store_data.copy()

# %%
actual_data.head(5)

# %%
category_data = pd.get_dummies(store_data['store_name'], prefix='store', prefix_sep='_')
del category_data['store_麻生店']
store_data = pd.concat([store_data, category_data], axis=1)
store_data.head(3)
# %%
