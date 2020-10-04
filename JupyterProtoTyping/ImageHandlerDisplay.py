import cv2
import numpy as np

class ImageHandlerDisplay:
    
    def __init__(self):
        print("##Constructor for"+str(__class__.__name__))
        
    @staticmethod
    def displayImage(img,title=""):
        cv2.imshow(title, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    @staticmethod
    def displayImageByMatplotlibWithFileOpen(fileNameImage,title=""):
        img = cv2.imread(fileNameImage, cv2.IMREAD_COLOR)
        ImageHandlerDisplay.displayImageByMatplotlib(img,title)
        del img
        
    @staticmethod
    def displayImageByMatplotlib(img,title=""):
        from PIL import Image
        import matplotlib.pyplot as plt
        import numpy as np
        
        img     = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        im_list = np.asarray(img)
        
        dpi     = 100
        img_w   = img.shape[0]/dpi * 2.0
        img_h   = img.shape[1]/dpi * 2.0
        fig     = plt.figure(dpi=dpi,figsize=(img_w, img_h))
        
        plt.imshow(im_list)
        plt.show()
    
