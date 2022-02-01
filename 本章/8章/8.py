''' 71th nock '''
# %%
import os
import tarfile

os.chdir(os.path.join('本章', '8章'))
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
