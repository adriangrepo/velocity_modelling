
import logging
import unittest

from velocityhelper.isocalc import IsoCalc
from velocityhelper.api.surfacemodel import SurfaceModel
from velocityhelper.api.isomodel import IsoModel
from velocityhelper.settings import TESTDATAPATH


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class IsoCalcTest(unittest.TestCase):
    
    def setUp(self):


        self.wellDataPath = TESTDATAPATH+"20150504_Markers.csv"
        self.isoCalcFunctions = TESTDATAPATH+"20150507_iso_calc_markers.csv"

        self.negativeZ = True
        self.wellDataDf = None
        self.isoCalcFunctionDf = None
        self.functionList = []
        
    def test_runCalcs(self):
        #TODO
        pass