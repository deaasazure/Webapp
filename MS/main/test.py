from profile.utils.player import ProfileClass as clsProfile
import pandas as pd
import os

obj_data_explore = clsProfile()
profile_status= obj_data_explore.create_profile("jay","I","cricket","keeper","1982-11-11","India","1982","azure","admin")
#profile_id=obj_data_explore.get_profile_id("admin")
#profile_df=obj_data_explore.show_profile_details("admin",'2')
#deletion_status=obj_data_explore.delete_profile_details("admin",'2')
#update_status=obj_data_explore.update_profile_details("admin",'1',"Vishal"," "," "," ","1982-10-10"," "," "," ")
#print(update_status)



