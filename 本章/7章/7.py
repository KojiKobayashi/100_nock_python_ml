# %%
''' 61th '''

# %%
import os

from scipy.sparse.construct import random
data_dir = 'data'
input_dir = os.path.join(data_dir, '0_input')
output_dir = os.path.join(data_dir, '1_output')
os.makedirs(input_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

# here, copy csv to input dir.

# %%
import pandas as pd
ml_data_file = 'ml_base_data.csv'
ml_data = pd.read_csv(os.path.join(input_dir, ml_data_file))
ml_data.head(3)

# %%
''' 62th knock '''
# one hot encoding
category_data = pd.get_dummies(ml_data['store_name'], prefix='store', prefix_sep='_')
display(category_data.head(3))

# %%
# 多重共線性のため一つ店を消す（これ本当に一般的なのか？）
del category_data['store_麻生店']
del ml_data['year_month']
del ml_data['store_name']
ml_data = pd.concat([ml_data, category_data], axis=1)
ml_data.columns

# %%
from sklearn.model_selection import train_test_split
train_data, test_data = train_test_split(ml_data, test_size=0.3, random_state=0)
print(f'Train count:{len(train_data)}/ Test count:{len(test_data)}')
print(f'Weekday Train0: {len(train_data.loc[train_data["y_weekday"]==0])}')
print(f'Weekday Train1: {len(train_data.loc[train_data["y_weekday"]==1])}')
print(f'Weekday Test0: {len(test_data.loc[test_data["y_weekday"]==0])}')
print(f'Weekday Test1: {len(test_data.loc[test_data["y_weekday"]==1])}')
print(f'Weekend Train0: {len(train_data.loc[train_data["y_weekend"]==0])}')
print(f'Weekend Train1: {len(train_data.loc[train_data["y_weekend"]==1])}')
print(f'Weekend Test0: {len(test_data.loc[test_data["y_weekend"]==0])}')
print(f'Weekend Test1: {len(test_data.loc[test_data["y_weekend"]==1])}')
# %%
