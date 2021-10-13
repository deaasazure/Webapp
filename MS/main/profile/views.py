'''
/*CHANGE HISTORY

--CREATED BY--------CREATION DATE--------VERSION--------PURPOSE----------------------
 Mehul Vaghela      12-Oct-2021           1.0           Intial Version 

 ****************************************************************************************/

*/
'''
# Python library import
import json
import logging
import traceback
import pandas as pd
import datetime 
from rest_framework.views import APIView
from rest_framework.response import Response

# Database variable file import
from database import *

# Ingest utils files

# Common file imports
from common.utils.exception_handler.python_exception import *
from common.utils.exception_handler.python_exception.common.common_exception import *
from common.utils.exception_handler.python_exception.ingest.ingest_exception import *


from common.utils.json_format.json_formater import *
from common.utils.activity_timeline import *
from common.utils.activity_timeline import activity_timeline
from common.utils.logger_handler import custom_logger as cl

from profile.utils.player import ProfileClass as clsProfile

user_name = 'admin'
log_enable = True
error_msg =""
status_code = 200
LogObject = cl.LogClass(user_name,log_enable)
LogObject.log_setting()
logger = logging.getLogger('profile_view')

profile_obj = clsProfile() #initialize the Profile Class
json_obj = JsonFormatClass() #initialize the JsonFormat Class 
timeline_Obj=activity_timeline.ActivityTimelineClass(database,user,password,host,port) #initialize the ActivityTimeline Class


# Class for Profile to retrive & insert 
#It will take url string as mlaas/ingest/create_Profile/.
class CreateProfileClass(APIView):

        def get(self, request, format=None):
                """
                This function is used to get Profile details Entered by the user.
        
                Args  : 
                        User_name[(String)]   :[Name of user]
                Return : 
                        status_code(500 or 200),
                        error_msg(Error message for retrival & insertions failed or successfull),
                        Response(return false if failed otherwise json data)
                """
                try:
                        logging.info("CreateProfileClass : GET Method : execution start")
                        user_name  = request.query_params.get('user_name') #get Username
                        profile_id  = request.query_params.get('profile_id') #get profile_id
                        profile_df = profile_obj.show_profile_details(user_name,profile_id) #call show_Profile_details to retrive Profile detail data and it will return dataframe
                        if isinstance(profile_df,str): #check the instance of dataset_df
                                status_code,error_msg=json_obj.get_Status_code(profile_df) # extract the status_code and error_msg from Profile_df
                                logging.info("CreateProfileClass : GET Method : execution : status_code :"+ status_code)
                                return Response({"status_code":status_code,"error_msg":error_msg,"response":"false"})
                        else:
                                logging.info("CreateProfileClass : GET Method : execution : status_code : 200")
                                return Response({"status_code":"200","error_msg":"successfull retrival","response":profile_df})  

                except Exception as e:
                        logging.error("CreateProfileClass : GET Method : " + str(e))
                        logging.error("CreateProfileClass : GET Method : " +traceback.format_exc())
                        return Response({"status_code":"500","error_msg":str(e),"response":"false"})  
        
        def post(self, request, format=None):
                """
                This function is used to Create Or Update Profile

                Args  : 
                        User_name[(String)]   :[Name of user]
                        ProfileName[(String)] :[Name of Profile]
                Return : 
                        status_code(500 or 200),
                        error_msg(Error message for retrival & insertions failed or successfull),
                        Response(return false if failed otherwise true)
                """
                try:
                                
                        logging.info("data ingestion : CreateProfileClass : POST Method : execution start")
                        user_name=request.POST.get('user_name')  #get Username
                        player_name=request.POST.get('player_name') #get player_name
                        type=request.POST.get('type') #get type
                        category=request.POST.get('category') #get category
                        player_role = request.POST.get('player_role')#get player_role
                        dob = request.POST.get('dob')#get dob
                        team_name = request.POST.get('team_name') #get team_name
                        founded_since = request.POST.get('founded_since') # get founded_since 
                        profile_pict_path = request.POST.get('profile_pict_path') # get profile_pict_path
                                               
                        profile_id=profile_obj.get_profile_id(user_name) #get the status if profile exist or not 
                        if profile_id > 0:
                                update_status=profile_obj.update_profile_details(user_name,profile_id,player_name,type,category,player_role,dob,team_name,founded_since,profile_pict_path) # extract the status_code and error_msg from datasetexist_status
                                status_code=200
                                error_msg=""
                                logging.info("data ingestion : ProfileExistClass : GET Method : execution stop : status_code :200")
                                return Response({"status_code":status_code,"error_msg":error_msg,"response":"false"})
                        else:
                                logging.info("data ingestion : DatasetExistClass : GET Method : execution stop : status_code :200")
                                profile_status=profile_obj.create_profile(player_name,type,category,player_role,dob,team_name,founded_since,profile_pict_path,user_name)    #call create_Profile method to create Profile and insert csv data into table
                                if profile_status != 0:
                                        status_code=200
                                        error_msg=""
                                        #status_code,error_msg=json_obj.get_Status_code(profile_status) # extract the status_code and error_msg from Profile_Status
                                        logging.info("data ingestion : CreateProfileClass : POST Method : execution stop : status_code :")
                                        return Response({"status_code":status_code,"error_msg":error_msg,"response":"false"}) 
                                else:
                                        activity_id = 'ur_5'
                                        activity_df = timeline_Obj.get_activity(activity_id,"US")
                                        activity_description = "{x} '{y}'".format(x=activity_df[0]["activity_description"],y= player_name)
                                        end_time = str(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
                                        activity_status,index = timeline_Obj.insert_user_activity(activity_id,user_name,player_name,category,activity_description,end_time)
                                        if isinstance(activity_status,str):
                                                status_code,error_msg=json_obj.get_Status_code(activity_status) # extract the status_code and error_msg from activity_status
                                                logging.info("data ingestion : CreateProfileClass : POST Method : execution stop : status_code :"+status_code)
                                                return Response({"status_code":status_code,"error_msg":error_msg,"response":"false"})
                                        else:
                                                logging.info("data ingestion : CreateProfileClass : POST Method : execution stop : status_code : 200")
                                                return Response({"status_code":"200","status_msg":"Successfully Inserted","response":"true"}) 

                except Exception as e:
                        logging.error("data ingestion : CreateProfileClass : POST Method : " + str(e))
                        logging.error("data ingestion : CreateProfileClass : POST Method : " +traceback.format_exc())
                        return Response({"status_code":"500","error_msg":str(e),"response":"false"})      
