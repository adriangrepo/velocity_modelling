import sys
print(sys.path)
import copy
import logging

from velocityhelper.api.surfacemodel import SurfaceModel
from velocityhelper.api.isomodel import IsoModel
from velocityhelper.api.dataio import DataIO
from velocityhelper.api.function import Function
from velocityhelper.api.calculations import Calculations
from settings import ISOCALCSPATH, ATTRIBCALCSOUTPUTPATH, ATTRIBCALCSPATH

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class AttributeCalc(object):
    '''Reads the attributes csv and outputs the attribute (eg DT) per zone
    All zones must be specified in a zones csv file with each zone on top
    of the other (no inter-zone gaps)
    Required columns are: 'TWT auto' and 'Well identifier'
    Data should be sorted on wells, then TWT auto before running
    '''

    def __init__(self):
        self.attributeDataPath = ATTRIBCALCSPATH+"lithostrat_qc_velocity_zones.csv"
        self.zoneDataPath = ATTRIBCALCSPATH + "Zones.csv"
        self.attribute = 'ALL_SONIC_SOOTH'
        #default setting for Petrel (Z is -ve below datum)
        self.negativeZ = True
        self.negativeTWT = True
        self.wellDataDf = None
        self.isoCalcFunctionDf = None
        self.functionList = []

    def runCalcs(self):
        dataIO = DataIO()
        self.wellDataDf = dataIO.readCSVZeroIndex(self.attributeDataPath)
        markerModels = dataIO.getAttributeData(self.wellDataDf, self.attribute, zIsNegative=self.negativeZ, twtIsNegative=self.negativeTWT)

        functionsDf = dataIO.readCSVZeroIndex(self.zoneDataPath)
        self.functionList = dataIO.functionReader(functionsDf)
        calculations = Calculations()
        allModels = []
        isoFunctionName = ""
        modelList = []
        for function in self.functionList:
            isoModels = calculations.doIsoCalculations(function, markerModels)
            if len(isoModels)>0:
                isoFunctionName = isoModels[0].calcFunction
            for item in isoModels:
                modelList.append(item.getDataList())
        if len(modelList) == 0:
            logger.info("No data to output. Check input file is formatted correctly")
        else:
            modelList.insert(0, IsoModel.HEADERS)
            dataIO.writeIsoModels(modelList, ATTRIBCALCSOUTPUTPATH, 'AttributeData', False)


if __name__ == '__main__':
    attributeCalc = AttributeCalc()
    attributeCalc.runCalcs()

