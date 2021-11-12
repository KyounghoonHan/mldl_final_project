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

def selected_apt_avg(value_gu, value_dong, value_apt):

    mapping  = ["도봉구", "동대문구", "동작구", "은평구", "강북구", "강동구", "강남구", "강서구", "금천구", "구로구", "관악구", "광진구",
                "종로구", "중구", "중랑구", "마포구", "노원구", "서초구", "서대문구", "성북구", "송파구", "성동구", "양천구", "영등포구",
                "용산구"]

    for gu in mapping:
        try:
            if gu == value_gu:          
                base_url = './predict_price/raw_data/'
                raw_data_url = base_url + f'{gu}.csv'

                df = pd.read_csv(raw_data_url, encoding='cp949')
                # print(df.head())  
                print(value_dong)
                print(value_apt)
                price_average = df[(df['법정동명'] == value_dong) & (df['건물명'] == value_apt ) & ((df['신고년도'] == 2020)|(df['신고년도'] == 2021))]['물건금액'].mean()
                price_average = round(float(f'{price_average:.0f}') / 100000000, 1)
                if price_average > 0:
                    return price_average
                else :    
                    print(price_average)                 
                    return "최근거래 없음" 
        except:
            return "Something went wrong"

def selected_dong_avg(value_gu, value_dong):
    
    mapping  = ["도봉구", "동대문구", "동작구", "은평구", "강북구", "강동구", "강남구", "강서구", "금천구", "구로구", "관악구", "광진구",
                "종로구", "중구", "중랑구", "마포구", "노원구", "서초구", "서대문구", "성북구", "송파구", "성동구", "양천구", "영등포구",
                "용산구"]

    for gu in mapping:
        try:
            if gu == value_gu:          
                base_url = './predict_price/raw_data/'
                raw_data_url = base_url + f'{gu}.csv'

                df = pd.read_csv(raw_data_url, encoding='cp949')
                # print(df.head())  
                print(value_dong)
                price_average = df[((df['신고년도']==2020) | (df['신고년도']==2021)) & (df['법정동명']==value_dong)]['물건금액'].mean()
                price_average = round(float(f'{price_average:.0f}') / 100000000, 1)
                if price_average > 0:
                    return price_average
                else :    
                    print(price_average)                 
                    return "최근거래 없음" 
        except:
            return "Something went wrong"
  

def prediction_ml(value_gu, value_dong, value_apt, value_size, value_floor, value_cstr_year, value_built_year, value_brand_score, value_trade_index, value_sell):
    
    # 전부 String type으로 들어옴 ex) 마포구, 신공덕동, kcc웰츠, 118.64, 12, 2011, 10, 0, 100, 2021
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
    
    input_data = pd.DataFrame(data)
    
    mapping  = {"도봉구":"dobong", "동대문구":"dongdaemoon", "동작구":"dongjak", "은평구":"eunpyeong", "강북구":"gangbuk", "강동구":"gangdong",
                "강남구":"gangnam", "강서구":"gangseo", "금천구":"geumcheon", "구로구":"guro", "관악구":"gwanak", "광진구":"gwangjin",
                "종로구":"jongno", "중구":"junggu", "중랑구":"jungnang", "마포구":"mapo", "노원구":"nowon", "서초구":"seocho",
                "서대문구":"seodaemoon", "성북구":"seongbuk", "송파구":"songpa", "성동구":"sungdong", "양천구":"yangcheon", "영등포구":"yeongdeungpo",
                "용산구":"yongsan"}
    
    # predict_list = ['노원구','월계동','2021','71.83','3','1983','동신','38','0','100']
    # input_data = pd.DataFrame([predict_list])
    # input_data.columns = ['자치구명','법정동명','신고년도','건물면적','층정보','건축년도','건물명','경과년도','브랜드점수','매매지수']    
    for ko, en in mapping.items():
        try:
            if ko == value_gu:          
                base_url = './predict_price/saved_models/'
                model_url = base_url + f'model_apart_{en}.pkl'
                pipeline_url = base_url + f'pipeline_{en}.pkl'
                stack_url = base_url + f'stack_{en}.pkl'

                model_loaded = joblib.load(model_url)
                pipeline_loaded = joblib.load(pipeline_url)
                stack_loaded = joblib.load(stack_url)
                
                x_test_transformed = pipeline_loaded.transform(input_data)
                s_test = stack_loaded.transform(x_test_transformed)
                print(s_test.shape)
                pred_y = model_loaded.predict(s_test)
                
                print(pred_y)
                
                pred_y = int(pred_y) / 100000000
                
                print(pred_y)
                
                return pred_y
        except:
            return "Something went wrong"

    # base_url = './predict_price/saved_models/'
    # model_url = base_url + 'model_apart_nowon.pkl'
    # pipeline_url = base_url + 'pipeline_nowon.pkl'
    # stack_url = base_url + 'stack_nowon.pkl'

    # model_loaded = joblib.load(model_url)
    # pipeline_loaded = joblib.load(pipeline_url)
    # stack_loaded = joblib.load(stack_url)
    
    # x_test_transformed = pipeline_loaded.transform(input_data)
    # s_test = stack_loaded.transform(x_test_transformed)
    # print(s_test.shape)
    # pred_y = model_loaded.predict(s_test)
    
    # print(pred_y)
    
    # pred_y = int(pred_y) / 100000000
    
    # print(pred_y)
    
    # return pred_y
    
    # pipeline_loaded = joblib.load(pipeline_url)     
    # model_loaded = joblib.load(model_url)
    
    # pipeline_loaded.fit(input_data)
    # input_data_transformed = pipeline_loaded.transform(input_data)
    
    # print(input_data_transformed.shape)
    
    # result = model_loaded.predict(input_data_transformed)
    
    # return result