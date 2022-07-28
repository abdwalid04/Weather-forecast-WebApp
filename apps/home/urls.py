# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    # the data_table page
    path('table/', views.table, name='table'),
    
    # the data_table page
    path('tablevalide/', views.tablevalide, name='tablevalide'),
    
    # the validation page
    path('validation/', views.Viewvalide, name='validation'),
    
    # the data_table page
    path('upload/', views.upload, name='upload'),

    # the map page
    path('map/', views.map, name='map'),
    
    # the MLmodel page
    path('model/', views.model, name='model'),
    
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),
]
