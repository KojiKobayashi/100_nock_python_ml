# %%
''' 61th '''

# %%
import os

from scipy.sparse.construct import diags, random

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
X_cols = list(train_data.columns)
X_cols.remove('y_weekday')
X_cols.remove('y_weekend')
target_y = 'y_weekday'
y_train = train_data[target_y]
X_train = train_data[X_cols]
y_test = test_data[target_y]
X_test = test_data[X_cols]
display(y_train.head(3))
display(X_train.head(3))
# %%

from sklearn.tree import DecisionTreeClassifier

model = DecisionTreeClassifier(random_state=0)
model.fit(X_train, y_train)

# %%
y_pred_train = model.predict(X_train)
y_pred_test = model.predict(X_test)
y_pred_test

# %%
from sklearn.metrics import (accuracy_score, confusion_matrix, f1_score,
                             precision_score, recall_score)

acc_train = accuracy_score(y_train, y_pred_train)
acc_test = accuracy_score(y_test, y_pred_test)
f1_train = f1_score(y_train, y_pred_train)
f1_test = f1_score(y_test, y_pred_test)
recall_train  = recall_score(y_train, y_pred_train)
recall_test  = recall_score(y_test, y_pred_test)
precision_train  = precision_score(y_train, y_pred_train)
precision_test  = precision_score(y_test, y_pred_test)

print(f'acc       train:{round(acc_train,2)} test:{round(acc_test,2)}')
print(f'f1        train:{round(f1_train,2)} test:{round(f1_test,2)}')
print(f'racall    train:{round(recall_train,2)} test:{round(recall_test,2)}')
print(f'precision train:{round(precision_train,2)} test:{round(precision_test,2)}')

# %%
print(confusion_matrix(y_train, y_pred_train))
print(confusion_matrix(y_test, y_pred_test))

# %%
tn_train, fp_train, fn_train, tp_train = confusion_matrix(y_train, y_pred_train).ravel()
tn_test, fp_test, fn_test, tp_test = confusion_matrix(y_test, y_pred_test).ravel()
print(tn_train, fp_train, fn_train, tp_train)
print(tn_test, fp_test, fn_test, tp_test )

# %%
score_train = pd.DataFrame({'DataCategory':['train'],
    'acc':acc_train, 'f1':f1_train,
    'recall':recall_train, 'precision':precision_train,
    'tp':tp_train,'fn':fn_train,'fp':fp_train,'tn':tn_train})
score_test = pd.DataFrame({'DataCategory':['test'],
    'acc':acc_test, 'f1':f1_test,
    'recall':recall_test, 'precision':precision_test,
    'tp':tp_test,'fn':fn_test,'fp':fp_test,'tn':tn_test})
score = pd.concat([score_train, score_test], ignore_index=True)
score

# %%
importance = pd.DataFrame({'cols':X_train.columns, 'importance':model.feature_importances_})
importance = importance.sort_values('importance', ascending=False)
importance.head(10)

# %%
'''67th knock'''
def make_model_and_eval(model, X_train, X_test, y_train, y_test):
    model.fit(X_train, y_train)
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)

    acc_train = accuracy_score(y_train, y_pred_train)
    acc_test = accuracy_score(y_test, y_pred_test)
    f1_train = f1_score(y_train, y_pred_train)
    f1_test = f1_score(y_test, y_pred_test)
    recall_train  = recall_score(y_train, y_pred_train)
    recall_test  = recall_score(y_test, y_pred_test)
    precision_train  = precision_score(y_train, y_pred_train)
    precision_test  = precision_score(y_test, y_pred_test)

    tn_train, fp_train, fn_train, tp_train = confusion_matrix(y_train, y_pred_train).ravel()
    tn_test, fp_test, fn_test, tp_test = confusion_matrix(y_test, y_pred_test).ravel()

    score_train = pd.DataFrame({'DataCategory':['train'],
        'acc':acc_train, 'f1':f1_train,
        'recall':recall_train, 'precision':precision_train,
        'tp':tp_train,'fn':fn_train,'fp':fp_train,'tn':tn_train})
    score_test = pd.DataFrame({'DataCategory':['test'],
        'acc':acc_test, 'f1':f1_test,
        'recall':recall_test, 'precision':precision_test,
        'tp':tp_test,'fn':fn_test,'fp':fp_test,'tn':tn_test})
    score = pd.concat([score_train, score_test], ignore_index=True)

    importance = pd.DataFrame({'cols':X_train.columns, 'importance':model.feature_importances_})
    importance = importance.sort_values('importance', ascending=False)

    cols = pd.DataFrame({'X_cols':X_train.columns})

    display(score)
    return score, importance, model, cols
    

# %%
model = DecisionTreeClassifier(random_state=0)
score, importance, model, cols = make_model_and_eval(model, X_train, X_test, y_train, y_test)

# %%
''' 68th nock '''
import datetime

now = datetime.datetime.now().strftime("%Y%m%D%H%M%S")
target_output_dir_name = 'results_' + now
target_output_dir = os.path.join(output_dir, target_output_dir_name)
os.makedirs(target_output_dir, exist_ok=True)
print(target_output_dir)
# %%
score_name = 'score.csv'
importance_name = 'importance.csv'
cols_name = 'X_cols.csv'
model_name = 'model.pickle'
score_path = os.path.join(target_output_dir, score_name)
importance_path = os.path.join(target_output_dir, importance_name)
cols_path = os.path.join(target_output_dir, cols_name)
model_path = os.path.join(target_output_dir, model_name)

score.to_csv(score_path, index=False)
importance.to_csv(importance_path, index=False)
cols.to_csv(cols_path, index=False)
import pickle

with open(model_path, mode='wb') as f:
    pickle.dump(model, f, protocol=2)
# %%
