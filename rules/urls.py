from django.urls import path

from . import views

app_name = 'rules'

urlpatterns = [
    # ex: /events/
    path('', views.create, name='create'),
]
