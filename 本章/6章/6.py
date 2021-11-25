# %%
''' 51th nock '''
import os
data_dir = 'data'
input_dir = os.path.join(data_dir, '0_input')
ouput_dir = os.path.join(data_dir, '1_output')
master_dir = os.path.join(data_dir, '99_master')
os.makedirs(input_dir, exist_ok=True)
os.makedirs(ouput_dir, exist_ok=True)
os.makedirs(master_dir, exist_ok=True)

# ここで 0 に注文データ、99 にマスターデータをコピーしておく
# %%
''' 52th knock '''
import glob
tbl_order_file = os.path.join(input_dir, 'tbl_order_*.csv')
tbl_order_paths = glob.glob(tbl_order_file)
tbl_order_paths

# %%
''' 52th knock '''
import pandas as pd
m_area_file = 'm_area.csv'
m_store_file = 'm_store.csv'
m_area = pd.read_csv(os.path.join(master_dir, m_area_file))
m_store = pd.read_csv(os.path.join(master_dir, m_store_file))
m_area.head(3)

# %%
tbl_order_path = tbl_order_paths[0]
print(f'読み込みデータ:{tbl_order_path}')
order_data = pd.read_csv(tbl_order_path)
print(f'データ件数:{len(order_data)}')
order_data.head(3)  # fileの順番が本と違うので、出力も差異あり

# %%
''' 53 th knock '''
order_data = order_data.loc[order_data['store_id'] != 999]
order_data = pd.merge(order_data, m_store, on='store_id', how='left')
order_data = pd.merge(order_data, m_area, on='area_cd', how='left')
order_data.loc[order_data['takeout_flag'] == 0, 'takeout_name'] = 'デリバリー'
order_data.loc[order_data['takeout_flag'] == 1, 'takeout_name'] = 'お持ち帰り'
order_data.loc[order_data['status'] == 0, 'status_name'] = '受付'
order_data.loc[order_data['status'] == 1, 'status_name'] = 'お支払済'
order_data.loc[order_data['status'] == 2, 'status_name'] = 'お渡し済'
order_data.loc[order_data['status'] == 9, 'status_name'] = 'キャンセル'
order_data.head(3)

# %%
# 欠損地カウント
order_data.isna().sum()

# %%
''' 54 th nock '''
# 受け取りまでの時間計算
def cal_delta(t):
    t1, t2 = t
    delta = t2 - t1
    return delta.total_seconds()/60

order_data.loc[:, 'order_accept_datetime'] = pd.to_datetime(order_data['order_accept_date'])
order_data.loc[:, 'delivered_datetime'] = pd.to_datetime(order_data['delivered_date'])
order_data.loc[:, 'delta'] = order_data[['order_accept_datetime', 'delivered_datetime']].apply(cal_delta, axis=1)
order_data.head(3)


# %%
# 休日平日
order_data.loc[:, 'order_accept_hour'] = order_data['order_accept_datetime'].dt.hour
order_data.loc[:, 'order_accept_weekday'] = order_data['order_accept_datetime'].dt.weekday
order_data.loc[order_data['order_accept_weekday'] >= 5, 'weekday_info'] = '休日' 
order_data.loc[order_data['order_accept_weekday'] < 5, 'weekday_info'] = '平日'
order_data.head(3)

# %%
# 55th knock
store_data = order_data.groupby(['store_name']).count()[['order_id']]
store_f = order_data.loc[(order_data['status_name']=='お渡し済') | (order_data['status_name']=='お支払済')].groupby(['store_name']).count()[['order_id']]
store_c = order_data.loc[order_data['status_name']=='キャンセル'].groupby(['store_name']).count()[['order_id']]
store_d = order_data.loc[order_data['takeout_name']=='デリバリー'].groupby(['store_name']).count()[['order_id']]
store_t = order_data.loc[order_data['takeout_name']=='お持ち帰り'].groupby(['store_name']).count()[['order_id']]
store_weekday = order_data[order_data['weekday_info']=='平日'].groupby(['store_name']).count()[['order_id']]
store_weekend = order_data[order_data['weekday_info']=='休日'].groupby(['store_name']).count()[['order_id']]

# %%
times = order_data['order_accept_hour'].unique()
store_time = []
for time in times:
    tmp = order_data.loc[order_data['order_accept_hour']==time].groupby(['store_name']).count()[['order_id']]
    tmp.columns = [f'order_time_{time}']
    store_time.append(tmp)
store_time[0:3]

# %%
store_time = pd.concat(store_time, axis=1)   # 横に連結
store_time.head(3)

# %%
store_delta = order_data.loc[order_data['status_name']!='キャンセル'].groupby(['store_name']).mean()[['delta']]
store_delta

# %%
store_data.columns = ['order']
store_f.columns = ['order_fin']
store_c.columns = ['order_cancel']
store_d.columns = ['order_delivery']
store_t.columns = ['order_takeout']
store_weekday.columns = ['order_weekday']
store_weekend.columns = ['order_weekend']
store_delta.columns = ['delta_avg']

#%%
store_data = pd.concat([store_data, store_f, store_c, store_d, store_t, store_weekday, store_weekend, store_time, store_delta], axis=1)
store_data.head(3)

