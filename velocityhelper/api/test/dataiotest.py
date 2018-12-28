import logging
import unittest
import pandas as pd
import numpy.testing as npt

from velocityhelper.api.dataio import DataIO
from velocityhelper.api.surfacemodel import TopsModel
from velocityhelper.api.isomodel import IsoModel
from velocityhelper.api.surfacemodel import SurfaceModel
from velocityhelper.settings import TESTDATAPATH

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

'''
#get nth item from list else default

x[index] if len(x) > index else default

'''
class DataIOTest(unittest.TestCase):

    def setUp(self):

        
        self.functionsPath = TESTDATAPATH+"20150507_Calc_Functions.csv"
        self.markersPath = TESTDATAPATH+"20150504_Markers.csv"
        self.deltaTopPath = TESTDATAPATH+"20150504_Grid_TWT.csv"
        self.deltaBasePath = TESTDATAPATH+"20150504_Grid_Z.csv"
        self.topsPath = TESTDATAPATH+"20150509_Missing_Tops.csv"


    def test_readCSVZeroIndex(self):
        #TODO
        pass

    def test_writeCSV(self):
        logger.debug(">>test_writeCSV")
        dataIO = DataIO()
        isoModel = IsoModel()
        results = []
        for i in range(10):
            isoModel.row=i
            isoModel.well="Well_"+str(i)
            isoModel.calcFunction = "A-B"
            isoModel.isochron = 234.55+i
            isoModel.isopach = 10+i
            isoModel.vint = 1000+10*i
            results.append(isoModel.getDataList())
        self.assertEquals(10, len(results))
        testFile = TESTDATAPATH +"20150507_test_writeCSV.csv"

        results.insert(0, IsoModel.HEADERS)
        dataIO.writeCSV(results, testFile, appendFlag = False)

        #Read data back in and check it
        readBackDf = dataIO.readCSV(testFile)
        assert isinstance(readBackDf, pd.DataFrame) and len(readBackDf.index)>0
        isochrons = []
        isopachs = []
        vints = []
        for i, row in readBackDf.iterrows():
            isochron = row['Isochron']
            isopach = row['Isopach']
            vint = row['Vint']
            isochrons.append(isochron)
            isopachs.append(isopach)
            vints.append(vint)
        npt.assert_allclose(234.55, float(isochrons[0]), rtol=1e-5)
        npt.assert_allclose(19.0, float(isopachs[9]), rtol=1e-5)
        npt.assert_allclose(1050.0, float(vints[5]), rtol=1e-5)


    def test_writeDictToCSV(self):
        #TODO
        pass

    def test_getData(self):
        logger.debug(">test_getData()")
        dataIO = DataIO()
        markersPD = dataIO.readCSVZeroIndex(self.markersPath)
        markerData = dataIO.getData(markersPD)
        angelSurfs = markerData.get("ANGEL_1")
        self.assertEqual("DELA", angelSurfs[0].surfaceName)
        self.assertEqual("ANGEL_1", angelSurfs[0].well)
        #self.assertEqual("marker", angelSurfs[0].surfaceType)
        self.assertEqual(79.9, angelSurfs[0].z)
        self.assertEqual(146.5, angelSurfs[0].twtAuto)

    def test_functionReader(self):
        #TODO
        pass

    def test_topsReader(self):
        dataIO = DataIO()
        tops = TopsModel()
        topsDf = dataIO.readCSVZeroIndex(self.topsPath)
        logger.debug("--() topsDf length: "+str(len(topsDf.index)))
        tops.topsList = dataIO.topsReader(topsDf)

        self.assertEquals(34, len(tops.topsList))
        self.assertEquals("ANGL", tops.topsList[0])

    def test_writeIsoModels(self):
        dataIO = DataIO()
        markersDf = dataIO.readCSVZeroIndex(self.markersPath)
        markersData = dataIO.getData(markersDf)

        topsDf = dataIO.readCSVZeroIndex(self.topsPath)
        topsList = ["DUMMY", "DELA", "BARE"]

        wellSurfaces = dataIO.checkMissingSurfaces(markersData, topsList)
        surfacesList = wellSurfaces["ANGEL_1"]
        self.assertEquals("DUMMY", surfacesList[0])










