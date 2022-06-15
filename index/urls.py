from django.urls import path
from . import views
from .views import activate

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('account/', views.account, name='account'),
    path('pacient_list/', views.pacient_list, name='pacient_list'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
                activate, name='activate'),
    path('verify/', views.verify, name='verify'),
]