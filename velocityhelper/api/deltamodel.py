
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class DeltaModel(object):
    ''' Stores calculated data '''

    HEADERS = ["Well", "Surface","Grid TWT","Grid Z","Well TWT","Well Z","Delta TWT", "Delta Z"]

    def __init__(self):
        self.id = 0
        self.well = ""
        self.surfaceName = None
        self.gridTwt = 0
        self.gridZ = 0
        self.wellTwt = 0
        self.wellZ = 0
        self.deltaTWT = 0
        self.deltaZ = 0

    def getDataList(self):
        '''List of calculated data only, so can be formatted for a single csv file row'''
        data = []
        data.append(self.well)
        data.append(self.surfaceName)
        data.append(self.gridTwt)
        data.append(self.gridZ)
        data.append(self.wellTwt)
        data.append(self.wellZ)
        data.append(self.deltaTWT)
        data.append(self.deltaZ)
        return data