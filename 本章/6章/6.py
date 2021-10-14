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
order_data.head(3) # fileの順番が本と違うので、出力も差異あり

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
