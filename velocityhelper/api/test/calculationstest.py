import logging
import unittest

import numpy.testing as npt

from velocityhelper.api.dataio import DataIO
from velocityhelper.api.surfacemodel import SurfaceModel
from velocityhelper.api.isomodel import IsoModel
from velocityhelper.api.calculations import Calculations
from velocityhelper.api.function import Function
from velocityhelper.settings import TESTDATAPATH


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

'''
#get nth item from list else default

x[index] if len(x) > index else default

'''
class CalculationsTest(unittest.TestCase):

    def setUp(self):

        self.isoCalcsMarkersPath = TESTDATAPATH+"20150504_Markers.csv"
        self.deltaTopPath = TESTDATAPATH+"20150504_Grid_TWT.csv"
        self.deltaBasePath = TESTDATAPATH+"20150504_Grid_Z.csv"
        self.functionsPath = TESTDATAPATH+"20150507_Calc_Functions.csv"

    '''
    def test_calcDifference(self):
        logger.debug(">test_calcDifference()")
        dataIO = DataIO()
        markers_df = dataIO.readCSVZeroIndex(self.isoCalcsMarkersPath)
        allWells = markers_df['Well identifier'].tolist()
        uniqueWells = list(set(allWells))
        self.assertEqual(67, len(uniqueWells))

        #grids_twt_df = dataIO.readCSVZeroIndex(self.deltaTopPath)
        twtData = dataIO.getData(markers_df)
        calculations = Calculations()
        self.assertEquals(66, len(twtData.keys()))
        results = calculations.calcDifference(twtData, "BARE", "MAND", "TWT")
        #self.assertEqual(42, len(results))
        found = False
        for resultObject in results:
            if resultObject.well == "ADAMS_1":
                print("Well MAND-BARE: "+str(resultObject.value))
                npt.assert_allclose(1310.84-430.09, resultObject.value, rtol=1e-5)
                self.assertEqual("MAND-BARE_twt", resultObject.calcFunction)

                found = True
        self.assertEqual(True, found)
    '''

    def test_doIsoCalculations(self):
        dataIO = DataIO()

        calculations = Calculations()
        resultObject = IsoModel()
        resultObject.calcDomain = "TWT"

        function = Function()
        function.top = "BARE"
        function.base = "MAND"

        baseSurface1 = SurfaceModel()
        topSurface1 = SurfaceModel()
        well = "ADAMS_1"
        baseSurface1.well = well
        baseSurface1.surfaceName = "MAND"
        baseSurface1.z = 2000
        baseSurface1.twtAuto = 1000

        topSurface1.well = well
        topSurface1.surfaceName = "BARE"
        topSurface1.z = 1500
        topSurface1.twtAuto = 800

        baseSurface2 = SurfaceModel()
        topSurface2 = SurfaceModel()
        well = "ADAMS_2"
        baseSurface2.well = well
        baseSurface2.surfaceName = "MAND"
        baseSurface2.z = 2000
        baseSurface2.twtAuto = 1000

        topSurface2.well = well
        topSurface2.surfaceName = "BARE"
        topSurface2.z = 1500
        topSurface2.twtAuto = 800

        models = []
        models.append(topSurface1)
        models.append(baseSurface1)

        models2 = []
        models2.append(topSurface2)
        models2.append(baseSurface2)
        wellSurfaceData = {}
        wellSurfaceData['ADAMS_1'] = models
        wellSurfaceData['ADAMS_2'] = models2
        isoModels = calculations.doIsoCalculations(function, wellSurfaceData)
        self.assertEquals(2, len(isoModels))
        self.assertEquals("0, ADAMS_2, BARE-MAND, 200, 500, 5000.0",isoModels[0].__str__() )


    def test_computeSingleDiff(self):
        dataIO = DataIO()
        markersPD = dataIO.readCSVZeroIndex(self.isoCalcsMarkersPath)
        markerData = dataIO.getData(markersPD)

        calculations = Calculations()
        resultObject = IsoModel()
        resultObject.calcDomain = "TWT"
        domain = "TWT"
        well = "ADAMS_1"
        surface = SurfaceModel()
        topSurface = surface.getSurface(markerData[well], "BARE")
        baseSurface = surface.getSurface(markerData[well], "MAND")
        self.assertEqual("BARE", topSurface.surfaceName)
        self.assertEqual("MAND", baseSurface.surfaceName)
        resultObject = calculations.computeSingleDiff(well, baseSurface, topSurface)
        logger.debug("fn:{0}".format(resultObject.calcFunction))
        self.assertEqual("BARE-MAND", resultObject.calcFunction)
        npt.assert_allclose(880.75, resultObject.isochron, rtol=1e-5)


    def test_computeVint(self):
        baseSurface = SurfaceModel()
        topSurface = SurfaceModel()
        well = "ANGEL_1"
        baseSurface.well = well
        baseSurface.surfaceName = "MUDE"
        baseSurface.z = 2000
        baseSurface.twtAuto = 1000

        topSurface.well = well
        topSurface.surfaceName = "MIRI"
        topSurface.z = 1500
        topSurface.twtAuto = 800

        calculations = Calculations()
        vint = calculations.computeVint(baseSurface, topSurface)
        npt.assert_allclose(5000.0, vint, rtol=1e-5)


    def test_convertTWTmsToOWTsec(self):
        calculations = Calculations()
        owt = calculations.convertTWTmsToOWTsec(200)
        npt.assert_allclose(0.1, owt, rtol=1e-5)

    def test_calcDifDomain(self):
        pass

    def test_calcDiffTWT(self):
        dataIO = DataIO()
        markersPD = dataIO.readCSVZeroIndex(self.isoCalcsMarkersPath)
        markerData = dataIO.getData(markersPD)
        well = "ADAMS_1"
        surface = SurfaceModel()
        topSurface = surface.getSurface(markerData[well], "BARE")
        baseSurface = surface.getSurface(markerData[well], "TREL")
        npt.assert_allclose(430.09, topSurface.twtAuto, rtol=1e-5)
        npt.assert_allclose(803.45, baseSurface.twtAuto, rtol=1e-5)
        calculations = Calculations()
        deltaVal = calculations.calcIsochron(baseSurface, topSurface)
        calcFunction = calculations.getZoneText(baseSurface, topSurface)
        logger.debug("--test_calcDiffTWT() fn:{0}".format(calcFunction))
        self.assertEqual("BARE-TREL", calcFunction)
        npt.assert_allclose(373.36, deltaVal, rtol=1e-5)


    def test_calcDiffTWT_2(self):
        baseSurface = SurfaceModel()
        topSurface = SurfaceModel()
        well = "ANGEL_1"
        baseSurface.well = well
        baseSurface.surfaceName = "MUDE"
        baseSurface.z = 2000
        baseSurface.twtAuto = 1000

        topSurface.well = well
        topSurface.surfaceName = "MIRI"
        topSurface.z = 1500
        topSurface.twtAuto = 800

        calculations = Calculations()
        deltaTWT = calculations.calcIsochron(baseSurface, topSurface)
        npt.assert_allclose(200.0, deltaTWT, rtol=1e-5)


    def test_calcDiffZ(self):
        baseSurface = SurfaceModel()
        topSurface = SurfaceModel()
        well = "ANGEL_1"
        baseSurface.well = well
        baseSurface.surfaceName = "MUDE"
        baseSurface.z = 2000
        baseSurface.twtAuto = 1000

        topSurface.well = well
        topSurface.surfaceName = "MIRI"
        topSurface.z = 1500
        topSurface.twtAuto = 800

        calculations = Calculations()
        deltaZ = calculations.calcIsopach(baseSurface, topSurface)
        npt.assert_allclose(500.0, deltaZ, rtol=1e-5)














