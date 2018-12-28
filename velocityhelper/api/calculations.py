import copy
import logging

from isomodel import IsoModel
from surfacemodel import SurfaceModel
from function import Function
import numpy as np

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Calculations(object):
    '''Data calculations  '''

    def doIsoCalculations(self, function, isoCalcsMarkerDict):
        #print(">>doIsoCalculations()")
        assert isinstance(function, Function)
        isoModels = []
        surface = SurfaceModel()
        for well, value in isoCalcsMarkerDict.iteritems():
            topSurface = surface.getSurface(isoCalcsMarkerDict[well], function.top)
            baseSurface = surface.getSurface(isoCalcsMarkerDict[well], function.base)
            if topSurface != None and baseSurface != None:
                #TWT or Z domain
                isoModel = self.computeSingleDiff(well, baseSurface, topSurface)
                isoModel.attribute = topSurface.attribute
                isoModel.attributeName = topSurface.attributeName
                isoModels.append(isoModel)
        return isoModels


    def computeSingleDiff(self, well, baseSurface, topSurface):
        isoModel = IsoModel()
        isoModel.well = well
        isoModel.topSurface = topSurface
        isoModel.baseSurface = baseSurface
        isoModel.isochron = self.calcIsochron(baseSurface, topSurface)
        isoModel.isopach = self.calcIsopach(baseSurface, topSurface)
        isoModel.isochronOWTsec = self.calcIsochronOWTs(baseSurface, topSurface)
        isoModel.calcFunction = self.getZoneText(baseSurface, topSurface)
        vInt = self.computeVint(baseSurface, topSurface)
        isoModel.vint = vInt
        isoModel.midPointDepth = self.calcMidPointDepth(baseSurface, topSurface)
        isoModel.midPointOWT = self.calcMidPointOWT(baseSurface, topSurface)
        isoModel.OWT = self.calcOWT(topSurface)
        return isoModel

    def computeVint(self, baseSurface, topSurface):
        deltaTWT = self.calcIsochron(baseSurface, topSurface)
        deltaZ = self.calcIsopach(baseSurface, topSurface)
        timeSec = self.convertTWTmsToOWTsec(deltaTWT)
        vInt = 0
        if timeSec != 0:
            vInt = deltaZ/timeSec
        return vInt

    def convertTWTmsToOWTsec(self, twt):
        owtSec = float(twt)/2000.0
        return owtSec


    def calcMidPointDepth(self, base, top):
        deltaVal = base.z-top.z
        midPointZ = top.z + deltaVal
        return midPointZ

    def calcMidPointOWT(self, base, top):
        deltaTwt = base.twtAuto-top.twtAuto
        owt = (top.twtAuto)/2
        detlaOwt = deltaTwt/2
        midPointOWT = owt+detlaOwt
        return midPointOWT

    def calcOWT(self, top):
        owt = (top.twtAuto)/2
        return owt

    def getZoneText(self, base, top):
        zoneText =  str(top.surfaceName)+"-"+str(base.surfaceName)
        return zoneText


    def calcIsochron(self, base, top):
        #TWT(ms) isopach
        result = IsoModel()
        deltaTwt = base.twtAuto-top.twtAuto
        #calcFunction =  str(base.surfaceName)+"-"+str(top.surfaceName)+"_"+result.TWT
        return deltaTwt

    def calcIsochronOWTs(self, base, top):
        #OWT(sec) isopach
        result = IsoModel()
        deltaOwts = (base.twtAuto/2000)-(top.twtAuto/2000)
        return deltaOwts

    def calcIsopach(self, base, top):
        result = IsoModel()
        deltaZ = base.z-top.z
        #calcFunction =  str(base.surfaceName)+"-"+str(top.surfaceName)+"_"+result.Z
        return deltaZ

    # Polynomial Regression
    def regression(self, x, y, degree):
        results = {}
        coeffs = np.polyfit(x, y, degree)
         # Polynomial Coefficients
        results['polynomial m, c'] = coeffs.tolist()

        # r-squared
        p = np.poly1d(coeffs)
        #print p
        # fit values, and mean
        yhat = p(x)                         # or [p(z) for z in x]
        ybar = np.sum(y)/len(y)          # or sum(y)/len(y)
        ssreg = np.sum((yhat-ybar)**2)   # or sum([ (yihat - ybar)**2 for yihat in yhat])
        sstot = np.sum((y - ybar)**2)    # or sum([ (yi - ybar)**2 for yi in y])
        results['r2'] = ssreg / sstot
        return results

    def polyCoefficients(self, x, y):
        # fit with np.polyfit
        npx = np.asarray(x)
        npy = np.asarray(y)
        idx = np.isfinite(npx) & np.isfinite(npy)
        coefficients = np.polyfit(npx[idx], npy[idx], 1)
        return coefficients

    def calcVintFromLine(self, coefficients):
        '''Parameter: coeffiecients as ndarray'''
        mc = coefficients.tolist()

    def reciprocal(self, data):
        '''1/item for all items in list'''
        recipData = []
        for item in data:
            if item!=0:
                recip = 1/item
            else:
                recip = 0
            recipData.append(recip)
        return recipData




    '''
    #see DataIO
    def checkMissingSurfaces(self, dataDict):
        wellSurfaces = {}
        for well in dataDict.keys():
            missingSurfaces = []
            for surface in SurfaceModel.TOPS:
                checkedSurface = self.getSurface(dataDict[well], surface)
                if checkedSurface == None :
                    missingSurfaces.append(surface)
            wellSurfaces[well] = missingSurfaces
        return wellSurfaces
    '''
    '''

    def calcDeltaTWT(self, markerData, twtData):
        print(">>calcDeltaTWT()")
        results = []
        for well in markerData.keys():
            print("well list: "+well)
        for well in markerData.keys():
            isoModel = IsoModel()
            isoModel.calcDomain = "TWT"
            for surface in markerData[well]:
                if surface.surfaceType == "marker":
                    try:
                        twtSurfaces = twtData[well]
                        for twtSurf in twtSurfaces:
                            if surface.surfaceName in twtSurf.surfaceName:
                                deltaTWT = twtSurf.twtAuto-surface.twtAuto
                                isoModel.row = twtSurf.row
                                isoModel.well = surface.well
                                calcFunction =  twtSurf.surfaceName+"-"+surface.surfaceName+"_"+isoModel.calcDomain
                                isoModel.calcFunction = calcFunction
                                isoModel.value = deltaTWT
                    except KeyError as e:
                        print("Well {0} not found in twtData".format(well))
            results.append(isoModel)
        return results

    def calcDifference(self, dataDict, top, base, domain):
        print(">>calcDifference()")
        assert isinstance(top, str), 'Top argument of not of String type'
        assert isinstance(base, str), 'Base argument of not of String type'
        results = []
        surface = SurfaceModel()
        for well in dataDict.keys():
            topSurface = surface.getSurface(dataDict[well], top)
            baseSurface = surface.getSurface(dataDict[well], base)
            if topSurface != None and baseSurface != None:
                isoModel = self.computeSingleDiff(well, baseSurface, topSurface, domain)
                results.append(isoModel)
            else:
                pass
        return results

    def computeMultDiff(self, isoModel, baseSurface, topSurface, base, top, domain, distance):
        print(">>computeMultDiff()")
        deltaTotal = 0
        runningSurf = topSurface
        for i in range(distance):
            nextIndex = topSurface.index+i
            nextSurf = self.getSurfaceByIndex(nextIndex)
            calcFunction, deltaVal = self.calcDifDomain(nextSurf, runningSurf, domain)
            deltaTotal += deltaVal
            runningSurf = copy.deepcopy(nextSurf)
        calcFunction =  str(base)+"-"+str(top)+"_"+str(domain)
        isoModel.calcFunction = calcFunction
        isoModel.value = deltaTotal
        return isoModel

    def doVintCalculations(self, function, primaryDict, secondaryDict):
        print(">>doVintCalculations()")
        results = []
        surface = SurfaceModel()
        for well in primaryDict.keys():
            topSurface = surface.getSurface(primaryDict[well], function.top)
            baseSurface = surface.getSurface(primaryDict[well], function.base)
            if topSurface != None and baseSurface != None:
                #Vint gets no domain
                isoModel = self.computeVint(well, baseSurface, topSurface)
                results.append(isoModel)
        return results
    '''


    ''' #deprecated
    def calcDifDomain(self, base, top, domain):
        result = IsoModel()
        if result.TWT == domain.lower():
            calcFunction, deltaVal = self.calcDiffTWT(base, top)
        elif result.Z == domain.lower():
            calcFunction, deltaVal = self.calcDiffZ(base, top)
        else:
            logger.error("Domain is not recognised: "+str(domain))
            calcFunction, deltaVal = "", 0
        return calcFunction, deltaVal
    '''




