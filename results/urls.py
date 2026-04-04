from django.urls import path
from . import views

app_name = 'results'

urlpatterns = [
    path('', views.result_list, name='list'),
    path('<int:attempt_id>/', views.result_detail, name='detail'),
]
