import sys
sys.path.append("/hoge")

from alfpyclient.handler.mainHandler import AlfrescoHandler

if __name__ == '__main__':
    
    alfHdl      = AlfrescoHandler(url_server='[URL-SEVER]/alfresco', userName='USERNAME', password='PASSWORD')
    client      = alfHdl.connectClient()
    anyNode     = alfHdl.getNode('IDNODE')
    
    #===================================================================================================
    # Download files from Alfresco 
    #===================================================================================================
    alfHdl.downloadChildNodesAll(anyNode)
    
    #===================================================================================================
    # Upload files to Alfresco 
    #===================================================================================================
    alfHdl.uploadFile(url_server_api_upload="[URL-SEVER]/alfresco/service/api/upload",
                      fileName="[FileName]",
                      siteid="ID_SITE",
                      containerid="ID_CONTAINER")