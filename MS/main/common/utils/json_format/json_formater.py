import logging
import traceback
from ..logger_handler import custom_logger as cl
user_name = 'admin'
log_enable = True
LogObject = cl.LogClass(user_name,log_enable)
LogObject.log_setting()
logger = logging.getLogger('json_formater')

class JsonFormatClass:
    
    def get_json_format(self,project_dataset_json,column_data):
        """this function used to create a predefined json format where column_data argument will have list
            of column which has to be Display key should be false.
        
        Args:
            project_dataset_json[(list)]:[list of dictonery.]
            column_data[(String)] :[name of the column.]
        return:
            [list] : [list of dictonery]
        """
        try:
            logging.info("Common : JsonFormatClass : get_json_format : execution start")

            final_json_data=[]
            for x in project_dataset_json: #get dict object into a list of object
                    outer_dict={} 
                    key_data=list(x.keys()) # get first list of dictonery key's and convert into list
                    value_data=list(x.values()) # get first list of dictonery value's and convert into list
                    for y in range(len(x)):
                        if isinstance(value_data[y], list): #checking if key has the value List object instace
                            inner_json_data=[]
                            temp_dict={}
                            for j in value_data[y]: #get the list of dictonery
                                inner_outer_dict={} 
                                inner_key_data=list(j.keys()) #get dictonery key's and convert into list
                                inner_value_data=list(j.values())  #get dictonery value's and convert into list
                                for k in range(len(inner_key_data)):
                                    if inner_key_data in column_data: #checking column_data values if present then its display key should be false otherwise True
                                        inside_inner_dict={ inner_key_data[k]:{
                                                "values": inner_value_data[k],
                                                "display":"false",
                                        }}
                                        inner_outer_dict.update(inside_inner_dict) #merge the dictonery with  inside_inner_dict 
                                    else:
                                        inside_inner_dict={ inner_key_data[k]:{
                                                "values": inner_value_data[k],
                                                "display":"true",
                                        }}
                                        inner_outer_dict.update(inside_inner_dict) #merge the dictonery with  inside_inner_dict
                                temp_dict.update(inner_outer_dict) #merge the inner_outer_dict with the outer function temp_dict dictonery
                            inner_json_data.append(temp_dict) # temp_dict append with the inner_json_data list
                            inner_temp_dict={     #inner_json_data list assign as the value of key_data[y]
                                key_data[y]:inner_json_data
                            }
                            outer_dict.update(inner_temp_dict) #inner_temp_dict merge with the main outer_dict dictonery
                        else:
                            if key_data[y] in column_data: #checking column_data values if present then its display key should be false otherwise True
                                inner_dict={ key_data[y]:{
                                        "values":value_data[y],
                                        "display":"false",
                                }}
                                outer_dict.update(inner_dict)
                            else:
                                inner_dict={ key_data[y]:{
                                        "values":value_data[y],
                                        "display":"true",
                                }}
                                outer_dict.update(inner_dict)
                    final_json_data.append(outer_dict) #final outer_dict dictonery append into final_json_data list
            logging.info("Common : JsonFormatClass : get_json_format : execution stop")
            return final_json_data #return custom format data
        except Exception as exc:
            logging.error("data preprocess : SchemaClass : get_json_format : Exception " + str(exc))
            logging.error("data preprocess : SchemaClass : get_json_format : " +traceback.format_exc())
            return str(exc)


    def get_Status_code(self,Status):
        """this function used to extract the status_code and status_msg from the string

        Args:
            Status[(String)]:[ value of status code and error message]
        return:
            [String,String]:[return extracted status_code ,status_msg]
        """
        try:
            logging.info("Common : JsonFormatClass : get_Status_code : execution start")
            status=Status 
            status_code=status.split(",")[0].split(":")[1]
            status_msg=status.split(",")[1].split(":")[1]
            logging.info("Common : JsonFormatClass : get_Status_code : execution stop")
            return status_code,status_msg
        except Exception as exc:
            logging.error("data preprocess : SchemaClass : get_Status_code : Exception " + str(exc))
            logging.error("data preprocess : SchemaClass : get_Status_code : " +traceback.format_exc())
            return str(exc)

    def menu_nested_format(self,dataset_json1,dataset_json2):
        """this function used to create predefind jsonformat where multiple list of dictonery has been passed.

        Args:
            dataset_json1 [(list)] : [list of dictonery with column and records]
            dataset_json2 [(list)] : [list of dictonery with column and records]
        return:
            [list] :[list of dictonery]
        """
        try:
            logging.info("Common : JsonFormatClass : menu_nested_format : execution start")

            column_data=['modulename','parentId','link']
            inside_column_data=['icon','modulename']
            json_data=[]
            final_json_data=[]
            json_data2=[]
            for x in dataset_json1:
                outer_dict={}
                for y in dataset_json2: 
                    if x['id']==y['parentId']:
                        y_keys=list(y.keys())
                        y_data=list(y.values())
                        inner_dict={}
                        for i in range(len(y_keys)):
                            if y_keys[i] not in inside_column_data:
                                inner_dict.update({y_keys[i]:y_data[i]})
                        json_data.append(inner_dict)
                x_keys=list(x.keys())
                x_data=list(x.values())
                for j in range(len(x_keys)):
                    if x_keys[j] not in column_data:
                        outer_dict.update({x_keys[j]:x_data[j]})
                outer_dict.update({"subItems":json_data})
                final_json_data.append(outer_dict)
                json_data=[]
            final_json_data.insert(0,{"id": 1,
                "label": 'MENU',
                "isTitle": 'true'      
            })
            final_json_data.insert(7,{"id": 7,
                "label": 'Modeling',
                "link":"/modeling/type",
                "icon": 'mdi-database-export',
                "subItems": []
            })
            
            logging.info("Common : JsonFormatClass : menu_nested_format : execution stop")
            return final_json_data
        except Exception as exc:
            logging.error("data preprocess : SchemaClass : menu_nested_format : Exception " + str(exc))
            logging.error("data preprocess : SchemaClass : menu_nested_format : " +traceback.format_exc())
            return str(exc)

    def get_column_name(self,column_list):
        """this function used to create a List of  dictonery where every column name  having its key as "data".

        Args:
            column_name [(list)] : [list of column name]
            
        return:
            [list] :[return the list of dictonery]
        """
        try:
            logging.info("Common : JsonFormatClass : get_column_name : execution start")
            json_list=[]
            for name in column_list:
                temp_dict ={
                    "data" : name
                }
                json_list.append(temp_dict)
            logging.info("Common : JsonFormatClass : get_column_name : execution stop")
            return json_list
        except Exception as exc:
            logging.error("data preprocess : SchemaClass : get_column_name : Exception " + str(exc))
            logging.error("data preprocess : SchemaClass : get_column_name : " +traceback.format_exc())
            return str(exc)

    def get_schema_format(self,index,column_name,data_type,column_attribute,date_format):
        """
        function will get all updated column name and column list which are available in the dataset.
        Args : 

        Return :
                [list] :[return the list of dictonery] 
        """
        try:
            logging.info("Common : JsonFormatClass : get_schema_format : execution start")
            json_data = []
            for x in range(len(index)):
                    temp_dict = {
                        "index" : index[x],
                        "column_name":column_name[x],
                        "data_type":data_type[x],
                        "column_attribute":column_attribute[x],
                        "change_column_name":"",
                        "date_format": date_format[x]
                    }
                    json_data.append(temp_dict)
            logging.info("Common : JsonFormatClass : get_schema_format : execution stop")
            return json_data
        except Exception as exc:
            logging.error("data preprocess : SchemaClass : get_schema_format : Exception " + str(exc))
            logging.error("data preprocess : SchemaClass : get_schema_format : " +traceback.format_exc())
            return str(exc)
