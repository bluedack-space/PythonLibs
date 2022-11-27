import os

from pythonLibs.dataHandler.DataItem import *
import pandas as pd

class DataItemList():

    itemList  = None

    def __init__(self):
        self.initialization()

    def initialization(self):

        if self.itemList is not None:
            del self.itemList

        self.itemList = []
    
    def appendDataItem(self,dataItem):
        self.itemList.append(dataItem)
    
    def appendDataItemBase(self,name,unitName,formula,numData=None):
        item = DataItem()
        item.setUnit(unitName=unitName)
        item.setName(name=name)

        if formula=="nan":
            item.setPhysicalValue(isPhysicalValue=True)
            item.setConvertFormula(hasConvertFormula=False)
        else:
            item.setPhysicalValue(isPhysicalValue=False)
            item.setConvertFormula(hasConvertFormula=True)
            item.setFormula(formula=formula)

        self.appendDataItem(item)

        if numData is not None:
            item.allocateDataList(numData=numData)

    def reader(self,fnameConfig=None):
        if os.path.splitext(fnameConfig)[1]=='.xlsx':
            df      = pd.read_excel(fnameConfig,header=None)
            numVars = df.shape[1]
            for nv in range(numVars):
                name     = str(df.iloc[0,nv])
                unitName = str(df.iloc[1,nv])
                if df.shape[0]==3:
                    formula  = str(df.iloc[2,nv])
                else:
                    formula = "nan"

                # Added by Keiichiro Fujimoto 2022/11/09                 
                self.appendDataItemBase(name=name,unitName=unitName,formulat=formula)

            #self.displayData()

    def setConfig(self,varNameList=None,varUnitList=None,varFormulaList=None):
            numVars = len(varNameList)
            for nv in range(numVars):
                name     = varNameList[nv]
                unitName = varUnitList[nv]
                formula  = varFormulaList[nv]

                if formula == "":
                    formula  = "nan"
                
                # Added by Keiichiro Fujimoto 2022/11/09                 
                self.appendDataItemBase(name=name,unitName=unitName,formulat=formula)

    def displayData(self):
        numVars = len(self.itemList)
        for nv in range(numVars):
            item = self.itemList[nv]
            print("------------------------------")
            item.displayData()

    def getTotalItemNumbers(self):
        return len(self.itemList)

    def getItem(self,index=None):
        return self.itemList[index]

    def setValue(self,icol,irow,value):
        self.itemList[icol].dataList[irow] = value

    def getValue(self,icol,irow):
        return self.itemList[icol].dataList[irow]

    def getIndexByName(self,name=None):
        numVars = len(self.itemList)
        for nv in range(numVars):
            item = self.itemList[nv]
            if item.name==name:
                return nv
        return None

    def getDataAsPandasDataFrame(self,withUnitName=True):

        numVars = len(self.itemList)
        for nv in range(numVars):
            item     = self.itemList[nv]
            dataList = item.getDataList()
            dataList = dataList.copy()

            if nv==0:
                df  = pd.DataFrame(dataList,columns=[item.name])
            else:
                df  = pd.concat([df,pd.DataFrame(dataList,columns=[item.name])], axis=1)

            if withUnitName:
                varName = item.name + "[" + item.unitName + "]"
            else:
                varName = item.name

            #item.displayData()

            df = df.rename(columns={item.name: varName})

        return df

    def generateDataFromPandasDataFrame(self,df,formulaList=None):
        self.initialization()
        numVars = df.shape[1]
        numData = df.shape[0]
        for nv in range(numVars):
            varName   = df.columns[nv]
            item_name = varName.split('[')[0]
            unit_name = varName.split('[')[1].split(']')[0]

            if formulaList==None:
                formula = 'nan'
            else:
                formula = formulaList[nv]

            self.appendDataItemBase(name=item_name,unitName=unit_name,formula=formula,numData=numData)

            for i in range(numData):
                self.itemList[nv].dataList[i] = df.iat[i,nv]
    
    def writeConfig(self,fnameExcelConfig):
        numVars = len(self.itemList)

        df = pd.DataFrame([["" for nv in range(numVars)] for i in range(3)])

        for nv in range(numVars):
            item = self.itemList[nv]
            df.iat[0,nv] = item.name
            df.iat[1,nv] = item.unit
            if item.formula!=None:
                df.iat[2,nv] = item.formula
            else:
                df.iat[2,nv] = ""

        df.to_excel(fnameExcelConfig,header=None,index=None)

    def writeData(self,fnameExcelData):
        numVars = len(self.itemList)
        nv      = 0
        item    = self.itemList[nv]
        numData = len(item.dataList)

        varNameList = [self.itemList[nv].name for nv in range(numVars)]

        df = pd.DataFrame([["" for nv in range(numVars)] for i in range(numData)],columns=varNameList)

        for nv in range(numVars):
            item = self.itemList[nv]
            print(item.dataList)
            for ii in range(len(item.dataList)):
                df.iat[ii,nv] = item.dataList[ii]
        
        df.to_excel(fnameExcelData,index=None)

    def writeDataAndConfigFromPandasDataFrame(self,df=None,fnameExcelConfig=None,fnameExcelData=None):
        self.generateDataFromPandasDataFrame(df=df)
        self.writeConfig(fnameExcelConfig=fnameExcelConfig)
        self.writeData  (fnameExcelData=fnameExcelData)

if __name__ == '__main__':

    dataItemList = DataItemList()

    dataItemList.appendDataItemBase(name="V1",unitName="MPa",formula="nan",numData=100)
    dataItemList.appendDataItemBase(name="V2",unitName="K",  formula="nan",numData=100)
    dataItemList.appendDataItemBase(name="V3",unitName="km", formula="nan",numData=100)

    dataItemList.setValue(icol=0,irow=0,value=1.0)
    dataItemList.setValue(icol=0,irow=1,value=2.0)
    dataItemList.setValue(icol=0,irow=2,value=3.0)

    dataItemList.setValue(icol=1,irow=0,value=10.0)
    dataItemList.setValue(icol=1,irow=1,value=20.0)
    dataItemList.setValue(icol=1,irow=2,value=30.0)

    dataItemList.setValue(icol=2,irow=0,value=100.0)
    dataItemList.setValue(icol=2,irow=1,value=200.0)
    dataItemList.setValue(icol=2,irow=2,value=300.0)

    df = dataItemList.getDataAsPandasDataFrame(withUnitName=True)
    print(df)
    
    dataItemList.generateDataFromPandasDataFrame(df=df)
    df = dataItemList.getDataAsPandasDataFrame(withUnitName=True)
    print(df)
    
    dataItemList.writeConfig(fnameExcelConfig="config.xlsx")
    dataItemList.writeData(fnameExcelData="data.xlsx")

    del dataItemList