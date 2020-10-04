import ipywidgets as widgets
import os

class JupyterWidgetsFileUploader:

    widgets = None 
    FileNameUploaded  = None
    FileNameDefault   = None
    
    def __init__(self):
        print("##Constructor for"+str(__class__.__name__))
    
    def getInstance(self,FileNameDefault=None):
        self.FileNameDefault  = FileNameDefault
        s = widgets.FileUpload(
            accept='',      # Accepted file extension e.g. '.txt', '.pdf', 'image/*', 'image/*,.pdf'
            multiple=True   # True to accept multiple files upload else False
        )
        s.style.button_color = "lightgreen"
        self.widgets = s
        s.observe(self.ListenerDefault, names='value')
        return s
    
    def ListenerDefault(self,b):
        self.widgets.style.button_color = "yellow"
        for elem in b.new.values():
            self.FileNameUploaded = elem['metadata']['name']
            print(self.FileNameUploaded)
            with open(elem['metadata']['name'], 'wb') as file:
                file.write( elem['content'])
            print("Upload has been completed...")
            if self.FileNameDefault!=None:
                print("Uploaded File has been renamed...")
                os.rename(os.getcwd()+"/"+self.FileNameUploaded,os.getcwd()+"/"+self.FileNameDefault)
                
        self.widgets.style.button_color = "lightgreen"
        
# from JupyterWidgetsFileUploader import *
# hdl = JupyterWidgetsFileUploader()
# s  = hdl.getInstance("input.jpg")
# s

