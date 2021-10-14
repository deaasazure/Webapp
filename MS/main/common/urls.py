from django.urls import path
from .views import *

urlpatterns = [
    #mlaas/common/user/login/
    #URL For User Login
    path('main/common/user/login/',UserLoginClass.as_view()),

    #URL for menu
    path('main/common/menu/',MenuClass.as_view()),

    #url for activity timeline
    path('main/common/activity/',ActivityTimelineClass.as_view()),

    #url to read logfile 
    path('main/common/logfile/',LogFileClass.as_view()),

    #url to get dag details
    #path('main/common/daginfo/',DagInfoClass.as_view()),

    
    #path('mlaas/common/test/',TestMongoClass.as_view()),

]