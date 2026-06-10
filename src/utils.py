class Utils:
    def __init__(self):
        pass
    
    def load_one_file(self, path):
        path = path + "001.txt"
        
        file = open(path, "r")
        text = file.read()
        file.close()
        
        return text