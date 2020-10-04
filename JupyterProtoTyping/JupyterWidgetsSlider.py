from ipywidgets import IntSlider, HBox, interactive_output

class JupyterWidgetsSlider:
    
    widgets = None
    
    def __init__(self):
        print("##Constructor for"+str(__class__.__name__))
    
    def getInstanceOfIntegerSlider(self,min=0,max=15,onUpdate=None):
        self.widgets = IntSlider(min=min, max=max)
        ui           = HBox([self.widgets])
        if onUpdate==None:
            out          = interactive_output(self.ListenerDefault, {'value': self.widgets})
        else:
            out          = interactive_output(onUpdate, {'value': self.widgets})
        display(ui, out)
        return self.widgets
    
    def ListenerDefault(self,value):
        print("value="+str(value))

