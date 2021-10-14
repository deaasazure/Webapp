class Error404(Exception):
     def __init__(self):
        self.msg = "Not Found"
        self.status_code = 404
    
class Error400(Exception):
    def __init__(self):
        self.msg = "Bad Request"
        self.status_code = 400

class Error403(Exception):
    def __init__(self):
        self.msg = "Forbidden"
        self.status_code = 403

class Error401(Exception):
    def __init__(self):
        self.msg = "Unauthorized"
        self.status_code = 401

class Error415(Exception):
    def __init__(self):
        self.msg = "UnsupportedMediaType"
        self.status_code = 415