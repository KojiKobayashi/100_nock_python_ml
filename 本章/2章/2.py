# %%
'''
11th nock
'''

# %%
import pandas as pd
order_data = pd.read_csv('order_data.csv')
print(len(order_data))
order_data.head()

# %%
# status=0 は受付、9はキャンセル
order_data = order_data.loc[(order_data['status'] == 1) | (order_data['status'] == 2)]
print(len(order_data))
order_data.columns

# %%
# 不要な項目削除
analyze_data = order_data[['store_id', 'customer_id', 'coupon_cd', 'order_accept_date', 'delivered_date', 'total_amount', 'store_name', 'wide_area', 'narrow_area', 'takeout_name', 'status_name']]
print(analyze_data.shape)
analyze_data.head()

# %%
'''
12th nock
'''

# %%
analyze_data.describe()

# %%
analyze_data.dtypes
# %%
# 扱わないのは数字に変換しておく
# warning でる。元データの order_data を変えるべき
analyze_data[['store_id', 'coupon_cd']] = analyze_data[['store_id', 'coupon_cd']].astype(str)

# %%
# warning 抑止
import warnings
warnings.filterwarnings('ignore')

# %%
analyze_data.describe()

# %%
'''
13th nock
月別の売り上げを集計
'''

# %%
analyze_data['order_accept_date'] = pd.to_datetime(analyze_data['order_accept_date'])
analyze_data['order_accept_month'] = analyze_data['order_accept_date'].dt.strftime('%Y%m')
analyze_data[['order_accept_date', 'order_accept_month']].head()

# %%
analyze_data['delivered_date'] = pd.to_datetime(analyze_data['delivered_date'])
analyze_data['delivered_month'] = analyze_data['delivered_date'].dt.strftime('%Y%m')
analyze_data[['delivered_date', 'delivered_month']].head()

# %%
analyze_data.dtypes

# %%
# 月別統計
month_data = analyze_data.groupby('order_accept_month')
month_data.describe()

# %%
month_data.sum()
# %%
