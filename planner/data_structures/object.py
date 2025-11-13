class Object:
    def __init__(self, name, type):
        self.name = name
        self.type = type
        
    def __eq__(self, other):
        return self.name == other.name and self.type == other.type
    
    

class PreconditionObject:
    def __init__(self, name, type,encoding_id):
        self.name = name
        self.type = type
        self.encoding_id = encoding_id
        
    def __eq__(self, other):
        return self.name == other.name and self.type == other.type
    
    
