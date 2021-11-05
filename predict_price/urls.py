from django.urls import path
from . import views 

app_name = 'predict_price'

urlpatterns = [
    path('', views.first_view, name='first_view'),  
    path('caculator/', views.calculator, name='caculator'),
    path('prediction/', views.prediction, name='prediction'),
]
