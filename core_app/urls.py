from django.urls import path
from .views import *

urlpatterns = [

    path('', home, name='home'),
    
    path('newblog/', newblog, name='newblog'),
    
    path('sortCategories/<id>', sortCategories, name='sortCategories'),
    
    path('blog/<id>', blog, name='blog'),

]
