# %%
import pandas as pd

# %%

'''
この時点ですでにアラートが出る

python3.7/site-packages/pandas/compat/__init__.py:117: UserWarning: Could not import the lzma module. Your installed Python is incomplete. Attempting to use lzma compression will result in a RuntimeError.
  warnings.warn(msg)
python 3.7.11, pandas 1.0.5
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
