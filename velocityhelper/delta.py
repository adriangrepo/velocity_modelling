


from velocityhelper.api.deltamodel import DeltaModel

from velocityhelper.api.dataio import DataIO

from settings import DELTACALCSPATH

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Delta(object):

    def __init__(self):
        self.gridPath = DELTACALCSPATH+"20150514_Grids_TWT.csv"
        self.wellTopPath = DELTACALCSPATH+"20150514_Lithostrat_WellTopData.csv"
        self.gridDf = None
        self.wellTopDf = None
        self.negativeZ = False


    def calcDifferences(self):
        dataIO = DataIO()
        self.wellTopDf = dataIO.readCSVZeroIndex(self.wellTopPath)
        wellTopDict = dataIO.getData(self.wellTopDf, self.negativeZ)

        self.gridDf = dataIO.readCSVZeroIndex(self.gridPath)
        gridDict = dataIO.getData(self.gridDf, self.negativeZ)

        deltaList = []
        for gridList in gridDict.values():
            for gridModel in gridList:
                for topList in wellTopDict.values():
                    for topModel in topList:
                        if gridModel.well == topModel.well:
                            if gridModel.surfaceName == topModel.surfaceName:
                                deltaModel = DeltaModel()
                                deltaModel.well = gridModel.well
                                deltaModel.surfaceName = gridModel.surfaceName
                                deltaModel.gridTwt = gridModel.twtAuto
                                deltaModel.wellTwt = topModel.twtAuto
                                deltaModel.gridZ = gridModel.z
                                deltaModel.wellZ = topModel.z
                                deltaModel.deltaTWT = gridModel.twtAuto - topModel.twtAuto
                                deltaModel.deltaZ = ((-1)*gridModel.z) - ((-1)*topModel.z)
                                deltaList.append(deltaModel.getDataList())
        if len(deltaList)>0:
            deltaList.insert(0, DeltaModel.HEADERS)
            dataIO.writeIsoModels(deltaList, DELTACALCSPATH, "DeltaCalcs", False)
        else:
            logger.debug("No matching surfaces found")

    '''
    def writeResults(self, results, appendFlag):
        dataIO = DataIO()
        result = IsoModel()
        resultsCSV = result.getResultsCSV(results)
        dataIO.writeCSV(resultsCSV, self.filePath+results[0].calcFunction+"_calc.csv", appendFlag)
        first = False

    def calcLoop(self, readWb, data,  functionList, domain):
        first = True
        for function in functionList:
            result = IsoModel()
            results = readWb.calcDifference(data, function)
            resultsCSV = result.getResultsCSV(results)
            if first:
                appendFlag=False
            else:
                appendFlag=True
            readWb.writeCSV(resultsCSV, DELTACALCSPATH+"Deltas_Output.csv", appendFlag)
            first = False
    '''

    '''
    def runFunctions(self):
        dataIO = DataIO()
        functionsDf = dataIO.readCSVZeroIndex(self.functionsPath)
        functionList = dataIO.functionReader(functionsDf)
        calculations = Calculations()
        first = True
        for function in functionList:
            if (Function.ISOPACH == function.operation.lower()) or (Function.ISOCHRON == function.operation.lower()):
                if self.markersDf == None:
                    self.markersDf = dataIO.readCSVZeroIndex(self.isoCalcsMarkersPath)
                results = calculations.doIsoCalculations(function, self.markersDf)
            elif Function.VINT == function.operation.lower():
                if self.deltaTopDf == None:
                    self.deltaTopDf = dataIO.readCSVZeroIndex(self.deltaWellTopPath)
                if self.deltaBaseDf == None:
                    self.deltaBaseDf = dataIO.readCSVZeroIndex(self.deltaBaseDf)
                results = calculations.doVintCalculations(function, self.deltaWellTopPath, self.deltaBaseDf)
            self.writeResult(results)
    '''

if __name__ == '__main__':

    delta = Delta()
    delta.calcDifferences()

