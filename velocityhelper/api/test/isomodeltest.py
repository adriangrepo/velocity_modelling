
import logging
import unittest

from velocityhelper.api.surfacemodel import SurfaceModel
from velocityhelper.api.isomodel import IsoModel

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class IsoModelTest(unittest.TestCase):

    def test_getList(self):
        result = IsoModel()
        result.row=0
        result.well="Well_0"
        result.calcFunction = "A-B"
        result.isochron = 260
        result.isochronOWTsec = 1.2
        result.isopach = 500
        result.vint = 400
        result.midPointDepth = 330
        result.midPointOWT = 270
        result.OWT = 200
        result.attribute = 3000
        list0 = result.getDataList()
        list1 = []
        list1.append("Well_0")
        list1.append(260)
        list1.append(1.2)
        list1.append(500)
        list1.append(400)
        list1.append(330)
        list1.append(270)
        list1.append(200)
        list1.append(3000)
        list1.append('A-B')

        self.assertEqual(list1, list0)

    #deprecated
    '''
    def test_getZoneCards(self):
        #Model1
        baseSurface1 = SurfaceModel()
        topSurface1 = SurfaceModel()
        well = "ANGEL_1"
        baseSurface1.well = well
        baseSurface1.surfaceName = "MAND"
        baseSurface1.z = 2000
        baseSurface1.twtAuto = 1000

        topSurface1.well = well
        topSurface1.surfaceName = "TREL"
        topSurface1.z = 1500
        topSurface1.twtAuto = 800

        isomodel1 = IsoModel()
        isomodel1.id = 0
        isomodel1.well = "ANGEL_1"
        isomodel1.calcFunction = "MAND-TREL"
        isomodel1.topSurface = topSurface1
        isomodel1.baseSurface = baseSurface1
        isomodel1.isochron = 200.0
        isomodel1.isopach = 500.0
        isomodel1.vint = 5000.0

        isomodels = []
        isomodels.append(isomodel1)

        zoneCards = isomodel1.getZoneCards(isomodels)
        self.assertEquals("MAND-TREL", zoneCards[0].zoneName)
        self.assertEquals(['Well', 'MAND-TREL_isochron', 'MAND-TREL_isochronOWTsec', 'MAND-TREL_isopach', 'MAND-TREL_vint'], zoneCards[0].allRowText[0])
        self.assertEquals(['ANGEL_1', 200.0, 0, 500.0, 5000.0], zoneCards[0].allRowText[1])


    def test_getModelCSV(self):
        #Model1
        baseSurface1 = SurfaceModel()
        topSurface1 = SurfaceModel()
        well = "ANGEL_1"
        baseSurface1.well = well
        baseSurface1.surfaceName = "MAND"
        baseSurface1.z = 2000
        baseSurface1.twtAuto = 1000

        topSurface1.well = well
        topSurface1.surfaceName = "TREL"
        topSurface1.z = 1500
        topSurface1.twtAuto = 800

        isomodel1 = IsoModel()
        isomodel1.id = 0
        isomodel1.well = "ANGEL_1"
        isomodel1.calcFunction = "MAND-TREL"
        isomodel1.topSurface = topSurface1
        isomodel1.baseSurface = baseSurface1
        isomodel1.isochron = 200.0
        isomodel1.isochronOWTsec = 1.2
        isomodel1.isopach = 500.0
        isomodel1.vint = 5000.0

        isomodels = []
        isomodels.append(isomodel1)

        wellSet = ["ANGEL_1"]

        rowTextList = isomodel1.getModelCSV(wellSet, isomodels, isomodel1.calcFunction)
        self.assertEqual(['ANGEL_1', 200.0, 1.2, 500.0, 5000.0],rowTextList[1])


    def test_getModelHeader(self):
        #Model1
        baseSurface1 = SurfaceModel()
        topSurface1 = SurfaceModel()
        well = "ANGEL_1"
        baseSurface1.well = well
        baseSurface1.surfaceName = "MAND"
        baseSurface1.z = 2000
        baseSurface1.twtAuto = 1000

        topSurface1.well = well
        topSurface1.surfaceName = "TREL"
        topSurface1.z = 1500
        topSurface1.twtAuto = 800

        isomodel1 = IsoModel()
        isomodel1.id = 0
        isomodel1.well = "ANGEL_1"
        isomodel1.calcFunction = "MAND-TREL"
        isomodel1.topSurface = topSurface1
        isomodel1.baseSurface = baseSurface1
        isomodel1.isochron = 200.0
        isomodel1.isopach = 500.0
        isomodel1.vint = 5000.0

        header = isomodel1.getModelHeader(isomodel1)
        self.assertEqual(['Well', 'MAND-TREL_isochron', 'MAND-TREL_isochronOWTsec', 'MAND-TREL_isopach', 'MAND-TREL_vint'],header)

    def test_getResultsCSV(self):
        #Model1
        baseSurface1 = SurfaceModel()
        topSurface1 = SurfaceModel()
        well = "ANGEL_1"
        baseSurface1.well = well
        baseSurface1.surfaceName = "MAND"
        baseSurface1.z = 2000
        baseSurface1.twtAuto = 1000

        topSurface1.well = well
        topSurface1.surfaceName = "TREL"
        topSurface1.z = 1500
        topSurface1.twtAuto = 800

        isomodel1 = IsoModel()
        isomodel1.id = 0
        isomodel1.well = "ANGEL_1"
        isomodel1.calcFunction = "MAND-TREL"
        isomodel1.topSurface = topSurface1
        isomodel1.baseSurface = baseSurface1
        isomodel1.isochron = 200.0
        isomodel1.isopach = 500.0
        isomodel1.vint = 5000.0

        #Model 2
        baseSurface2 = SurfaceModel()
        topSurface2 = SurfaceModel()
        well = "ANGEL_1"
        baseSurface2.well = well
        baseSurface2.surfaceName = "FORE"
        baseSurface2.z = 4000
        baseSurface2.twtAuto = 2000

        topSurface2.well = well
        topSurface2.surfaceName = "MIRI"
        topSurface2.z = 1500
        topSurface2.twtAuto = 800

        isomodel2 = IsoModel()
        isomodel2.id = 1
        isomodel2.well = "ANGEL_1"
        isomodel2.calcFunction = "FORE-MIRI"
        isomodel2.topSurface = topSurface2
        isomodel2.baseSurface = baseSurface2
        isomodel2.isochron = 400.0
        isomodel2.isopach = 500.0
        isomodel2.vint = 4166.666667

        #Model3
        baseSurface3 = SurfaceModel()
        topSurface3 = SurfaceModel()
        well = "ANGEL_2"
        baseSurface3.well = well
        baseSurface3.surfaceName = "MAND"
        baseSurface3.z = 2000
        baseSurface3.twtAuto = 1000

        topSurface3.well = well
        topSurface3.surfaceName = "TREL"
        topSurface3.z = 1500
        topSurface3.twtAuto = 800

        isomodel3 = IsoModel()
        isomodel3.id = 2
        isomodel3.well = "ANGEL_2"
        isomodel3.calcFunction = "MAND-TREL"
        isomodel3.topSurface = topSurface3
        isomodel3.baseSurface = baseSurface3
        isomodel3.isochron = 200.0
        isomodel3.isopach = 500.0
        isomodel3.vint = 5000.0

        isoList = []
        isoList.append(isomodel1)
        isoList.append(isomodel2)
        isoList.append(isomodel3)

        zoneCards = isomodel1.getZoneCards(isoList)

        #for zoneCard in zoneCards:
        #    for i, row in enumerate(zoneCard.allRowText):
        #        logger.debug("index:{0}, text:{1}, zone name:{2}, i:{3}".format(zoneCard.index, row, zoneCard.zoneName, i))
        self.assertEqual(['Well', 'MAND-TREL_isochron', 'MAND-TREL_isochronOWTsec', 'MAND-TREL_isopach', 'MAND-TREL_vint'], zoneCards[0].allRowText[0])
        self.assertEqual("MAND-TREL", zoneCards[0].zoneName)
        self.assertEqual(['ANGEL_1', 200.0, 0, 500.0, 5000.0], zoneCards[0].allRowText[1])
        self.assertEqual(['ANGEL_2', 200.0, 0, 500.0, 5000.0], zoneCards[0].allRowText[2])
        self.assertEqual(['ANGEL_1',400.0,0, 500.0,4166.666667], zoneCards[1].allRowText[1])
        self.assertEqual("FORE-MIRI", zoneCards[1].zoneName)
    '''