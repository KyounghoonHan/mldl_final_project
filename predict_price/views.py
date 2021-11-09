from django.shortcuts import render
from .models import Apartment, Dong
import pandas as pd
from django.db.models import Count


# Create your views here.
def first_view(request):

    name_list = Apartment.objects.order_by('dong').values('dong', 'name').distinct()
    dong_name_group = {}
    for dong_name_each in name_list:
        if dong_name_each['dong'] not in dong_name_group.keys():
            dong_name_group[dong_name_each['dong']] = [dong_name_each['name']]
        else:
            dong_name_group[dong_name_each['dong']].append(dong_name_each['name'])

    # print("*******************")
    # print(name_list)
    # print("*******************")
    # print(dong_name_group)

    apt_list = Apartment.objects.order_by('gu').values('gu', 'dong').distinct()   
    gu_dong_group = {} # {'강남구': ['대치동', '압구정동', '도곡동',...], '강동구': ['상일동', '암사동', '길동', ...] ... }
    for gu_dong_each in apt_list :
        if gu_dong_each['gu'] not in gu_dong_group.keys() :
            gu_dong_group[gu_dong_each['gu']] = [gu_dong_each['dong']] # [] 감싸서 강제로 list로 전환 하여 append 할수 있게함
        else:
            gu_dong_group[gu_dong_each['gu']].append(gu_dong_each['dong'])

    # print("*******************")
    # print(apt_list)
    # print("*******************")
    # print(gu_dong_group)

    context = {'gu_dong_group':gu_dong_group, 'dong_name_group':dong_name_group, }
    return render(request, 'predict_price/first_view.html', context)

def prediction(request):

    return render(request, 'predict_price/result.html', {})

def inprocess(request):
    value_gu = request.POST['select_input_gu']
    value_dong = request.POST['select_input_dong']
    value_apt = request.POST['select_input_apt']
    value_size = request.POST['select_input_size']
    
    # Load deep learning code
    # predict_result = predict_iris_one(data_1d_array)
    test = "800000"

    context = {'test':test} # 'predict_result':predict_result 전달

    # return render(request, 'predict_price/result.html', context)
    return render(request, 'predict_price/inprocess.html', context)