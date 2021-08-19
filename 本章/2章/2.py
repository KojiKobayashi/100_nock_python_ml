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
'''
14th nock
月別推移の可視化
'''

# %%
import matplotlib.pyplot as pyplot
%matplotlib inline
month_data.sum().plot()

# %%

month_data.mean().plot()
# %%
'''
15th nock
'''

# %%
# ヒストグラム作成
pyplot.hist(analyze_data['total_amount'])

# %%
pyplot.hist(analyze_data['total_amount'], bins=21)

# %%
'''
16th nock
'''

# %%
# 都道府県と月別売り上げでクロス集計作成
pre_data = pd.pivot_table(analyze_data, index='order_accept_month', columns='narrow_area', values='total_amount', aggfunc='mean')
pre_data

# %%
import japanize_matplotlib

# %%
print(pre_data.columns)
for area in pre_data.columns:
    print(area)
    pyplot.plot(list(pre_data.index), pre_data[area], label=area)
pyplot.legend()

# %%
'''
17th nock
店舗別集計
'''

# %%
store_clustering = analyze_data.groupby('store_id').agg(['size', 'mean', 'median', 'max', 'min'])['total_amount']
store_clustering.reset_index(inplace=True, drop=True)
print(len(store_clustering))
store_clustering.head()

# %%
import seaborn as sns
hexbin = sns.jointplot(x='mean', y='size', data=store_clustering, kind='hex')

# %%
analyze_data.dtypes
# %%
'''
18th nock
'''

# %%
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# %%
# 標準化
sc = StandardScaler()
store_clustering_sc = sc.fit_transform(store_clustering)

# クラスタリング
kmeans = KMeans(n_clusters=4, random_state=0)
clusters = kmeans.fit(store_clustering_sc)
store_clustering['cluster'] = clusters.labels_
print(store_clustering['cluster'].unique())
store_clustering.head()

# %%
'''
19th nock
'''

# %%
store_clustering.columns = ['月内売り上げ', '月内平均値', '月内中央値', '月内最大値', '月内最小値', 'cluster']
store_clustering.groupby('cluster').count()

# %%
store_clustering.groupby('cluster').mean()

# %%
'''
20th nock
'''
# %%
from sklearn.manifold import TSNE
tsne = TSNE(n_components=2, random_state=0)
x = tsne.fit_transform(store_clustering_sc)
tsne_df = pd.DataFrame(x)
tsne_df['cluster'] = store_clustering['cluster']
tsne_df.columns = ['axis_0', 'axis_1', 'cluster']
tsne_df.head()

# %%
tsne_graph = sns.scatterplot(x = 'axis_0', y='axis_1', hue='cluster', data=tsne_df)
# %%
