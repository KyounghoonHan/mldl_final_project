from django.shortcuts import render
from .models import Apartment, Dong
import pandas as pd
from django.db.models import Count


# Create your views here.
def first_view(request):

    size_list = Apartment.objects.order_by('size').values('size').distinct() 
    apt_list = Apartment.objects.order_by('gu').values('gu', 'dong').distinct()
    
    gu_dong_group = {} # {'강남구': ['대치동', '압구정동', '도곡동',...], '강동구': ['상일동', '암사동', '길동', ...] ... }
    for gu_dong_each in apt_list :
        if gu_dong_each['gu'] not in gu_dong_group.keys() :
            gu_dong_group[gu_dong_each['gu']] = [gu_dong_each['dong']] # [] 감싸서 강제로 list로 전환 하여 append 할수 있게함
        else:
            gu_dong_group[gu_dong_each['gu']].append(gu_dong_each['dong'])

    print("*******************")
    print(apt_list)
    print("*******************")
    print(gu_dong_group)

    context = {'apt_list':apt_list, 'gu_dong_group':gu_dong_group, 'size_list':size_list}
    return render(request, 'predict_price/first_view.html', context)


def prediction(request):
    value_gu = request.POST['select_input_gu']
    value_dong = request.POST['select_input_dong']
    value_size = request.POST['select_input_size']
    
    # Deep Learning 
    # predict_result = predict_iris_one(data_1d_array)
    context = {'value_gu': value_gu, 'value_dong': value_dong, 'value_size': value_size}
    return render(request, 'predict_price/result.html', context)


def calculator(reqeust):
    pass