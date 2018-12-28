import os.path

from velocityhelper.api.isomodel import IsoModel
from velocityhelper.api.dataio import DataIO
from velocityhelper.api.function import Function
from velocityhelper.api.calculations import Calculations
from settings import ISOCALCSPATH, ISOCALCSOUTPUTPATH
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class IsoCalc(object):
    ''' Calculates isochron, isopach, midpoint depth, vint ... for the input data file (here the 'wellData' file)
    Top and Base of each zone should be defined in a 'functions file' which includes an index column
    '''

    def __init__(self):

        #tops data
        self.wellDataPath = ISOCALCSPATH+"20150511_WellTopData_no_M13.csv"

        #file containing zones to calculate
        self.isoCalcFunctions = ISOCALCSPATH+"20150514_IsoZones.csv"

        #default setting for Petrel (Z is -ve below datum)
        self.negativeZ = True
        self.wellDataDf = None
        self.isoCalcFunctionDf = None
        self.functionList = []

    def checkFiles(self):
        dataIO = DataIO()
        exists1 = dataIO.checkFileExists(self.wellDataPath)
        exists2 = dataIO.checkFileExists(self.isoCalcFunctions)
        if exists1 and exists2:
            return True


    def runCalcs(self):
        dataIO = DataIO()
        self.wellDataDf = dataIO.readCSVZeroIndex(self.wellDataPath)
        markerModels = dataIO.getData(self.wellDataDf, self.negativeZ)

        functionsDf = dataIO.readCSVZeroIndex(self.isoCalcFunctions)
        self.functionList = dataIO.functionReader(functionsDf)
        calculations = Calculations()
        allModels = []
        isoFunctionName = ""
        for function in self.functionList:
            modelList = []
            isoModels = calculations.doIsoCalculations(function, markerModels)
            if len(isoModels)>0:
                isoFunctionName = isoModels[0].calcFunction
            for item in isoModels:
                modelList.append(item.getDataList())
            modelList.insert(0, IsoModel.HEADERS)
            dataIO.writeIsoModels(modelList, ISOCALCSOUTPUTPATH, isoFunctionName, False)

if __name__ == '__main__':

    isoCalc = IsoCalc()
    if isoCalc.checkFiles():
        isoCalc.runCalcs()

