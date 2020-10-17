from alfpyclient.common.connections import connect
from alfpyclient.api.nodes import NodesAPI

class AlfrescoHandler():
    url_server = None
    id_node    = None
    userName   = None
    password   = None
    client     = None
    node       = None
    nodesApi   = None
    
    def __init__(self,url_server,userName,password):
        self.setURLServer(url_server)
        self.setUserName(userName)
        self.setPassword(password)
        
    def __del__(self):
        if self.nodesApi !=None:
            del self.nodesApi
            
        if self.client !=None:
            del self.client
        
    def setURLServer(self,url_server=None):
        self.url_server = url_server
        
    def setIdNode(self,id_node=None):
        self.id_node = id_node
        
    def setUserName(self,userName=None):
        self.userName = userName
        
    def setPassword(self,password=None):
        self.password = password
        
    def connectClient(self):
        if self.client == None:
            self.client = connect(self.url_server, userName=self.userName, password=self.password)
        if self.nodesApi==None:
            self.nodesApi = NodesAPI(self.client)
        return self.client
    
    def getNode(self,idNode=None):
        node     = self.nodesApi.getNode(idNode)
        return node
    
    def getCompanyHome(self):
        return self.nodesApi.getCompanyHome()
    
    def getSharedFiles(self):
        return self.nodesApi.getSharedFiles()
    
    def getMyFiles(self):
        return self.nodesApi.getMyFiles()
    
    def getNodeId(self,node):
        return node.id
    
    def getNodeName(self,node):
        return node.name
    
    def getNodeNodeType(self,node):
        return node.nodeType
    
    def getNodeName(self,node):
        return node.name
    
    def isNodeFolder(self,node):
        return node.isFolder
    
    def isNodeFile(self,node):
        return node.isFile
    
    def downloadNode(self,node):
        print("Down Loading... : "+node.name)
        with open('./' + node.name, 'wb') as f:
            node.downloadContent(f)
            
    def downloadChildNodesAll(self,node):
        folderContents = node.childAssociations['cm:contains']
        for node_cld in folderContents:
            self.downloadNode(node_cld)
            
    def uploadFile(self,url_server_api_upload=None,fileName=None,siteid=None,containerid=None):
        import json
        import requests
        auth  = (self.userName, self.password)
        files = {"filedata": open(fileName, "rb")}
        data  = {"siteid": siteid, "containerid": containerid}
        r = requests.post(url_server_api_upload, files=files, data=data, auth=auth)
        print(r.status_code)
        print(json.loads(r.text))
        
