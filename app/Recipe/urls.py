from django.urls import path

from .views import HomeTemplateView

app_name = 'Recipe'

urlpatterns = [
    path('', HomeTemplateView.as_view(), name='home')
]