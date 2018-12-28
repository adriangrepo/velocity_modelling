from function import Function
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class IsoModel(object):
    ''' Stores calculated data '''

    TWT = 'twt'
    Z = 'z'
    HEADERS = ["Well", "Isochron","IsochronOWTsec","Isopach","Vint","MidPointDepth","MidPointOWT","OWT","Attribute","Top-Base"]

    def __init__(self):
        self.id = 0
        self.well = ""
        self.calcFunction = ""
        self.topSurface = None
        self.baseSurface = None
        self.midPointDepth = 0
        self.midPointOWT = 0
        self.OWT = 0
        self.isochron = 0
        self.isochronOWTsec = 0
        self.isopach = 0
        self.vint = 0
        self.attribute = 0
        self.attributeName = ""

    #deprecated
    def __str__(self):
        return ("{0}, {1}, {2}, {3}, {4}, {5}").format(self.id, self.well, self.calcFunction, self.isochron, self.isopach, self.vint)

    def getDataList(self):
        '''List of calculated data only, so can be formatted for a single csv file row'''
        data = []
        data.append(self.well)
        data.append(self.isochron)
        data.append(self.isochronOWTsec)
        data.append(self.isopach)
        data.append(self.vint)
        data.append(self.midPointDepth)
        data.append(self.midPointOWT)
        data.append(self.OWT)
        data.append(self.attribute)
        data.append(self.calcFunction)
        return data


    def getModelZone(self):
        hasBase = True
        hasTop = True
        baseTopString = ""
        if self.baseSurface == None:
            hasBase = False
            logger.debug(">>getModelZone BaseSurface is None "+self.calcFunction)
        if self.topSurface == None:
            hasTop = False
            logger.debug(">>getModelZone TopSurface is None "+self.calcFunction)
        if hasBase and hasTop:
            baseTopString = self.baseSurface.surfaceName+"-"+self.topSurface.surfaceName
        return baseTopString

    def getWellSet(self, isoModels):
        wells = []
        modelZones = []
        for model in isoModels:
            wells.append(model.well)
            modelZones.append(model.calcFunction)
        wellSet = set(wells)
        modelZoneSet = set(modelZones)
        return wellSet, modelZoneSet

    #deprecated
    '''

    def getZoneCards(self, isoModels):
        # Returns a list of ZoneCards

        wellSet, modelZoneSet = self.getWellSet(isoModels)

        zones = []

        zoneIndex = 0
        for zone in modelZoneSet:
            zoneCard = ZoneCard()

            zoneCard.allRowText = self.getModelCSV(wellSet, isoModels, zone)
            zoneCard.zoneName = zone
            zoneCard.index = zoneIndex
            zoneIndex += 1
            if zoneCard.allRowText:
                zones.append(zoneCard)
        return zones

    def getModelHeader(self, model):
        headerCSV = []
        headerCSV.append('Well')
        headerCSV.append(model.calcFunction+"_"+Function.ISOCHRON)
        headerCSV.append(model.calcFunction+"_"+Function.ISOCHRONOWTSEC)
        headerCSV.append(model.calcFunction+"_"+Function.ISOPACH)
        headerCSV.append(model.calcFunction+"_"+Function.VINT)
        #headerText = ','.join(map(str, headerCSV))
        return headerCSV


    def getModelCSV(self, wellSet, isoModels, zone):
        # put in string list format for writing to CSV file

        allRowText = []
        headerInserted = False
        for model in isoModels:
            if zone == model.calcFunction:
                header = self.getModelHeader(model)
                for well in wellSet:
                    rowData = []
                    if well == model.well:
                        rowData.append(well)
                        rowData.append(model.isochron)
                        rowData.append(model.isochronOWTsec)
                        rowData.append(model.isopach)
                        rowData.append(model.vint)
                    if rowData:
                        #rowCSV = ','.join(map(str, rowData))
                        allRowText.append(rowData)
                #insert heaser at first row
                if not headerInserted:
                    allRowText.insert(0, header)
                    headerInserted = True
        return allRowText
    '''

#deprecated
'''
class ZoneCard(object):
    #allRowText is a list of row CSV's

    def __init__(self):
        self.id = 0
        self.zoneName = ""
        self.allRowText = []

'''


