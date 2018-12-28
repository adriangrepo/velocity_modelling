
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class SurfaceModel(object):
    '''Stores surface input data '''

    def __init__(self):
        self.row = 0
        self.index = 0
        self.well = ""
        self.surfaceName = ""
        #depth, twt, marker
        self.surfaceType = ""
        self.z = 0
        self.zDelta = 0
        self.twtAuto = 0
        #from petrel attribute export
        self.attribute = 0
        self.attributeName = ""


    def __str__(self):
        return ("{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}").format(self.row, self.well, self.surfaceName, self.surfaceType, self.z, self.zDelta, self.twtAuto, self.sonicVint)



    def __unicode__(self):
        return unicode(str(self))

    def getSurface(self, dataList, surfaceName):
        for surface in dataList:
            if surfaceName == surface.surfaceName:
                return surface
        return None

    def getSurfaceByIndex(self, dataList, surfaceIndex):
        for surface in dataList:
            if surface.index == surfaceIndex:
                return surface
        return None

    def getWellSet(self, surfaceModels):
        wells = []
        modelZones = []
        for model in surfaceModels:
            wells.append(model.well)
        wellSet = set(wells)
        return wellSet

    def getSurfaceNameSet(self, surfaceModelList):
        assert isinstance(surfaceModelList, list)
        zones = []
        zoneSet = []
        for model in surfaceModelList:
            zones.append(model.surfaceName)
        zoneSet = set(zones)
        return zoneSet


    def getAllWellSurfaceNameSet(self, wellSurfaceDict):
        assert isinstance(wellSurfaceDict, dict)
        allSurfaces = []

        for well, surfaceList in wellSurfaceDict.iteritems():
            for surface in surfaceList:
                allSurfaces.append(surface.surfaceName)

        surfaceNameSet = set(allSurfaces)
        return surfaceNameSet

class TopsModel(object):
    '''Keeps a list of tops to check against '''
    def __init__(self):
        self.topsList = []