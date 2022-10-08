from django.urls import path, include
from . import views

app_name = 'User'

urlpatterns = [
    path('api/login/', views.UserLoginApiView.as_view(), name='login'),

]