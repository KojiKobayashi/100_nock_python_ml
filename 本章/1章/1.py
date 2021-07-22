# %%
import pandas as pd

# %%

'''
この時点ですでにアラートが出る

python3.7/site-packages/pandas/compat/__init__.py:117: UserWarning: Could not import the lzma module. Your installed Python is incomplete. Attempting to use lzma compression will result in a RuntimeError.
  warnings.warn(msg)
python 3.7.11, pandas 1.0.5

このときは一旦pythonを uninstall して
sudo apt-get install liblzma-dev
して再インストール
'''

# %%
m_stores = pd.read_csv('m_store.csv')
m_stores

# %%
len(m_stores)

# %%
m_stores.head()

# %%

m_area = pd.read_csv('m_area.csv')
m_area

# %%
tbl_order4 = pd.read_csv('tbl_order_202004.csv')
tbl_order4

# %%
'''
nock 2
'''

# %%
tbl_order5 = pd.read_csv('tbl_order_202005.csv')
tbl_order5

# %%
order_all = pd.concat([tbl_order4, tbl_order5], ignore_index=True)
order_all

# %%
len(tbl_order4) + len(tbl_order5) == len(order_all)

# %%
'''
3rd nock
'''

# %%
import os
current_dir = os.getcwd()
current_dir

# %%
os.listdir(current_dir)

# %%
tbl_order_file = os.path.join(current_dir, 'tbl_order_*.csv')
tbl_order_file

# %%
import glob
tbl_order_files = glob.glob(tbl_order_file)
tbl_order_files

# %%
'''
4th nock
'''

#%%
order_all = pd.DataFrame()
file = tbl_order_files[0]
order_data = pd.read_csv(file)
print(f'{file}:{len(order_data)}')
order_all = pd.concat([order_all, order_data], ignore_index=True)
order_all

# %%
order_all = pd.DataFrame()
for file in tbl_order_files:
  order_data = pd.read_csv(file)
  print(f'{file}:{len(order_data)}')
  order_all = pd.concat([order_all, order_data], ignore_index=True)
order_all

# %%
# 欠損値のカウント
order_all.isnull().sum()

# %%
order_all.describe()

# %%
order_all['total_amount'].describe()

# %%
print(order_all['order_accept_date'].min())
print(order_all['order_accept_date'].max())
print(order_all['delivered_date'].min())
print(order_all['delivered_date'].max())

# %%


# %%
