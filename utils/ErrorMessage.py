class ErrorMessage:
    
    def missing_args(self, args): 
        return {"error": "Missing arguments: {}".format(args)}, 400
    
    def missing_headers(self, headers):
        return {"error": "Missing headers: {}".format(headers)}, 400
    
    def not_found(self, resource):
        return {"error": "Not found: {}".format(resource)}, 404

