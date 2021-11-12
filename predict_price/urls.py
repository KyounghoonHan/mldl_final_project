from django.urls import path
from . import views 

app_name = 'predict_price'

urlpatterns = [
    path('', views.first_view, name='first_view'),  
    path('inprocess/', views.inprocess, name='inprocess'),
    # path('prediction/', views.prediction, name='prediction'), # original
    path('prediction/<str:apt_name>/<str:price>/<str:apt_average>/<str:dong_average>', views.prediction, name='prediction'), # added
]
