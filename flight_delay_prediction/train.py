# Flight Delay prediction

# Import required libraries
import numpy as np
import pandas as pd
import opendatasets as od
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
from sklearn.metrics import roc_auc_score, accuracy_score, precision_score, recall_score, f1_score, make_scorer
import bentoml
import json

# Download dataset
dataset_url = 'https://www.kaggle.com/datasets/deepankurk/flight-take-off-data-jfk-airport'
od.download(dataset_url)

# Load data
df = pd.read_csv('flight-take-off-data-jfk-airport/M1_final.csv')

# change few column names
column_names = {"OP_UNIQUE_CARRIER":"CARRIER_CODE",
                "TAIL_NUM":"FLIGHT_NO",
                "CRS_ELAPSED_TIME":"SCHEDULED_DURATION",
                "CRS_DEP_M":"SCHEDULED_DEPARTURE",
                "DEP_TIME_M":"ACTUAL_DEP_TIME",
                "CRS_ARR_M":"SCHEDULED_ARRIVAL",
                "sch_dep":"FLT_SCH_ARRIVAL",
                "sch_arr":"FLT_SCH_DEPARTURE"
               }

df = df.rename(column_names, axis=1)

# Change column names and objects to lowercase, repalce sapces with _
df.columns = df.columns.str.lower().str.replace(' ', '_')

categorical_columns = list(df.dtypes[df.dtypes == 'object'].index)

for c in categorical_columns:
    df[c] = df[c].str.lower().str.replace(' ', '_')

# Drop rows with missing values
df.dropna(inplace=True)

# change dtype to int
df.dew_point = df.dew_point.astype('int64')

# convert 'dep_delay' into bianry 0 and 1  -- above 15 minutes is 1, below is 0
df_processed = df.copy()
df_processed['is_delayed'] = df_processed['dep_delay'].map(lambda x: 1 if x >= 15 else 0)
df_processed = df_processed.drop('dep_delay', axis=1)
df_processed = df_processed.drop('flight_no', axis=1)

# Train-val-test split
df_full_train, df_test = train_test_split(df_processed, stratify=df_processed['is_delayed'], test_size=0.2, random_state=42)
df_train, df_val = train_test_split(df_full_train, stratify=df_full_train['is_delayed'], test_size=0.25, random_state=42)

df_train = df_train.reset_index(drop=True)
df_val = df_val.reset_index(drop=True)
df_test = df_test.reset_index(drop=True)

y_train = df_train['is_delayed'].values
y_val = df_val['is_delayed'].values
y_test = df_test['is_delayed'].values

# drop 'is_delayed' from datasets
df_train = df_train.drop('is_delayed', axis=1)
df_val = df_val.drop('is_delayed', axis=1)
df_test = df_test.drop('is_delayed', axis=1)

categorical_columns = ['carrier_code', 'dest', 'wind', 'condition']
numerical_columns = ['month', 'day_of_month', 'day_of_week', 'scheduled_duration', 'distance', 'scheduled_departure', 'actual_dep_time', 'scheduled_arrival', 'temperature', 'dew_point', 'humidity', 'wind_speed', 'wind_gust', 'pressure', 'flt_sch_arrival', 'flt_sch_departure', 'taxi_out']

# one hot encoding
train_dict = df_train[categorical_columns + numerical_columns].to_dict(orient='records')
dv = DictVectorizer(sparse=False)
dv.fit(train_dict)
X_train = dv.fit_transform(train_dict)

val_dict = df_val[categorical_columns + numerical_columns].to_dict(orient='records')
X_val = dv.transform(val_dict)

test_dict = df_test[categorical_columns + numerical_columns].to_dict(orient='records')
X_test = dv.transform(test_dict)

# Train final model - XGBoost
dtrain = xgb.DMatrix(X_train, label=y_train)
xgb_params = {
    'eta': 0.1, 
    'max_depth': 3,
    'min_child_weight': 1,

    'objective': 'binary:logistic',
    'eval_metric': 'auc',

    'nthread': 8,
    'seed': 1,
    'verbosity': 1,
}
xgb_model = xgb.train(xgb_params, dtrain, num_boost_round=175)

# save xgboost model with BentoML
bentoml.xgboost.save_model(
    'flight_delay_prediction_model',
    xgb_model,
    custom_objects={
        'dictVectorizer': dv
    },
    signatures={
        "predict": {
            "batchable": True,
            "batch_dim": 0
        }
    }
)

# Get one row from df_test in JSON format for testing
request = df_test.iloc[100].to_dict()
print(json.dumps(request, indent=2))