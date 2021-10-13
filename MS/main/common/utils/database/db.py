'''
/*CHANGE HISTORY

--CREATED BY--------CREATION DATE--------VERSION--------PURPOSE----------------------
 Mehul Vaghela      12-Oct-2021           1.0           Initial Version 
*/
'''
#Python library imports
import psycopg2
import psycopg2.extras as extras
import pandas as pd 
import numpy as np
import json
import logging
import traceback
from sqlalchemy import create_engine

#database variable file import
from database import *
#from common.utils.dataset import dataset_creation as dc

#Common utils import
from common.utils.logger_handler import custom_logger as cl
from common.utils.exception_handler.python_exception.common.common_exception import *

user_name = 'admin'
log_enable = True
LogObject = cl.LogClass(user_name,log_enable)
LogObject.log_setting()
logger = logging.getLogger('dataset_creation')

#? Dataset Class Object
#DatasetObject = dc.DatasetClass()
class DBClass:

    def read_data(self,file_path):
        """This function is used read data from server file and load into dataframe.

        Args:
            file_path ([string]): [relative path of the file of server.]

        Returns:
            [dataframe]: [it will return read csv file data in the form of dataframe.]
        """

        read_df=pd.read_csv(file_path) #  Read csv file and load data into dataframe.

        column_name_list = read_df.columns.values.tolist()
    
        column_list = []
        for name in column_name_list:
            if read_df.dtypes.to_dict()[name] == 'object':
                column_list.append(name)
        
        read_df=pd.read_csv(file_path,parse_dates=column_list) #  Read csv file and load data into dataframe.
        
        dataframe = read_df.replace(r'^\s*$', np.nan, regex=True)
        
        return dataframe
    
    def database_connection(self,database,user,password,host,port):
        """This function is used to make connection with database.

        Args:
            database ([string]): [name of the database.],
            user ([string]): [user of the database.],
            password ([string]): [password of the database.],
            host ([string]): [host ip or name where database is running.],
            port ([string]): [port number in which database is running.]

        Returns:
            [object,string]: [it will return connection object well as connection string.]
        """
        try:
            connection_string = "postgresql://" + user + ":" + password + "@" + host + ":" + port + "/" + database # Make database connection string.
            connection = psycopg2.connect(database = database, user = user , password = password, host = host, port = port) #Get connection object by initializing connection to database. 
        except:
            return None,None
            
        return connection,connection_string

    def create_sequence(self,connection):
        cursor = connection.cursor()
        try:
            sql_command = 'CREATE SEQUENCE dataset_sequence INCREMENT 1 START 1;'
            cursor.execute(sql_command)
            connection.commit()
            cursor.close()
            return 0
        except (Exception,psycopg2.DatabaseError) as error:
            connection.rollback() # Rollback the changes.
            cursor.close() # Close the cursor
            return 1 # If failed.

    def get_sequence(self,connection):
        sql_command = "select nextval('dataset_sequence')"
        data = self.select_records(connection, sql_command)
        return data

    def is_exist_sequence(self,connection,seq_name):
        sql_command = "SELECT * FROM information_schema.sequences where sequence_name ='"+ seq_name +"'"
        data=self.select_records(connection,sql_command) #call select_records which return data if found else None
        if len(data) == 0: # check whether length of data is empty or not
            data = self.create_sequence(connection)
            if data == 0:
                return "True"
            else :
                return "False"
        else:
            return "True"

    #v1.3
    def create_schema(self,connection,user_name = None):
        """This function is used to create schema.

        Args:
            connection ([object]): [connection for database],
            user_name ([string]): [user name]

        Returns:
            [integer]: [status of create schema. if successfully then 0 else 1.]
        """
        if user_name == None :
            schema_name = "mlaas"
        else:
            schema_name = user_name.lower() # Get schema name.
            
        cursor = connection.cursor() # Open cursor for database.
        try:
            cursor.execute('CREATE Schema '+ schema_name +';') # Excute create schema query.
            connection.commit() # Commit the changes.
            return 0 # If successfully created.
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback() # Rollback the changes.
            cursor.close() # Close the cursor
            return 1 # If failed.
        
    def create_table(self,connection,table_name,schema):
        """This function is used to  create table into database.

        Args:
            connection ([object]): [object of the connection to the database.],
            table_name ([string]): [name of the table.],
            schema ([string]): [structure of the table.]

        Returns:
            [integer]: [it will return status of the table creation. if successfully the 0 else 1.]
        """
        cursor = connection.cursor() # Open cursor for database.
        try:
            cursor.execute('CREATE TABLE '+table_name+' ('+schema+');') # Excute create table query.
            connection.commit() # Commit the changes.
            return 0 # If successfully created.
        except (Exception, psycopg2.DatabaseError) as error:
            logging.info(str(error))
            connection.rollback() # Rollback the changes.
            cursor.close() # Close the cursor
            return 1 # If failed.
        
    
    
    def insert_records(self,connection,table_name,row_tuples,cols,column_name=None):
        """This function is used to insert data into database table.

        Args:
            connection ([object]): [object of the database connection.],
            table_name ([string]): [name of the table.],
            row_tuples ([list]): [list of the tuple of record.],
            cols ([string]): [column names in the form of strings.]

        Returns:
            [integer]: [it will return status of the data insertion. if successfully then 0 else 1.]
        """
        


        cols = cols # Get columns name for database insert query.
        tuples = row_tuples # Get record for database insert query.


        cursor = connection.cursor() # Open cursor for database.
        try:
            if column_name == None :
                query = "INSERT INTO %s(%s) VALUES %%s " % (table_name, cols) # Make query
                logging.info(str(table_name) + " <> table_name")
                logging.info(str(cols) + " <> columns")
                logging.info(str(query) + " <> Query")
                logging.info(str(tuples) + " <> tuples")
                extras.execute_values(cursor, query, tuples) # Excute insert query.
                index = 0
            else :
                query = f"INSERT INTO %s(%s) VALUES %%s RETURNING {column_name} " % (table_name, cols) # Make query
                extras.execute_values(cursor, query, tuples) # Excute insert query.
                index = [row[0] for row in cursor.fetchall()][0]
            
            status = 0
            connection.commit() # Commit the changes.
            cursor.close()
            return status,index # If successfully inserted.
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback() # Rollback the changes.
            cursor.close() # Close the cursor.
            logging.error(str(error))
            return 1,None # If failed.

    
    def select_records(self,connection,sql_command):
        """This function is used to retrieve data from database table into dataframe.

        Args:
            connection ([object]): [object of the database connection.],
            sql_command ([string]): [select sql command.]

        Returns:
            [dataframe]: [it will return dataframe of the selected data from the database table.]
        """
        sql_command = str(sql_command) # Get sql command.
        try :
            
           
            data = pd.read_sql(sql_command, connection) # Read data from database table.
            self.update_records(connection,'commit')
            # connection_string = "postgresql://" + user + ":" + password + "@" + host + ":" + port + "/" + database # Make database connection string.
            # engine = create_engine(connection_string) # Create database engine.
            # data = pd.read_sql_query(sql_command, engine) #method of sqlalchemy
            # engine.dispose()
            return data   
        except(Exception, psycopg2.DatabaseError) as error:
            logging.info(str(error) + "check")
            return None
        
       

    def delete_records(self,connection,sql_command):
        """This function is used to delete data from database table.

        Args:
            connection ([object]): [connection object of the database class.],
            sql_command ([string]): [delete sql command]

        Returns:
            [integer]: [it will return stauts of deleted record. if successfully then 0 else 1.]
        """
        
        cursor = connection.cursor() # Open the cursor.
        sql_command = sql_command # Get delete query
        try:
            cursor.execute(sql_command) # Execute the delete query.
            connection.commit() # Commit the changes.
            status = 0 # If Successfully.
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback() # Rollback the changes.
            cursor.close() # Close the cursor.
            status = 1 # If failed
            logger.info(str(error) + " Error in delete record function")
        return status

    def update_records(self,connection,sql_command):
        """This function is used to update records into database.

        Args:
            connection ([object]): [connection for database],
            sql_command ([string]): [query string for update command]

        Returns:
            [integer]: [status of updated records. if successfully then 1 else 0.]
        """
        
        cursor = connection.cursor() # Open the cursor.
        sql_command = sql_command # Get update query
        try:
            cursor.execute(sql_command) # Execute the update query.
            connection.commit() # Commit the changes.
            cursor.close() # Close the cursor.
            status = 0 # If Successfully.
            
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback() # Rollback the changes.
            cursor.close() # Close the cursor.
            status = 1 # If failed
            
            logging.error(str(error))
        return status

    def column_rename(self,file_data_df):
        """This function is used to rename column of dataframe for % , ( , ) this special characters.

        Args:
            file_data_df ([dataframe]): [dataframe of the file data.]

        Returns:
            columns [List of renamed column]: [List of unchanged column]
        """
        df_columns=file_data_df.columns.values
        df_columns_new =[]
        
        for i in df_columns: # this loop check a column name
            str1 =""
            for x in i: # this loop check each character column name
                if '%' in x:
                    str1 += x.replace('%','percent_isg') #It will replace column name when column name contains % 

                elif '(' in x:
                    str1 += x.replace('(','open_Bracket_isg') #It will replace column name when column name contains ( 

                elif ')' in x:
                    str1 += x.replace(')','close_Bracket_isg') #It will replace column name when column name contains )
                    
                else:
                    str1 += x
            df_columns_new.append(str1) # it append the renamed column name

        return df_columns_new ,df_columns # it returns list of changed and unchanged column name

    def load_df_into_db(self,connection_string,table_name,file_data_df,user_name):
        """This function is used to load csv data  into database table.

        Args:
            connection_string ([object]): [connection string of the database connection.],
            table_name ([string]): [name of the table.],
            file_data_df ([dataframe]): [dataframe of the file data.],
            user_name ([string]): [name of the user.]

        Returns:
            [integer]: [it will return status of loaded data into database table. if successfully then 0 else 1.]
        """
    
        engine = create_engine(connection_string) # Create database engine.
        schema_name = user_name.lower()
        try :
            
            file_data_df.to_sql(table_name,engine,schema=schema_name, chunksize=10000) # Load data into database with table structure.
            
            status = 0 # If successfully.
        except Exception as e:
            logging.error("Exception: "+str(e))
            status = 1 # If failed.
            
        return status

    def get_column_names(self, connection, table_name):
        '''
        Returns name of the columns from the given csv table.
        
        Args:
            connection_string ([object]): [connection string of the database connection.],
            table_name ([string]): [name of the table.]
        
        Returns:
            columns ([List of Strings]): [List of Column names]
        '''
        
        col_cursor = connection.cursor()

        # concatenate string for query to get column names
        # SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = 'some_table';
        sql_command = "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE "
        sql_command += "table_name = '{}' order by ordinal_position;".format( table_name )
        
        try:
            # execute the SQL string to get list with col names in a tuple
            col_cursor.execute(sql_command)

            # get the tuple element from the list
            col_names = ( col_cursor.fetchall() )

            columns = []

            # iterate list of tuples and grab first element
            for tup in col_names:

                # append the col name string to the list
                columns += [ tup[0] ]
            
            # close the cursor object to prevent memory leaks
            col_cursor.close()
        except:
            raise NullValue        
        return columns
    
    
    def get_schema_columnlist(self, connection,schema_id,type):
        col_cursor = connection.cursor()
        # sql_command = "select case when changed_column_name='' then column_name else changed_column_name end column_list  from mlaas.schema_tbl where schema_id =1 and column_attribute!='Ignore' order by index" 
        if type=="schema":
            sql_command = "select column_name column_list  from mlaas.schema_tbl where schema_id ="+str(schema_id)+" and column_attribute!='Ignore' order by index"           
        elif type=="Select":
            sql_command = "select case when changed_column_name='' then column_name else changed_column_name end column_list  from mlaas.schema_tbl where schema_id="+str(schema_id)+" and column_attribute='Select' order by index"    
        elif type== "all":
            sql_command = "select column_name, case when changed_column_name='' then column_name else changed_column_name end column_list  from mlaas.schema_tbl where schema_id="+str(schema_id)+" order by index"
            
            #Execute sql query and return dataframe 
            dataframe = self.select_records(connection,sql_command)
            
            #Get the previous column name and changed column name from the schema table
            prev_col_name,current_col_name =list(dataframe['column_name']),list(dataframe['column_list']) 
            return prev_col_name,current_col_name

        else:
            sql_command = "select case when changed_column_name='' then column_name else changed_column_name end column_list  from mlaas.schema_tbl where schema_id="+str(schema_id)+" and column_attribute!='Ignore' order by index"           
        
        logger.info(sql_command)
        try:
            # execute the SQL string to get list with col names in a tuple
            col_cursor.execute(sql_command)

            # get the tuple element from the list
            col_names = ( col_cursor.fetchall() )

            columns = []

            # iterate list of tuples and grab first element
            for tup in col_names:

                # append the col name string to the list
                columns += [ tup[0] ]
            
            # close the cursor object to prevent memory leaks
            col_cursor.close()
        except:
            raise NullValue
        
        return columns
    

    
    def get_order_clause(self,connection,schema_id,table_name,sort_type,sort_index):    
        """ function used to get ORDER by clause string

        Args:
            table_name[(String)] : [Name of the table]
            sort_type[(String)] : [value of the sort type]
            sort_index[(integer)] : [index of column]
        Return : 
            [String,List] : [return the Order clause,list of column name]
        """ 
        if schema_id != None:
            columns_list=self.get_schema_columnlist(connection,schema_id,type="ab") #get the column list   
        else:
            col_table_name=table_name.partition(".")[2] #trim from the string and get the table name
            col_table_name=col_table_name[1:-1]
            columns_list=self.get_column_names(connection,col_table_name) #get the column list    
        if sort_type =="asc" and  str(sort_index) == "0":  #check if value sort_type and sort_index is empty
            order_clause=f'ORDER BY "{columns_list[0]}"'
        else:
            order_clause=f'ORDER BY "{columns_list[int(sort_index)]}" {sort_type}' #formated string for order By clause 
        return order_clause,columns_list
    
    def get_global_search_clause(self,connection,schema_id,columns,global_value):
        """ function used to create search  string for sql command

        Args:
            table_name[(String)] : [Name of the table]
            sort_type[(String)] : [value of the sort type]
            sort_index[(integer)] : [index of column]
        Return : 
            [String] : [return the search pattern string]
        """ 
        if schema_id != None:
            columns_list=self.get_schema_columnlist(connection,schema_id,type="schema") 
            columns=columns_list[1:]
        else:
            columns=columns     
        empty_string=""
        global_value=global_value.lower()
        for i in range(len(columns)):
            empty_string+="lower(cast(\""+str(columns[i])+"\" as varchar)) like '%"+str(global_value)+"%' or "   # create the string with Like operator  
        global_search_clause="("+empty_string[:len(empty_string)-3]+")" # remove the "or" string appended at last 
        return global_search_clause
    
    def get_customfilter(self,connection,customefilter):
        """ function used to get customfilter clause
        Args:
            customefilter ([type]): [dictionary]
        Returns:
            [String]: [retun the custom filter string]
        """
        dict=customefilter
        empty_string=""
        for x in dict:
            if dict[x]!="":
                dict[x]=dict[x].replace("'","''")
                dict[x]=dict[x].lower()
                empty_string+="lower(cast(\""+x+"\" as varchar)) like '%"+dict[x]+"%' or "
        customefilter="("+empty_string[:len(empty_string)-3]+")" # remove the "or" string appended at last 
        return customefilter
    
    def get_query_string(self,connection,schema_id):
        try:
            logging.info("database : DBClass : get_query_string : Execution start")

            # sql command to get details from schema table  based on  schema id 
            sql_command = "select column_name,case when changed_column_name = '' then column_name else changed_column_name end column_list  from mlaas.schema_tbl where schema_id ="+str(schema_id)+"and column_attribute !='Ignore' order by index"
            
            #execute sql commnad if data exist then return dataframe else return None
            schema_df = self.select_records(connection,sql_command) 

            #extract the column name and column_list
            column_name,column_list = schema_df['column_name'],schema_df['column_list']

            string_query = ""
            for count in range(0,len(column_name)):
                #append string column name as alias  column list name
                string_query +='"'+column_name[count]+'" as "'+column_list[count]+'",'
            
            logging.info("database : DBClass : get_query_string : Execution stop")
            return string_query[:len(string_query)-1]
        except  Exception as exc:
            logging.error("database : DBClass : get_query_string : Exception " + str(exc))
            return str(exc)

    
    def pagination(self,connection,table_name,start_index,length,sort_type,sort_index,global_search_value,customefilter,schema_id):
        """ function used to create Sql query string

        Args:
                start_index[(Integer)] : [value of the starting index]
                length[(Integer)] :[value of length of records to be shown]
                sort_type[(String)] : [value of sort_type ascending or descending]
                sort_index[(Integer)] : [index value of the column to perform sorting]
                global_value[(String)] : [value that need be search in table]
                
        Return : 
            [String] : [return the sql query string for data]
            [String] : [return the sql query string for filter row count]
        """
        try: 
            end_index = (start_index + length)-1 #get total length
            limit_index=start_index+length #calculate limit
            order_clause,columns_list=self.get_order_clause(connection,schema_id,table_name,sort_type,sort_index) #call get_order_clause function and get order by string and column list            
            columns=columns_list[1:] #remove first column
            global_search_clause="" #initialize global_search_clause
            if global_search_value!="":
                global_search_clause=self.get_global_search_clause(connection,schema_id,columns,global_search_value)  #call get_global_search_clause function and get search query string
                global_search_clause= "where "+global_search_clause  #add where to global_search_clause
            customefilter=self.get_customfilter(connection,customefilter) #call get_customfilter value
            customefilter_clause="" #initialize customefilter_clause
            if schema_id == None:
                select_clause="*"
            else:
                query = self.get_query_string(connection,schema_id)
                # select_clause=str(columns_list[0])+","+str(query)
                select_clause=str(query)
            if customefilter!='()':
                customefilter_clause="where "+customefilter #add where to customefilter_clause 
            if str(sort_index) != "0" or global_search_value!="" or customefilter_clause!="":  
                if start_index==0:                              #checking column
                    if customefilter_clause !="":
                        sql_data = f'select * from (SELECT {str(select_clause)} From {table_name} {global_search_clause} {order_clause}) as dt {customefilter_clause} {order_clause} limit {length}'   #sql Query with customefilter_clause
                        sql_filtercount = f'select count(*) from (SELECT {str(select_clause)} From {table_name} {global_search_clause} ) as dt {customefilter_clause} ' #sql Query for filter row count                             
                    else:
                        sql_data = f'SELECT {str(select_clause)} From {table_name} {global_search_clause} {order_clause} limit {length}'  #sql Query without customefilter_clause 
                        sql_filtercount = f'SELECT count(*) From {table_name} {global_search_clause}'   #sql Query for filter row count                             
                else:
                    if customefilter_clause !="":
                        sql_data = f'select {str(select_clause)} from (SELECT * From {table_name} {global_search_clause} {order_clause} limit {limit_index} offset {start_index}) as dt {customefilter_clause} {order_clause} limit {length}'  #sql Query with customefilter_clause
                        sql_filtercount = f'select count(*) from (SELECT {str(select_clause)} From {table_name} {global_search_clause}) as dt {customefilter_clause}'#sql Query for filter row count                              
                    else:   
                        sql_data = f'select {str(select_clause)} from (SELECT * From {table_name} {global_search_clause} {order_clause} limit {limit_index} offset {start_index}) as dt limit {length}' #sql Query for filter row count  
                        sql_filtercount = f'select count(*) from (SELECT {str(select_clause)} From {table_name} {global_search_clause}) as dt'  #sql Query for filter row count                                 
            
            else:
                sql_data =  f'SELECT {str(select_clause)} From {table_name} where "{columns_list[0]}" >= {start_index} {order_clause} limit {length}' # sql Query without any filter and clause 
                sql_filtercount = f'SELECT count(*) From {table_name}' #sql Query with customefilter_clause

            logger.info("sql_data===="+str(sql_data))
            return sql_data,sql_filtercount
        except Exception as exc:
            return str(exc) 

    def is_existing_table(self,connection,table_name,schema):
        """ function used to check the table is Exists or Not in database

        Args:
                table_name[(String)] : [Name of the table]
                schema[String] : [Name of the Schema]
        Return : 
            [String] : [return the True if record found else False]
        """
        sql_command = "SELECT 1 FROM information_schema.tables WHERE table_schema ='"+schema+"' AND table_name = '"+table_name+"'"
        data=self.select_records(connection,sql_command) #call select_records which return data if found else None
        print(str(data) + "checking")
        if len(data) == 0: # check whether length of data is empty or not
            self.create_schema(connection)
            return "False"
        else:
            return "True"
    
     

       
    def get_table_name(self,connection,table_name):
        """
        function used to create table name by adding unique sequence number init.
        Args :
                table_name[(String)] : [Name of old table]
        Return :
                [String] : [return the table name]
        """
        logging.info("data ingestion : SchemaClass : get_table_name : execution start")
        split_value = table_name.split('_tbl')[0].split('_')[-1] # Extract the sequence number
        table_name = table_name.split(split_value) # split with the sequence number
        seq = self.get_sequence(connection) #get the sequence number
        table_name = table_name[0]+str(seq['nextval'][0])+table_name[1] #create table name by joining sequence
        logging.info("data ingestion : SchemaClass : get_table_name : execution stop")
        return table_name
    
    def user_authentication(self,connection,user_name,password):
        """[summary]

        Args:
            connection ([String]): [connection String]
            user_name ([String]): [User Name]
            password ([String]): [password]

        Raises:
            UserAuthenticationFailed: [User authentication failed]
        Returns:
            [String]: [if user authenticated then it return True]
        """
        try:
            sql_command = "SELECT user_name from mlaas.user_auth_tbl where user_name='"+ str(user_name) +"' and password='"+ str(password) +"'"
            user_df = self.select_records(connection,sql_command)
            if user_df is None:
                raise UserAuthenticationFailed(500)          
            if len(user_df) > 0 :
                return True
            else:
                raise UserAuthenticationFailed(500)
        except UserAuthenticationFailed as exc:
            return exc.msg
  
    

        
    def change_datatype(self, connection,column_string, table_name,type='float8'):
        """[it will change data type of table]

        Args:
            column_string ([type]): [column name which we want to change type]
            table_name ([type]): [table name]

        Returns:
            [status]: [0,1]
        """
        sql_command = f'ALTER TABLE {table_name} ALTER COLUMN "{str(column_string)}" type "{type}"'
        logger.info("sql_command==="+sql_command) 
        status = self.update_records(connection,sql_command)   
        return status
           
    def get_column_df(self, connection, table_name,column_string):
        
        """[This function return specific column dataframe]

        Returns:
            [pandas df]: [specific column df]
        """
        
        sql_command = f'SELECT "{str(column_string)}" FROM {table_name} order by index'
        data_df = self.select_records(connection,sql_command)   
        return data_df 
    
    
