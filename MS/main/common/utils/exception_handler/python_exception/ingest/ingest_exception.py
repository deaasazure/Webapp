'''
/*CHANGE HISTORY

 --CREATED BY-------------CREATION DATE-------------VERSION-----------PURPOSE----------------------
 Shivani Bhalodiya        04-JAN-2021                 1.0             Initial Version 
 Abhishek Negi            13-JAN-2021                 1.1             Added SameColumnName class exception
 Abhishek Negi            13-JAN-2021                 1.2             Added SchemaCreationFailed class exception
 */
'''



class DatasetCreationFailed(Exception):
    """Dataset Creation Failed Exception"""
    def __init__(self,status_code):
        self.msg = "Dataset creation failed"
        self.status_code = status_code
        self.msg = "status_code:" + str(status_code) + ",error_msg:"+self.msg

    def __str__(self):
        return (self.msg)

class DatasetDeletionFailed(Exception):
    """Dataset Deletion Failed Exception"""
    def __init__(self,status_code):
        self.msg = "Dataset deletion failed"
        self.status_code = status_code
        self.msg = "status_code:" + str(status_code) + ",error_msg:"+self.msg

    def __str__(self):
        return (self.msg)

class UserAuthenticationFailed(Exception):
    """User Authentication Failed Exception"""
    def __init__(self,status_code):
        self.msg = "User authentication failed"
        self.status_code = status_code
        self.msg = "status_code:" + str(status_code) + ",error_msg:"+self.msg

    def __str__(self):
        return (self.msg)

class ProjectDeletionFailed(Exception):
    """Project Deletion Failed Exception"""
    def __init__(self,status_code):
        self.msg = "Project deletion failed"
        self.status_code = status_code
        self.msg = "status_code:" + str(status_code) + ",error_msg:"+self.msg

    def __str__(self):
        return (self.msg)

class DatasetInUse(Exception):
    """Dataset InUse Failed Exception"""
    def __init__(self,status_code):
        self.msg = "Dataset  is already in use"
        self.status_code = status_code
        self.msg = "status_code:" + str(status_code) + ",error_msg:"+self.msg

    def __str__(self):
        return (self.msg)

class ProjectCreationFailed(Exception):
    """ Project Creation Failed Exception """
    def __init__(self,status_code):
        self.msg = "Project creation failed"
        self.status_code = status_code
        self.msg = "status_code:" + str(status_code) + ",error_msg:"+self.msg

    def __str__(self):
        return (self.msg)

class  ProjectDataNotFound(Exception):
    """  Project Data Not Found. """
    def __init__(self,status_code):
        self.msg = " ProjectData not found"
        self.status_code = status_code
        self.msg = "status_code:" + str(status_code) + ",error_msg:"+self.msg

    def __str__(self):
        return (self.msg)

class DatasetDataNotFound(Exception):
    """ Dataset Data Not Found Exception """
    def __init__(self,status_code):
        self.msg = "Dataset data not found"
        self.status_code = status_code
        self.msg = "status_code:" + str(status_code) + ",error_msg:"+self.msg

    def __str__(self):
        return (self.msg)

class ProjectAlreadyExist(Exception):
    """ Project Already Exist Exception"""
    def __init__(self,status_code):
        self.msg = "Project already exist"
        self.status_code = status_code
        self.msg = "status_code:" + str(status_code) + ",error_msg:"+self.msg

    def __str__(self):
       return (self.msg)

class DatasetAlreadyExist(Exception):
    """ Dataset Already Exist Exception"""
    def __init__(self,status_code):
        self.msg = "Dataset already exist"
        self.status_code = status_code
        self.msg = "status_code:" + str(status_code) + ",error_msg:"+self.msg

    def __str__(self):
        return (self.msg)

		
class LoadCSVDataFailed(Exception):
    """  Load CSV Data Failed"""
    def __init__(self,status_code):
        self.msg = "Load csv data failed"
        self.status_code = status_code
        self.msg = "status_code:" + str(status_code) + ",error_msg:"+self.msg
     
    def __str__(self):
        return (self.msg)
    

class InvalidColumnName(Exception):
    """  Value of column name and change column name cannot be same"""
    def __init__(self,status_code):
        self.msg = "Column name should not contains '('  ')'  or '%' "
        self.status_code = status_code
        self.msg = "status_code:" + str(status_code) + ",error_msg:"+self.msg
     
    def __str__(self):
        return (self.msg)


class SchemaCreationFailed(Exception):
    """  Schema creation failed"""
    def __init__(self,status_code):
        self.msg = "Schema creation failed"
        self.status_code = status_code
        self.msg = "status_code:" + str(status_code) + ",error_msg:"+self.msg
     
    def __str__(self):
        return (self.msg)

class SchemaInsertionFailed(Exception):
    """  Schema Insertion failed"""
    def __init__(self,status_code):
        self.msg = "Schema Insertion failed"
        self.status_code = status_code
        self.msg = "status_code:" + str(status_code) + ",error_msg:"+self.msg
     
    def __str__(self):
        return (self.msg)

class RowsColumnRequired(Exception):
    """  """
    def __init__(self,status_code):
        self.msg = "CSV must have multiple rows and columns"
        self.status_code = status_code
        self.msg = "status_code:" + str(status_code) + ",error_msg:"+self.msg
     
    def __str__(self):
        return (self.msg)

class RawDatasetDeletionFailed(Exception):
    """Dataset Deletion Failed Exception"""
    def __init__(self,status_code):
        self.msg = " Raw dataset deletion failed"
        self.status_code = status_code
        self.msg = "status_code:" + str(status_code) + ",error_msg:"+self.msg

    def __str__(self):
        return (self.msg)

class DatasetColumnUpdateFailed(Exception):
    """Dataset Updation Failed Exception"""
    def __init__(self,status_code):
        self.msg = "Dataset column update failed"
        self.status_code = status_code
        self.msg = "status_code:" + str(status_code) + ",error_msg:"+self.msg

    def __str__(self):
        return (self.msg)

class VariableDatasetCreationFailed(Exception):
    """Dataset Creation Failed Exception"""
    def __init__(self,status_code):
        self.msg = "Variable dataset creation failed"
        self.status_code = status_code
        self.msg = "status_code:" + str(status_code) + ",error_msg:"+self.msg

    def __str__(self):
        return (self.msg)
