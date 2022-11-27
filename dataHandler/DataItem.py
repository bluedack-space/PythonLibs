from pythonLibs.dataHandler.EngUnitConversion import *
from pythonLibs.dataHandler.UnitHandler import *

class DataItem():

    isPhysicalValue_   = None
    isDateTime_        = None
    hasConvertFormula_ = None
    unitName           = None
    unit               = None
    name               = None
    formula            = None
    type               = float
    dataList           = []

    def __init__(self):
        self.initialization()

    def __del__(self):
        self.dataList = None

    def initialization(self):
        self.setPhysicalValue(isPhysicalValue=True)
        self.setConvertFormula(hasConvertFormula=False)

    def isPhysicalValue(self):
        return self.isPhysicalValue_

    def setPhysicalValue(self, isPhysicalValue):
        self.isPhysicalValue_ = isPhysicalValue

    def isDateTime(self):
        return self.isDateTime_

    def setDateTime(self, isDateTime):
        self.isDateTime_ = isDateTime

    def hasConvertFormula(self):
        return self.hasConvertFormula_

    def setConvertFormula(self, hasConvertFormula):
        self.hasConvertFormula_ = hasConvertFormula

    def setName(self,name):
        self.name = name

    def getUnitName(self):
        return self.unitName

    def setUnit(self,unitName):
        self.unitName = unitName
        self.unit = UnitHandler.getUnit(unitName=self.unitName)
        if self.unit=="DateTime":
            self.setDateTime(isDateTime=True)
        else:
            self.setDateTime(isDateTime=False)

    def changeUnit(self,unitNameNew,withDataListConversion=True):
        if withDataListConversion and self.isPhysicalValue():
            for i in range(len(self.dataList)):
                self.dataList[i] = UnitHandler.convertUnit(value=self.getValue(i),unitNameIn=self.getUnitName(),unitNameOut=unitNameNew)
        self.setUnit(unitName=unitNameNew)

    def getType(self):
        return self.type

    def setType(self,type):
        self.type = type
    
    def allocateDataList(self,numData):
        if self.getType() == float:
            self.dataList = [0.0] * numData
        elif self.getType() == int:
            self.dataList = [0] * numData
        elif self.getType() == str:
            self.dataList = [""] * numData

    def setDataList(self,dataList):
        self.dataList = dataList

    def getDataList(self):
        if self.isPhysicalValue():
            return self.dataList
        else:
            dataList = []
            for i in range(len(self.dataList)):
                dataList.append(self.getValueWithConvertByFormula(i))
            return dataList

    def setFormula(self,formula):
        if str(formula)!="nan":
            self.formula = str(formula)
            self.setConvertFormula(hasConvertFormula=True)
            self.setPhysicalValue(isPhysicalValue=False)
        else:
            self.formula = None

    def getValue(self, i):
        if self.isPhysicalValue():
            return self.getValue_Raw(i)
        else:
            return self.getValueWithConvertByFormula(i)

    def getValue_Raw(self, i):
        return self.dataList[i]

    def getValueWithConvertByFormula(self, i):
        return self.getValueWithConvertByFormulaForSpecifiedValue(V=self.dataList[i])

    def getValueWithConvertByFormulaForSpecifiedValue(self, V):
            return eval(str(self.formula))

    def displayData(self):
        print("Data Name:"+str(self.name))
        print("Unit     :"+str(self.unit))
        print("Formula  :"+str(self.formula))
        if len(self.dataList)!=0:
            for i in range(len(self.dataList)):
                print(str(self.getValue(i)))

