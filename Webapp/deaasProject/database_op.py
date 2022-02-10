import psycopg2
import psycopg2.extras as extras
import pandas as pd
import logging

class Database_op:
    def __init__(self):
        # Update connection string information
        self.database="citus"
        self.user = "citus" 
        self.password = "Vedity@123"
        self.host = "c.comoscls.postgres.database.azure.com"
        self.port = "5432"
        self.sslmode = "require"
        self.connection_string = "postgresql://" + self.user + ":" + self.password + "@" + self.host + ":" + self.port + "/" + self.database # Make database connection string.
        self.connection = psycopg2.connect(database = self.database, user = self.user , password = self.password, host = self.host, port = self.port) #Get connection object by initializing connection to database. 
        self.cursor = self.connection.cursor()
                
    def start_connection(self):
        conn = psycopg2.connect(database = self.database, user = self.user , password = self.password, host = self.host, port = self.port) #Get connection object by initializing connection to database. 
        self.cursor = self.conn.cursor()    
        return self.conn, self.cursor
    
    def close_connection(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        
    def insert_data(self,dataset_name,project_id,file_name,dataset_file_path,user_id):
        _,cursor = self.start_connection()
        print("Connection established")        
        cursor.execute("INSERT INTO mlaas.dataset_tbl (dataset_name,project_id,file_name,dataset_file_path,created_by) VALUES (%s, %s,%s, %s,%s);", (dataset_name,project_id,file_name,dataset_file_path,user_id))
        print("Row inserted")    
        self.close_connection()                    
        return "Data inserted successfully"

    def get_data(self):
        _,cursor = self.start_connection()
        query = "SELECT * FROM salesforce.account;"
        df = pd.read_sql_query(query, con=self.conn)
        print(df.head())
        self.close_connection()
        return df
    
    def insert_records(self,table_name,row,cols,column_name=None):
        """This function is used to insert data into database table.

        Args:
            connection ([object]): [object of the database connection.],
            table_name ([string]): [name of the table.],
            row_tuples ([list]): [list of the tuple of record.],
            cols ([string]): [column names in the form of strings.]

        Returns:
            [integer]: [it will return status of the data insertion. if successfully then 0 else 1.]
        """
        
        
        row_tuples = [tuple(row)]
        cols = cols # Get columns name for database insert query.
        tuples = row_tuples # Get record for database insert query.


        try:
            if column_name == None :
                query = "INSERT INTO %s(%s) VALUES %%s " % (table_name, cols) # Make query
                logging.info(str(table_name) + " <> table_name")
                logging.info(str(cols) + " <> columns")
                logging.info(str(query) + " <> Query")
                logging.info(str(tuples) + " <> tuples")
                extras.execute_values(self.cursor, query, tuples) # Excute insert query.
                index = 0
            else :
                query = f"INSERT INTO %s(%s) VALUES %%s RETURNING {column_name} " % (table_name, cols) # Make query
                extras.execute_values(self.cursor, query, tuples) # Excute insert query.
                index = [row[0] for row in self.cursor.fetchall()][0]
            
            status = 0
            self.connection.commit() # Commit the changes.
            self.cursor.close()
            return status,index # If successfully inserted.
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback() # Rollback the changes.
            self.cursor.close() # Close the cursor.
            logging.error(str(error))
            return 1,None # If failed.

                  
    def get_user_id(self,user_name):
        
        table_name="mlaas.user_auth_tbl"
        sql_command = "SELECT uid from "+ str(table_name) + " Where user_name = '"+ str(user_name) + "'"
        user_df = self.select_records(sql_command)    
        if len(user_df)>0 :
               user_id = int(user_df['uid'][0])
        else:
               user_id =0
        return user_id
    
    def select_records(self,sql_command):
        """This function is used to retrieve data from database table into dataframe.

        Args:
            connection ([object]): [object of the database connection.],
            sql_command ([string]): [select sql command.]

        Returns:
            [dataframe]: [it will return dataframe of the selected data from the database table.]
        """
        sql_command = str(sql_command) # Get sql command.
        try :
            
           
            data = pd.read_sql(sql_command, self.connection) # Read data from database table.
            # self.update_records(self.connection,'commit')
            return data   
        except(Exception, psycopg2.DatabaseError) as error:
            logging.info(str(error) + "check")
            return None
        
    def delete_records(self,sql_command):
        """This function is used to delete data from database table.

        Args:
            connection ([object]): [connection object of the database class.],
            sql_command ([string]): [delete sql command]

        Returns:
            [integer]: [it will return stauts of deleted record. if successfully then 0 else 1.]
        """
        
        cursor = self.connection.cursor() # Open the cursor.
        sql_command = sql_command # Get delete query
        try:
            cursor.execute(sql_command) # Execute the delete query.
            self.connection.commit() # Commit the changes.
            status = 0 # If Successfully.
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback() # Rollback the changes.
            self.cursor.close() # Close the cursor.
            status = 1 # If failed
            # logger.info(str(error) + " Error in delete record function")
        return status
    
    def update_records(self,sql_command):
        """This function is used to update records into database.

        Args:
            connection ([object]): [connection for database],
            sql_command ([string]): [query string for update command]

        Returns:
            [integer]: [status of updated records. if successfully then 1 else 0.]
        """
        
        try:
            self.cursor.execute(sql_command) # Execute the update query.
            self.connection.commit() # Commit the changes.
            self.cursor.close() # Close the cursor.
            status = 0 # If Successfully.
            
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback() # Rollback the changes.
            self.cursor.close() # Close the cursor.
            status = 1 # If failed
            
            logging.error(str(error))
        return status