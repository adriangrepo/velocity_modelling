from velocityhelper.api.dataio import DataIO
from settings import MISSINGCALCSPATH
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class FindMissing(object):

    def __init__(self):

        self.markersPath = MISSINGCALCSPATH+"WellTopData.csv"
        self.topsPath = MISSINGCALCSPATH+"TopToCheckFor.csv"

    def findMissingMarkers(self):
        if self.markersPath == "":
            logger.error("Markers file has not been specified")
            return
        elif self.topsPath == "":
            logger.error("TopsModel file has not been specified")
            return
        dataIO = DataIO()
        markersDf = dataIO.readCSVZeroIndex(self.markersPath)
        if len(markersDf.index)==0:
            logger.error("Markers data is empty")
            return
        markersData = dataIO.getData(markersDf)

        topsDf = dataIO.readCSVZeroIndex(self.topsPath)
        if len(topsDf.index)==0:
            logger.error("TopsModel data is empty")
            return
        topsList = dataIO.topsReader(topsDf)

        wellSurfaces = dataIO.checkMissingSurfaces(markersData, topsList)
        dataIO.writeDictToCSV(wellSurfaces, MISSINGCALCSPATH+"MissingSurfaces_Output.csv")

if __name__ == '__main__':

    findMissing = FindMissing()
    findMissing.findMissingMarkers()

