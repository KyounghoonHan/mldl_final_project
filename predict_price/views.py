from django.shortcuts import render
from .models import Apartment, Dong, Apt
import pandas as pd
from django.db.models import Count
from .predict_ml import prediction_ml, selected_apt_avg, selected_dong_avg


def first_view(request):

    # print("*******************")
    # print(name_list)
    # print("*******************")
    # print(dong_name_group)

    apt_list = Apt.objects.order_by('gu').values('gu', 'dong').distinct().order_by('dong')   
    gu_dong_group = {} # {'강남구': ['대치동', '압구정동', '도곡동',...], '강동구': ['상일동', '암사동', '길동', ...] ... }
    for gu_dong_each in apt_list :
        if gu_dong_each['gu'] not in gu_dong_group.keys() :
            gu_dong_group[gu_dong_each['gu']] = [gu_dong_each['dong']] # [] 감싸서 강제로 list로 전환 하여 append 할수 있게함
        else:
            gu_dong_group[gu_dong_each['gu']].append(gu_dong_each['dong'])

    name_list = Apt.objects.order_by('dong').values('dong', 'name').distinct().order_by('name')
    dong_name_group = {}
    for dong_name_each in name_list:
        if dong_name_each['dong'] not in dong_name_group.keys():
            dong_name_group[dong_name_each['dong']] = [dong_name_each['name']]
        else:
            dong_name_group[dong_name_each['dong']].append(dong_name_each['name'])

    size_list = Apt.objects.order_by('name').values('name', 'size').distinct().order_by('size')
    name_size_group = {}
    for name_size_each in size_list:
        if name_size_each['name'] not in name_size_group.keys():
            name_size_group[name_size_each['name']] = [name_size_each['size']]
        else:
            name_size_group[name_size_each['name']].append(name_size_each['size'])

    floor_list = Apt.objects.order_by('name').values('name', 'floor').distinct().order_by('floor')
    name_floor_group = {}
    for name_floor_each in floor_list:
        if name_floor_each['name'] not in name_floor_group.keys():
            name_floor_group[name_floor_each['name']] = [name_floor_each['floor']]
        else:
            name_floor_group[name_floor_each['name']].append(name_floor_each['floor'])

    cstr_year_list = Apt.objects.order_by('name').values('name', 'cstr_year').distinct().order_by('cstr_year')
    name_cstr_year_group = {}
    for name_cstr_year_each in cstr_year_list:
        if name_cstr_year_each['name'] not in name_cstr_year_group.keys():
            name_cstr_year_group[name_cstr_year_each['name']] = [name_cstr_year_each['cstr_year']]
        else:
            name_cstr_year_group[name_cstr_year_each['name']].append(name_cstr_year_each['cstr_year'])

    built_year_list = Apt.objects.order_by('name').values('name', 'built_year').distinct().order_by('built_year')
    name_built_year_group = {}
    for name_built_year_each in built_year_list:
        if name_built_year_each['name'] not in name_built_year_group.keys():
            name_built_year_group[name_built_year_each['name']] = [name_built_year_each['built_year']]
        else:
            name_built_year_group[name_built_year_each['name']].append(name_built_year_each['built_year'])

    brand_score_list = Apt.objects.order_by('name').values('name', 'brand_score').distinct().order_by('brand_score')
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


def prediction(request, apt_name, price, apt_average, dong_average):
    
    # 최선도 님과 함께
    # - 아파트가 속한 동 내 아파트 평균가 계산
    # - 해당 아파트의 평균가 계산
    # -> 이 2가지 계산이 끝난 후 아래 context 에 포함시켜 result.html 에서 보여주셔요!
    
    context = {'apt_name':apt_name, 'price':price, 'apt_average':apt_average, 'dong_average':dong_average}
    
    return render(request, 'predict_price/result.html', context)


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
    
    print(type(value_gu), value_gu)
    print(type(value_dong), value_dong)
    print(type(value_apt), value_apt)
    print(type(value_size), value_size)
    print(type(value_floor), value_floor)
    print(type(value_cstr_year), value_cstr_year)
    print(type(value_built_year), value_built_year)
    print(type(value_brand_score), value_brand_score)
    print(type(value_trade_index), value_trade_index)
    print(type(value_sell), value_sell)
  
    predict_result = prediction_ml(value_gu, value_dong, value_apt, value_size, value_floor, value_cstr_year, value_built_year, value_brand_score,
                                value_trade_index, value_sell)

    apt_avg = selected_apt_avg(value_gu, value_dong, value_apt)

    dong_avg = selected_dong_avg(value_gu, value_dong)    
    
    context = {'value_apt':value_apt, 'predict_result':predict_result, 'apt_avg':apt_avg, 'dong_avg':dong_avg}

    return render(request, 'predict_price/inprocess.html', context) 

    # test = "800000"
    
    # return render(request, 'predict_price/inprocess.html', {'test':test})