# %%
''' 56th knock '''

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

    order_data.loc[:, 'order_accept_datetime'] = pd.to_datetime(order_data['order_accept_date'])
    order_data.loc[:, 'delivered_datetime'] = pd.to_datetime(order_data['delivered_date'])
    order_data.loc[:, 'delta'] = order_data[['order_accept_datetime', 'delivered_datetime']].apply(cal_delta, axis=1)

    order_data.loc[:, 'order_accept_hour'] = order_data['order_accept_datetime'].dt.hour
    order_data.loc[:, 'order_accept_weekday'] = order_data['order_accept_datetime'].dt.weekday
    order_data.loc[order_data['order_accept_weekday'] >= 5, 'weekday_info'] = '休日' 
    order_data.loc[order_data['order_accept_weekday'] < 5, 'weekday_info'] = '平日'

    store_data = order_data.groupby(['store_name']).count()[['order_id']]
    store_f = order_data.loc[(order_data['status_name']=='お渡し済') | (order_data['status_name']=='お支払済')].groupby(['store_name']).count()[['order_id']]
    store_c = order_data.loc[order_data['status_name']=='キャンセル'].groupby(['store_name']).count()[['order_id']]
    store_d = order_data.loc[order_data['takeout_name']=='デリバリー'].groupby(['store_name']).count()[['order_id']]
    store_t = order_data.loc[order_data['takeout_name']=='お持ち帰り'].groupby(['store_name']).count()[['order_id']]
    store_weekday = order_data[order_data['weekday_info']=='平日'].groupby(['store_name']).count()[['order_id']]
    store_weekend = order_data[order_data['weekday_info']=='休日'].groupby(['store_name']).count()[['order_id']]

    times = order_data['order_accept_hour'].unique()
    store_time = []
    for time in times:
        tmp = order_data.loc[order_data['order_accept_hour']==time].groupby(['store_name']).count()[['order_id']]
        tmp.columns = [f'order_time_{time}']
        store_time.append(tmp)
    store_time = pd.concat(store_time, axis=1)   # 横に連結

    store_delta = order_data.loc[order_data['status_name']!='キャンセル'].groupby(['store_name']).mean()[['delta']]

    store_data.columns = ['order']
    store_f.columns = ['order_fin']
    store_c.columns = ['order_cancel']
    store_d.columns = ['order_delivery']
    store_t.columns = ['order_takeout']
    store_weekday.columns = ['order_weekday']
    store_weekend.columns = ['order_weekend']
    store_delta.columns = ['order_avg']
    store_data = pd.concat([store_data, store_f, store_c, store_d, store_t, store_weekday, store_weekend, store_time, store_delta], axis=1)

    return store_data

# %%
order_data = pd.read_csv(tbl_order_path)
store_data = data_processing(order_data)
store_data.head(3)

# %%
''' 57th knock'''
store_all = []
for tbl_order_path in tbl_order_paths:
    print(f'{tbl_order_path}')
    tg_ym = tbl_order_path.split('_')[-1][:6]
    order_data = pd.read_csv(tbl_order_path)
    store_data = data_processing(order_data)
    store_data.loc[:, 'year_month'] = tg_ym
    store_data.reset_index(drop=False, inplace=True)
    store_all.append(store_data)
store_all = pd.concat(store_all, ignore_index=True)
display(store_all.head(3))
display(store_all.tail(3))
store_monthly_name = 'store_monthly_data.csv'
store_all.to_csv(os.path.join(ouput_dir, store_monthly_name), index=False)

# %%
''' 58th knock '''
# 一か月前との差をとって目的変数とする
y = store_all[['store_name', 'year_month', 'order_weekday', 'order_weekend']].copy()
y.loc[:, 'one_month_ago'] = pd.to_datetime(y['year_month'], format='%Y%m')
from dateutil.relativedelta import relativedelta
y.loc[:, 'one_month_ago'] = y['one_month_ago'].map(lambda x: x - relativedelta(months=1))
y.loc[:, 'one_month_ago'] = y['one_month_ago'].dt.strftime('%Y%m')
y.head(3)

# %%
y_one_month = y.copy()
y_one_month.rename(columns={'order_weekday':'order_weekday_one_month_ago'}, inplace=True)
y_one_month.rename(columns={'order_weekend':'order_weekdend_one_month_ago'}, inplace=True)
# 元票の一か月前とこのjoin用カラムを結合キーとして一か月ずらす
y_one_month.rename(columns={'year_month':'year_month_for_join'}, inplace=True)
# left_on, right_on でキーの違う列を結合できる
y = pd.merge(y,y_one_month[['store_name', 'year_month_for_join', 'order_weekday_one_month_ago', 'order_weekdend_one_month_ago']]
    , left_on=['store_name', 'one_month_ago'], right_on=['store_name', 'year_month_for_join'], how='left')
y.loc[y['store_name'] == 'あきる野店']

# %%
y.dropna(inplace=True)
y.loc[y['order_weekday'] - y['order_weekday_one_month_ago']>0, 'y_weekday'] = 1
y.loc[y['order_weekday'] - y['order_weekday_one_month_ago']<=0, 'y_weekday'] = 0
y.loc[y['order_weekend'] - y['order_weekdend_one_month_ago']>0, 'y_weekend'] = 1
y.loc[y['order_weekend'] - y['order_weekdend_one_month_ago']<=0, 'y_weekend'] = 0
y.head(3)

# %%
