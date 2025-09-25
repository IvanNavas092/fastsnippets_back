from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('chat', views.chat, name='chat'),
    path('api/csrf/',views.get_csrf, name='get_csrf'),

]