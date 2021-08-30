# %%
'''
21th nock
'''

# %%
import pandas as pd
from IPython.display import display, clear_output
from pandas._config.config import options

# %%
m_store = pd.read_csv('m_store.csv')
m_area = pd.read_csv('m_area.csv')
order_data = pd.read_csv('tbl_order_202004.csv')
order_data = pd.merge(order_data, m_store, on='store_id', how='left')
order_data = pd.merge(order_data, m_area, on='area_cd', how='left')

# %%
order_data.loc[order_data['takeout_flag'] == 0, 'takeout_name'] = 'デリバリ－'
order_data.loc[order_data['takeout_flag'] == 1, 'takeout_name'] = 'お持ち帰り'

# %%
order_data.loc[order_data['status'] == 0, 'status_name'] = '受付'
order_data.loc[order_data['status'] == 1, 'status_name'] = 'お支払い'
order_data.loc[order_data['status'] == 2, 'status_name'] = 'お渡し済み'
order_data.loc[order_data['status'] == 9, 'status_name'] = 'キャンセル'
# %%
order_data.head()

# %%
from ipywidgets import Dropdown


def order_by_store(val):
    clear_output()
    display(dropdown)
    pick_data = order_data.loc[(order_data['store_name'] == val['new']) & order_data['status'.isin([1, 2])]]
    display(pick_data.head()) # VSCode の jupyter extension では無理


store_list = m_store['store_name'].to_list()
dropdown = Dropdown(options=store_list)
dropdown.observe(order_by_store, names='value')
display(dropdown)

# %%
%matplotlib inline
import matplotlib.pyplot as plt
import japanize_matplotlib

# %%
def graph_by_store(val):
    clear_output()
    display(dropdown2)
    pick_data = order_data.loc[
        (order_data['store_name'] == val['new'])
        & [order_data['status'].isin([1,2])]
    ]
    temp = pick_data[['order_accept_data', 'total_amount'].copy()]
    temp.loc[:, 'order_accept_date'] = pd.to_datetime(temp['order_accept_date'])
    temp.set_index('order_accept_date', inplace=True)
    temp.resample('D').sum().plot()　# VSCode の jupyter extension では無理

dropdown2 = Dropdown(options = store_list)
dropdown2.observe(graph_by_store, names='value')
display(dropdown2)

# %%
# ipywidgets は ブラウザじゃないと厳しいらしいので三章はとばす