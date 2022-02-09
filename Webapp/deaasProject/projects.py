'''
/*CHANGE HISTORY

--CREATED BY--------CREATION DATE--------VERSION--------PURPOSE----------------------
 Mehul Vaghela       01-Nov-2021          1.0           Initial Version. 
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
from common.utils.user.user_login import *
from common.utils.exception_handler.python_exception.common.common_exception import *
from common.utils.exception_handler.python_exception.ingest.ingest_exception import *
from common.utils.logger_handler import custom_logger as cl
# from django.core.files.storage import FileSystemStorage
from dateutil.parser import parse

user_name = 'admin'
log_enable = True

LogObject = cl.LogClass(user_name,log_enable)
LogObject.log_setting()

logger = logging.getLogger('ingestion')


class ProjectClass(UserClass):

    def __init__(self):
        """This constructor is used to initialize database credentials.
           It will initialize when object of this class is created.
        """
        UserObj = UserClass() # Get database object from database class
        self.connection = UserObj.connection
        self.connection_string=UserObj.connection
        
    
    def make_project_schema(self):
        """This function is used to make schema for creating project table.
           E.g. column_name  data_type.

        Returns:
            [string]: [it will return name of the table, structure of the table and columns of the table.]
        """
        logging.info("projectClass : make_project_schema : execution start")
        # project table name
        table_name = 'mlaas.project_tbl'
        # Columns for project table
        cols = 'project_name,project_desc,created_by' 
        # Schema for project table.
        schema ="project_name  text,"\
                "project_desc text,"\
                "project_status int4,"\
                "created_by int8 NULL,"\
                "created_on TIMESTAMPTZ NOT NULL DEFAULT NOW()" 
                
        logging.info("projectClass : make_project_schema : execution end")
        return table_name,schema,cols

    def make_project_records(self,project_name,project_desc,user_name):
        """This function is used to make records for inserting data into project table.
           E.g. column_name_1,column_name_2 .......,column_name_n.

        Args:
            project_name ([string]): [name of the project.],
            project_desc ([string]): [descriptions of the project.],
            user_name ([string]): [name of the user.],
            original_dataset_id ([integer]): [dataset id of the created dataset.]

        Returns:
            [tuple]: [it will return records in the form of tuple.]
        """
        logging.info("projectClass : make_project_records : execution start")
        user_id=super().get_user_id(user_name) 
        row = project_name,project_desc,user_id
        row_tuples = [tuple(row)] # Make record for project table.
        print(row_tuples)
        logging.info("projectClass : make_project_records : execution end")
        return row_tuples
    
    def create_project(self,project_name,project_desc,user_name):
        """This function is used to create player project.
           E.g. team / individual project
           
        Args:
            project_name ([string]): [name of the player],
            type ([string]): [individual/Team],
            category ([string]): [cricket/football etc],
            
           
        Returns:
            [integer]: [status of the project creation. if successfully then 0 else 1.]
        """
        logging.info("projectclass : create_project : execution start")
        try:
            
            table_name,schema,cols = self.make_project_schema()
            
            row_tuples = self.make_project_records(project_name,project_desc,user_name)
            #Insert the dataset record into table
            project_status = super(UserClass,self).insert_records(self.connection,table_name,row_tuples,cols)
                
            if project_status == (0,0):
                self.project_id = self.get_project_id(project_name)
            else:
                self.project_id=0               
            return self.project_id    
        except (DatabaseConnectionFailed) as exc:
            logging.error("projectclass : create_project : Exception " + str(exc.msg))
            logging.error("projectclass : create_project : " +traceback.format_exc())
            return exc.msg,None,None
        logging.info("projectclass : create_project : execution end")
        
    
    def get_project_id(self,project_name):
        """This function is used to get project id of created project.

        Args:
            DBObject ([object]): [object of database class.],
            connection ([object]): [connection object of database class.],
            row_tuples ([list]): [list of tuple of record.],
            user_name ([string]): [name of the user.]

        Returns:
            [integer]: [it will return the project id of the created project.]
            [integer]: [it will return the schema id of the created project.]
        """
        try:
            logging.info("projectClass : get_project_id : execution start")
            
            project_id = super().get_user_id(project_name)
            
            table_name,*_ = self.make_project_schema()            
            
            logging.debug("projectClass : get_project_id : this will excute select query on table name : "+str(table_name) + " based on user name :"+str(user_name))
            sql_command = "SELECT project_id from "+ str(table_name) + " Where project_name = '"+ str(project_name) + "'"
            project_df = super(UserClass,self).select_records(self.connection,sql_command)
            if len(project_df)>0 :
                project_id = int(project_df['project_id'][0])
            else:
                project_id =0
            logging.info("projectClass : get_project_id : execution end")
            return project_id
        except (DatabaseConnectionFailed) as exc:
            logging.error("projectclass : create_project : Exception " + str(exc.msg))
            logging.error("projectclass : create_project : " +traceback.format_exc())
            return exc.msg,None,None
        
    
    def show_project(self,user_name,project_name):
        """This function is used to show details about all created projects.

        Args:
            DBObject ([object]): [object of database class.],
            connection ([object]): [connection object of database class.],
            user_name ([string]): [name of the user.]

        Returns:
            [dataframe]: [it will return dataframe of the project details.]
        """
        try:

            logging.info("projectClass : show_project_details : execution start")
            table_name,*_ = self.make_project_schema() # Get table name,schema and columns from dataset class
            # This command is used to get project details from project table of database.
            user_id = super().get_user_id(user_name)
            
            logging.debug("projectClass : show_project_details : this will excute select query on table name : "+table_name +" based on user name : "+user_name)
            try:
                if project_name is None:
                    sql_command = "SELECT p.* FROM "+ table_name + " p WHERE p.created_by ='"+ user_id +"'"
                else:
                    sql_command = "SELECT p.* FROM "+ table_name + " p WHERE p.project_name ='"+project_name+"'"
                logging.info("projectClass :"+sql_command)
                project_df=super(UserClass,self).select_records(self.connection,sql_command) # Get project details in the form of dataframe.
                if len(project_df) == 0 or project_df is None:
                    raise RecordNotFound(500)
                
            except Exception as e:
                logging.error("projectclass : create_project : " +traceback.format_exc())
                return str(e)
            
            logging.info("projectClass : show_project_details : execution end")        
            return project_df
            
        except Exception as exc:
            return exc.msg
            
            
    def delete_project(self,user_name,project_name):
        '''
        This function is used to delete an entry in the project_tbl
        
        Args:
            project_id ([integer]): [id of the entry which you want to delete.],
            user_name ([string]): [Name of the user.]
            
        Returns:
            status ([boolean]): [status of the project deletion. if successfully then 0 else 1.]
        '''
        logging.info("projectClass : delete_project_details : execution start")
        try:
            
            table_name,_,_ = self.make_project_schema()
            
            user_id = super().get_user_id(user_name)
            
            if project_name is None:
                    sql_command = "DELETE FROM "+ str(table_name) + "  WHERE created_by ="+ str(user_id)
            else:
                    sql_command = "DELETE FROM "+ str(table_name) + " WHERE project_name ="+ str(project_name)
            print(sql_command)    
            deletion_status = super(UserClass,self).delete_records(self.connection,sql_command)
            if isinstance(deletion_status,str):
                return deletion_status

            if deletion_status == 1:
                raise DataDeletionFailed(500)
            
            logging.info("projectClass : delete_project_details : execution end")
            return deletion_status
        
        except (DatabaseConnectionFailed,DataDeletionFailed) as exc:
            logging.error("projectClass : delete_project_details : Exception " + str(exc.msg))
            logging.error("projectClass : delete_project_details : " +traceback.format_exc())
            return exc.msg,None,None
        
    def update_project(self,user_name,project_id,project_name):
        '''
        This function is used to delete an entry in the project_tbl
        
        Args:
            project_id ([integer]): [id of the entry which you want to delete.],
            user_name ([string]): [Name of the user.]
            
        Returns:
            status ([boolean]): [status of the project deletion. if successfully then 0 else 1.]
        '''
        logging.info("projectClass : update_project_details : execution start")
        try:
            
            table_name,_,_ = self.make_project_schema()
            
            user_id = super().get_user_id(user_name)
            
            if project_id is None:
                    sql_command = "UPDATE "+str(table_name)+" SET project_name ='"+ str(project_name)+"' where created_by ='"+str(user_id)+"'"
            else:
                    sql_command = "UPDATE "+str(table_name)+" SET project_name ='"+str(project_name)+"' where project_id ='"+str(project_id)+"'"
                
            # Execute the sql query
            update_status = super(UserClass,self).update_records(self.connection,sql_command)

            if update_status !=0:
                raise DatasetColumnUpdateFailed(500)
                
            logging.info("projectClass : update_project_details : execution stop")
            return update_status
        
        except (DatabaseConnectionFailed,DataDeletionFailed) as exc:
            logging.error("projectClass : update_project_details : Exception " + str(exc.msg))
            logging.error("projectClass : update_project_details : " +traceback.format_exc())
            return exc.msg,None,None
        