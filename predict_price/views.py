from django.shortcuts import render
from .models import Apartment, Dong, Apt
import pandas as pd
from django.db.models import Count
# from .predict_ml import prediction

# Create your views here.
def first_view(request):

    # print("*******************")
    # print(name_list)
    # print("*******************")
    # print(dong_name_group)

    apt_list = Apt.objects.order_by('gu').values('gu', 'dong').distinct()   
    gu_dong_group = {} # {'강남구': ['대치동', '압구정동', '도곡동',...], '강동구': ['상일동', '암사동', '길동', ...] ... }
    for gu_dong_each in apt_list :
        if gu_dong_each['gu'] not in gu_dong_group.keys() :
            gu_dong_group[gu_dong_each['gu']] = [gu_dong_each['dong']] # [] 감싸서 강제로 list로 전환 하여 append 할수 있게함
        else:
            gu_dong_group[gu_dong_each['gu']].append(gu_dong_each['dong'])

    name_list = Apt.objects.order_by('dong').values('dong', 'name').distinct()
    dong_name_group = {}
    for dong_name_each in name_list:
        if dong_name_each['dong'] not in dong_name_group.keys():
            dong_name_group[dong_name_each['dong']] = [dong_name_each['name']]
        else:
            dong_name_group[dong_name_each['dong']].append(dong_name_each['name'])

    size_list = Apt.objects.order_by('name').values('name', 'size').distinct()
    name_size_group = {}
    for name_size_each in size_list:
        if name_size_each['name'] not in name_size_group.keys():
            name_size_group[name_size_each['name']] = [name_size_each['size']]
        else:
            name_size_group[name_size_each['name']].append(name_size_each['size'])

    floor_list = Apt.objects.order_by('name').values('name', 'floor').distinct()
    name_floor_group = {}
    for name_floor_each in floor_list:
        if name_floor_each['name'] not in name_floor_group.keys():
            name_floor_group[name_floor_each['name']] = [name_floor_each['floor']]
        else:
            name_floor_group[name_floor_each['name']].append(name_floor_each['floor'])

    cstr_year_list = Apt.objects.order_by('name').values('name', 'cstr_year').distinct()
    name_cstr_year_group = {}
    for name_cstr_year_each in cstr_year_list:
        if name_cstr_year_each['name'] not in name_cstr_year_group.keys():
            name_cstr_year_group[name_cstr_year_each['name']] = [name_cstr_year_each['cstr_year']]
        else:
            name_cstr_year_group[name_cstr_year_each['name']].append(name_cstr_year_each['cstr_year'])

    built_year_list = Apt.objects.order_by('name').values('name', 'built_year').distinct()
    name_built_year_group = {}
    for name_built_year_each in built_year_list:
        if name_built_year_each['name'] not in name_built_year_group.keys():
            name_built_year_group[name_built_year_each['name']] = [name_built_year_each['built_year']]
        else:
            name_built_year_group[name_built_year_each['name']].append(name_built_year_each['built_year'])

    brand_score_list = Apt.objects.order_by('name').values('name', 'brand_score').distinct()
    name_brand_score_group = {}
    for name_brand_score_each in brand_score_list:
        if name_brand_score_each['name'] not in name_brand_score_group.keys():
            name_brand_score_group[name_brand_score_each['name']] = [name_brand_score_each['brand_score']]
        else:
            name_brand_score_group[name_brand_score_each['name']].append(name_brand_score_each['brand_score'])

    # print("*******************")
    # print(floor_list)
    # print("*******************")
    # print(name_floor_group)

    context = {'gu_dong_group':gu_dong_group, 'dong_name_group':dong_name_group, 'name_size_group':name_size_group,
               'name_floor_group':name_floor_group, 'name_cstr_year_group':name_cstr_year_group, 'name_built_year_group':name_built_year_group,
               'name_brand_score_group':name_brand_score_group,
               }
    return render(request, 'predict_price/first_view.html', context)

def prediction(request):
    return render(request, 'predict_price/result.html', {})

def inprocess(request):
    value_gu = request.POST['select_input_gu']
    value_dong = request.POST['select_input_dong']
    value_apt = request.POST['select_input_apt']
    value_size = request.POST['select_input_size']
    value_floor = request.POST['select_input_floor']
    value_cstr_year = request.POST['select_input_cstr_year']
    value_built_year = request.POST['select_input_built_year']
    value_brand_score = request.POST['select_input_brand_score']
    value_trade_index = request.POST['select_input_trade_index']
    value_sell = request.POST['select_input_sell']
    
    # Load deep learning code
    # predict_result = predict_iris_one(data_1d_array)
    
    # predict_result = prediction(value_gu, value_dong, value_apt, value_size, value_floor, value_cstr_year, value_built_year, value_brand_score,
    #                             value_trade_index, value_sell)

    # context = {'predict_result':predict_result}
    
    test = "800000"

    # context = {'test':test, 'value_gu':value_gu, 'value_dong':value_dong, 'value_apt':value_apt, 'value_size':value_size,
    #            'value_sell':value_sell, 'value_floor':value_floor, 'value_cstr_year':value_cstr_year, 'value_built_year':value_built_year,
    #            'value_brand_score':value_brand_score, 'value_trade_index':value_trade_index,
    #            } # 'predict_result':predict_result 전달

    # return render(request, 'predict_price/result.html', context) 
    
    return render(request, 'predict_price/inprocess.html', {'test':test})