# %%
''' 61th '''

# %%
import os
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
