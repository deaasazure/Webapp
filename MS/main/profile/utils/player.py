'''
/*CHANGE HISTORY

--CREATED BY--------CREATION DATE--------VERSION--------PURPOSE----------------------
 Mehul Vaghela       11-Oct-2021          1.0           Initial Version. 
*/
'''
import pandas as pd 
import json
import re
import logging
import traceback
import datetime
from database import *



from common.utils.database import db
from common.utils.exception_handler.python_exception.common.common_exception import *
from common.utils.exception_handler.python_exception.ingest.ingest_exception import *
from common.utils.logger_handler import custom_logger as cl
from django.core.files.storage import FileSystemStorage
from dateutil.parser import parse
user_name = 'admin'
log_enable = True

LogObject = cl.LogClass(user_name,log_enable)
LogObject.log_setting()

logger = logging.getLogger('ingestion')


class ProfileClass():

    def __init__(self):
        """This constructor is used to initialize database credentials.
           It will initialize when object of this class is created with below parameter.
           
        Args:
            database ([string]): [name of the database.],
            user ([string]): [user of the database.],
            password ([string]): [password of the database.],
            host ([string]): [host ip or name where database is running.],
            port ([string]): [port number in which database is running.]
        """
        self.database = database # Database Name
        self.user = user # User Name
        self.password = password # Password
        self.host = host # Host Name
        self.port = port # Port Number
        self.DBObject,self.connection,self.connection_string = self.get_db_connection()
        if self.connection == None :
            raise DatabaseConnectionFailed(500)
        
    def get_db_connection(self):
        """This function is used to initialize database connection.
        
        Returns:
            [object,string]: [it will return database object as well as connection string.]
        """
        logging.info("data ingestion : profileclass : get_db_connection : execution start")
        DBObject = db.DBClass() # Get database object from database class
        connection,connection_string = DBObject.database_connection(self.database,self.user,self.password,self.host,self.port) # Initialize connection with database and get connection string , connection object.
        
        logging.info("data ingestion : profileclass : get_db_connection : execution end")
        return DBObject,connection,connection_string

    
    
    def make_profile_schema(self):
        """This function is used to make schema for creating profile table.
           E.g. column_name  data_type.

        Returns:
            [string]: [it will return name of the table, structure of the table and columns of the table.]
        """
        logging.info("data ingestion : ProfileClass : make_profile_schema : execution start")
        # profile table name
        table_name = 'mlaas.player_profile_tbl'
        # Columns for profile table
        cols = 'player_name,type,category,player_role,dob,team_name,founded_since,profile_pict_path,user_name' 
        # Schema for profile table.
        schema ="player_name  text,"\
                "type  text,"\
                "category text,"\
                "player_role text NULL,"\
                "dob timestamptz NULL,"\
                "team_name text NULL,"\
                "founded_since text NULL,"\
                "profile_pic_path text NULL,"\
                "user_name text NULL,"\
                "created_on TIMESTAMPTZ NOT NULL DEFAULT NOW()" 
                
        logging.info("data ingestion : ProfileClass : make_profile_schema : execution end")
        return table_name,schema,cols

    def make_profile_records(self,player_name,type,category,player_role,dob,team_name,founded_since,profile_pic_path,user_name):
        """This function is used to make records for inserting data into profile table.
           E.g. column_name_1,column_name_2 .......,column_name_n.

        Args:
            profile_name ([string]): [name of the profile.],
            profile_desc ([string]): [descriptions of the profile.],
            user_name ([string]): [name of the user.],
            original_dataset_id ([integer]): [dataset id of the created dataset.]

        Returns:
            [tuple]: [it will return records in the form of tuple.]
        """
        logging.info("data ingestion : ProfileClass : make_profile_records : execution start")
        
        #TODO : both dag are not run together
        # cleanup_dag_id = preprocessObj.get_cleanup_dag_name()
        # cleanup_dag_id = None
        # time.sleep(3)
        # model_dag_id = get_modeling_dag_name()
        
        row = player_name,type,category,player_role,dob,team_name,founded_since,profile_pic_path,user_name
        row_tuples = [tuple(row)] # Make record for profile table.
        logging.info("data ingestion : ProfileClass : make_profile_records : execution end")
        return row_tuples
    
    def create_profile(self,player_name,type,category,player_role,dob,team_name,founded_since,profile_pict_path,user_name):
        """This function is used to create player profile.
           E.g. team / individual profile
           
        Args:
            player_name ([string]): [name of the player],
            type ([string]): [individual/Team],
            category ([string]): [cricket/football etc],
            
           
        Returns:
            [integer]: [status of the profile creation. if successfully then 0 else 1.]
        """
        logging.info("Admin : profileclass : create_profile : execution start")
        try:
            
            table_name,schema,cols = self.make_profile_schema()
            row=player_name,type,category,player_role,dob,team_name,founded_since,profile_pict_path,user_name 
            row_tuples = [tuple(row)]
              
            print(row_tuples)  
            #Insert the dataset record into table
            profile_status = self.DBObject.insert_records(self.connection,table_name,row_tuples,cols)
                
            if profile_status == 0:
                print("Hurrey Success")
            else:
                print("Failed")               
                
        except (DatabaseConnectionFailed) as exc:
            logging.error("data ingestion : profileclass : create_profile : Exception " + str(exc.msg))
            logging.error("data ingestion : profileclass : create_profile : " +traceback.format_exc())
            return exc.msg,None,None
        logging.info("data ingestion : profileclass : create_profile : execution end")
        return profile_status
    
    def get_profile_id(self,user_name):
        """This function is used to get profile id of created profile.

        Args:
            DBObject ([object]): [object of database class.],
            connection ([object]): [connection object of database class.],
            row_tuples ([list]): [list of tuple of record.],
            user_name ([string]): [name of the user.]

        Returns:
            [integer]: [it will return the profile id of the created profile.]
            [integer]: [it will return the schema id of the created profile.]
        """
        try:
            logging.info("data ingestion : profileClass : get_profile_id : execution start")
            
            table_name,*_ = self.make_profile_schema()            
            
            logging.debug("data ingestion : profileClass : get_profile_id : this will excute select query on table name : "+str(table_name) + " based on user name :"+str(user_name))
            sql_command = "SELECT profile_id from "+ str(table_name) + " Where user_name = '"+ str(user_name) + "'"
            profile_df = self.DBObject.select_records(self.connection,sql_command)
            if len(profile_df)>0 :
                profile_id = int(profile_df['profile_id'][0])
            else:
                profile_id =0
            logging.info("data ingestion : profileClass : get_profile_id : execution end")
            return profile_id
        except (DatabaseConnectionFailed) as exc:
            logging.error("data ingestion : profileclass : create_profile : Exception " + str(exc.msg))
            logging.error("data ingestion : profileclass : create_profile : " +traceback.format_exc())
            return exc.msg,None,None
        
    
    def show_profile_details(self,user_name,profile_id):
        """This function is used to show details about all created profiles.

        Args:
            DBObject ([object]): [object of database class.],
            connection ([object]): [connection object of database class.],
            user_name ([string]): [name of the user.]

        Returns:
            [dataframe]: [it will return dataframe of the profile details.]
        """
        try:

            logging.info("data ingestion : profileClass : show_profile_details : execution start")
            table_name,*_ = self.make_profile_schema() # Get table name,schema and columns from dataset class
            # This command is used to get profile details from profile table of database.
            
            logging.debug("data ingestion : profileClass : show_profile_details : this will excute select query on table name : "+table_name +" based on user name : "+user_name)
            try:
                if profile_id is None:
                    sql_command = "SELECT p.* FROM "+ table_name + " p WHERE p.user_name ='"+ user_name +"'"
                else:
                    sql_command = "SELECT p.* FROM "+ table_name + " p WHERE p.profile_id ="+ profile_id 
                logging.info("data ingestion : profileClass :"+sql_command)
                profile_df=self.DBObject.select_records(self.connection,sql_command) # Get profile details in the form of dataframe.
                if len(profile_df) == 0 or profile_df is None:
                    raise RecordNotFound(500)
                
            except Exception as e:
                logging.error("data ingestion : profileclass : create_profile : " +traceback.format_exc())
                return str(e)
                    
            return profile_df
            
        except Exception as exc:
            return exc.msg
            logging.info("data ingestion : profileClass : show_profile_details : execution end")
            
    def delete_profile_details(self,user_name,profile_id):
        '''
        This function is used to delete an entry in the profile_tbl
        
        Args:
            profile_id ([integer]): [id of the entry which you want to delete.],
            user_name ([string]): [Name of the user.]
            
        Returns:
            status ([boolean]): [status of the profile deletion. if successfully then 0 else 1.]
        '''
        logging.info("data ingestion : ingestclass : delete_profile_details : execution start")
        try:
            
            table_name,_,_ = self.make_profile_schema()
            
            if profile_id is None:
                    sql_command = "DELETE FROM "+ table_name + "  WHERE user_name ='"+ user_name +"'"
            else:
                    sql_command = "DELETE FROM "+ table_name + " WHERE profile_id ='"+ profile_id +"'"
                
            deletion_status = self.DBObject.delete_records(self.connection,sql_command)
            if isinstance(deletion_status,str):
                return deletion_status

            if deletion_status == 1:
                raise DataDeletionFailed(500)
            
            logging.info("data ingestion : ingestclass : delete_profile_details : execution end")
            return deletion_status
        
        except (DatabaseConnectionFailed,DataDeletionFailed) as exc:
            logging.error("data ingestion : ingestclass : delete_profile_details : Exception " + str(exc.msg))
            logging.error("data ingestion : ingestclass : delete_profile_details : " +traceback.format_exc())
            return exc.msg,None,None
        
    def update_profile_details(self,user_name,profile_id,player_name,type,category,player_role,dob,team_name,founded_since,profile_pict_path):
        '''
        This function is used to delete an entry in the profile_tbl
        
        Args:
            profile_id ([integer]): [id of the entry which you want to delete.],
            user_name ([string]): [Name of the user.]
            
        Returns:
            status ([boolean]): [status of the profile deletion. if successfully then 0 else 1.]
        '''
        logging.info("data ingestion : ingestclass : update_profile_details : execution start")
        try:
            
            table_name,_,_ = self.make_profile_schema()
            
            if profile_id is None:
                    sql_command = "UPDATE "+str(table_name)+" SET player_name ='"+ str(player_name)+"' ,type = '"+str(type)+"', category='"+str(category)+"',player_role = '"+str(player_role)+"',dob = '"+str(dob)+"',team_name = '"+str(team_name)+"',founded_since = '"+str(founded_since)+"',profile_pict_path = '"+str(profile_pict_path)+"' where user_name ='"+str(user_name)+"'"
            else:
                    sql_command = "UPDATE "+str(table_name)+" SET player_name ='"+ str(player_name)+"' ,type = '"+str(type)+"', category='"+str(category)+"',player_role = '"+str(player_role)+"',dob = '"+str(dob)+"',team_name = '"+str(team_name)+"',founded_since = '"+str(founded_since)+"',profile_pict_path = '"+str(profile_pict_path)+"' where profile_id ='"+str(profile_id)+"'"
                
            # Execute the sql query
            update_status = self.DBObject.update_records(self.connection,sql_command)

            if update_status !=0:
                raise DatasetColumnUpdateFailed(500)
                
            logging.info("data ingestion : DatasetClass : update_profile_details : execution stop")
            return update_status
        
        except (DatabaseConnectionFailed,DataDeletionFailed) as exc:
            logging.error("data ingestion : ingestclass : update_profile_details : Exception " + str(exc.msg))
            logging.error("data ingestion : ingestclass : update_profile_details : " +traceback.format_exc())
            return exc.msg,None,None
        