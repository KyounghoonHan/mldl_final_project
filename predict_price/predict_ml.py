    # views.py or views.py 옆의 py 파일
    # models.load('./predict_price/saved_models' + 'saved_model.pkl')
    # './predict_price/data/~~~.csv'
    
from os import pipe
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.pipeline import Pipeline
from sklearn.tree import ExtraTreeRegressor

from catboost import CatBoostRegressor
from lightgbm import LGBMRegressor
from xgboost import XGBRegressor

from vecstack import StackingTransformer

import joblib

def prediction(value_gu, value_dong, value_apt, value_size, value_floor, value_cstr_year, value_built_year, value_brand_score, value_trade_index, value_sell):
    
    data = {
        '자치구명': [value_gu],
        '법정동명': [value_dong],
        '신고년도': [value_sell],
        '건물면적': [value_size],
        '층정보': [value_floor],
        '건축년도': [value_cstr_year],
        '건물명': [value_apt],
        '경과년도': [value_built_year],
        '브랜드점수': [value_brand_score],
        '매매지수': [value_trade_index]
    }
    
    input_data = pd.DateFrame(data)
    
    base_url = './predict_price/saved_models'
    model_url = base_url + 'model_apart_dobong.pkl'
    pipeline_url = base_url + 'pipeline.pkl'
    
    pipeline_loaded = joblib.load(pipeline_url)
    input_data_transformed = pipeline_loaded.transform(input_data)
        
    model_loaded = joblib.load(model_url)
    result = model_loaded.predict(input_data_transformed)
    
    return result