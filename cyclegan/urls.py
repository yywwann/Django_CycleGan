from django.urls import path

from . import views
app_name = 'cyclegan'
urlpatterns = [
    path('', views.index, name='index'),
    # path('show', views.upload, name='show')
]
