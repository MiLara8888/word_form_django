from django.urls import path  # path для создания путей
from . import views  # импорт представлений

urlpatterns = [
    path('', views.home, name='home'),
    path('results', views.results, name='results'),
    path('info', views.info, name='info')
]
