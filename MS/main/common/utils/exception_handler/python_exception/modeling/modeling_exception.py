'''
/*CHANGE HISTORY

 --CREATED BY-------------CREATION DATE-------------VERSION-----------PURPOSE----------------------
 Shivani Bhalodiya        18-FEB-2021                 1.0             Initial Version 
 
 */
'''

class ModelFailed(Exception):
    """Model Failed Exception"""
    def __init__(self,status_code):
        
        self.status_code = status_code
        
        if status_code == "M01":
            self.msg = "Model Training Failed"
             
        elif status_code == "M02" :
            self.msg = "Features Importance calculation Failed"
            
        elif status_code == "M03" :
            self.msg = "Get Actual Prediction Failed"
            
        elif status_code == "M04" :
            self.msg = "save Prediction Failed"
            
        elif status_code == "M05" :
            self.msg = "Performance Matrix Calculation Failed"
            
        elif status_code == "M06" :
            self.msg = "CV Score Calculation Failed"
            
        elif status_code == "M07" :
            self.msg = "Holdout Calculation Failed"
            
        elif status_code == "M08" :
            self.msg = "Model Summary Failed"
            
        elif status_code == "M09" :
            self.msg = "Learning Curve Failed"
            
        elif status_code == "M10" :
            self.msg = "MLFlow Log Artifacts Failed"
        
        elif status_code == "M11":
            self.msg = "Get Confusion Matrix Failed"

        elif status_code == "M12":
            self.msg = "Predict Probability Failed"

        elif status_code == "M13":
            self.msg = "ROC Curve Failed"

        elif status_code == "M14":
            self.msg = "Precision Recall Curve Failed"

        elif status_code == "M15":
            self.msg = "Get Partial Dependence Score Failed"

        elif status_code == "M16":
            self.msg = "Lift Chart Failed"

        else:
            self.msg = "Model failed"
            
        # self.msg = "status_code:" + str(status_code) + ",error_msg:"+self.msg

    def __str__(self):
        return (self.msg)

class ExperimentDosenotExist(Exception):
    """Experiment Does not Exist Exception"""
    def __init__(self,status_code):
        self.msg = "Dataset creation failed"
        self.status_code = status_code
        self.msg = "status_code:" + str(status_code) + ",error_msg:"+self.msg

    def __str__(self):
        return (self.msg)

class ModelIdDosenotExist(Exception):
    """Dataset Creation Failed Exception"""
    def __init__(self,status_code):
        self.msg = "Dataset creation failed"
        self.status_code = status_code
        self.msg = "status_code:" + str(status_code) + ",error_msg:"+self.msg

    def __str__(self):
        return (self.msg)


class DataDosenotExist(Exception):
    """Data Dose Not Exist Exception"""
    def __init__(self,status_code):
        self.msg = "Dataset creation failed"
        self.status_code = status_code
        self.msg = "status_code:" + str(status_code) + ",error_msg:"+self.msg

    def __str__(self):
        return (self.msg)

class ModelIsStillInQueue(Exception):
    """Model Is Still Is In Queue Exception"""
    def __init__(self,status_code):
        self.msg = "Model Is Still In Queue"
        self.status_code = status_code
        self.msg = "status_code:" + str(status_code) + ",error_msg:"+self.msg

    def __str__(self):
        return (self.msg)
        
class ExperimentAlreadyExist(Exception):
    """Experiment Does not Exist Exception"""
    def __init__(self,status_code):
        self.msg = "Experiment Already Exist"
        self.status_code = status_code
        self.msg = "status_code:" + str(status_code) + ",error_msg:"+self.msg

    def __str__(self):
        return (self.msg)
    
class ScaledDataNotFound(Exception):
    """scaling is pending"""
    def __init__(self,status_code):
        self.msg = "scaling is pending"
        self.status_code = status_code
        self.msg = "status_code:" + str(status_code) + ",error_msg:"+self.msg

    def __str__(self):
        return (self.msg)
