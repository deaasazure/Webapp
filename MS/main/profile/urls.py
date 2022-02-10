from django.urls import path
from .views import *

urlpatterns = [

    #URL For Create profile
    path('main/profile/create/',CreateProfileClass.as_view()),

    #URL For profile Detail
    #path('main/profile/detail/',ShowProfileClass.as_view()),

    #URL For delete profile Detail
    #path('main/profile/delete/',DeleteProfileClass.as_view()),

    #URL For profile exist
    #path('main/profile/exist/',profileExistClass.as_view()),
]