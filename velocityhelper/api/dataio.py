import csv
import copy
import logging
import os
import pandas as pd

from surfacemodel import SurfaceModel, TopsModel
from attributemodel import AttributeModel
from function import Function
from velocityhelper.api.isomodel import IsoModel
import velocityhelper.settings as settings


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class DataIO(object):
    '''CSV file reader, parser, writer  '''

    def checkFileExists(self, filePath):
        exists = True
        assert isinstance(filePath, str)
        if not os.path.isfile(filePath):
            logger.debug("--checkFileExists() File not found: "+filePath)
            exists = False
        return exists

    def readCSVZeroIndex(self, fileName):
        df = pd.read_csv(fileName, index_col=0)
        #remove double quotes from cells - added by OpenOffice to text cells
        df.apply(lambda s:s.str.replace('"', ""))
        if len(df.index)==0:
            logger.error("Error reading file or file is empty: "+fileName)
        return df

    def readCSV(self, fileName):
        try:
            df = pd.read_csv(fileName)
            #remove double quotes from cells - added by OpenOffice to text cells
            df.apply(lambda s:s.str.replace('"', ""))
            if len(df.index)==0:
                logger.error("Error reading file or file is empty: "+fileName)
        except IOError as e:
            logger.error("Could not read file: {0} {1}".format(fileName, e))
            df = None
        return df

    def read_data(self, fileName):
        with open(fileName, 'r') as f:
            parsed_data = [row for row in csv.reader(f.read().splitlines())]
        return parsed_data



    def printResults(self, results):
        print(">>printResults")
        for data in results:
            print(data)

    def writeCSV(self, results, fileName, appendFlag):
        print(">>writeCSV {0}".format(fileName))
        if appendFlag:
            typeWrite = 'a'
        else:
            #w is write, b is a windows binary mode flag
            typeWrite = 'wb'
        with open(fileName, typeWrite) as csv_file:
            csv_writer = csv.writer(csv_file, dialect='excel')
            for row in results:
                csv_writer.writerow(row)
            logger.info("Data written to file: "+str(fileName))


    def writeDictToCSV(self, results, fileName):
        print(">>writeDictToCSV {0}".format(fileName))
        with open(fileName, 'wb') as csv_file:
            csv_writer = csv.writer(csv_file, dialect='excel')
            for key, value in results.iteritems():
                csv_writer.writerow([key])
                csv_writer.writerow(value)

    def writeIsoModels(self, isoModels, filePath, isoFunctionName, appendFlag):
        assert len(isoModels)>0
        zoneFilePath = filePath+isoFunctionName+".csv"
        self.writeCSV(isoModels, zoneFilePath, appendFlag)

        #zoneCards = isoModel.getZoneCards(isoModels)
        #for zoneCard in zoneCards:
        #    zoneFilePath = filePath+zoneCard.zoneName+".csv"
        #    self.writeCSV([zoneCard.allRowText], zoneFilePath, appendFlag)


    def getData(self, df, zIsNegative = True, twtIsNegative = False):
        '''df is a Pandas dataframe
        zIsNegative is the default out of Petrel
        returns a well, surfaceModel dict object'''
        assert isinstance(df, pd.DataFrame) and len(df.index)>0
        wellSurfaceData = {}
        try:
            oldWellId = df[settings.PETREL_SPREADSHEET_WELL_HEADER].iloc[0]
            surfaceList = []
            j = 0
            rowCounter = 0
            for i, row in df.iterrows():
                #logger.debug(row)
                try:
                    surface = SurfaceModel()

                    wellId  = row[settings.PETREL_SPREADSHEET_WELL_HEADER]
                    surface.index = j
                    j += 1
                    surfaceName = row[settings.PETREL_SPREADSHEET_ZONE_HEADER]
                    surface.surfaceName = surfaceName
                    z    = row['Z']
                    surface.z = (-1)*z
                    twtAuto = row['TWT auto']
                    if twtIsNegative:
                        surface.twtAuto = (-1)*twtAuto
                    else:
                        surface.twtAuto = twtAuto
                    surface.row = row
                    surface.well = wellId

                    surface.index = j
                    #logger.debug("--getData() rowCounter: "+str(rowCounter)+" j: "+str(j)+" len(df.index): "+str(len(df.index))+" wellid: "+str(wellId)+" oldWellId: "+str(oldWellId))
                    if rowCounter == len(df.index)-1:
                        #logger.debug("Setting wellSurfaceData[wellId] = listCopy")
                        listCopy = copy.deepcopy(surfaceList)
                        wellSurfaceData[wellId] = listCopy
                    elif wellId == oldWellId:
                        #logger.debug("Appending Surface")
                        surfaceList.append(surface)
                    else:
                        #logger.debug("Setting wellSurfaceData[oldwellId] = listCopy, appending surface to new list, resetting j counter")
                        listCopy = copy.deepcopy(surfaceList)
                        wellSurfaceData[oldWellId] = listCopy
                        surfaceList = []
                        surfaceList.append(surface)
                        j = 0
                    oldWellId = wellId
                    rowCounter += 1
                except KeyError as ke:
                    template = "KeyError. Arguments:\n{0!r}"
    	            message = template.format(ke.args)
                    logger.debug("Column header name is missing. Can't parse data "+message)

                except AttributeError as e:
                    print (e)
        except KeyError as ke:
            template = "KeyError. Arguments:\n{0!r}"
    	    message = template.format(ke.args)
            logger.debug("--getData() Column header name is missing. Can't parse data "+message)
        return wellSurfaceData

    def getAttributeData(self, df, attributeName, zIsNegative = True, twtIsNegative = True):
        assert isinstance(df, pd.DataFrame) and len(df.index)>0
        wellSurfaceData = {}

        oldWellId = df[settings.PETREL_SPREADSHEET_WELL_HEADER].iloc[0]
        surfaceList = []
        j = 0
        for i, row in df.iterrows():
            try:
                surface = SurfaceModel()
                wellId  = row[settings.PETREL_SPREADSHEET_WELL_HEADER]
                surface.attribute = row[attributeName]
                surface.attributeName = attributeName

                surface.index = j
                j += 1
                surfaceName = row[settings.PETREL_SPREADSHEET_ZONE_HEADER]
                surface.surfaceName = surfaceName

                z    = row['Z']
                surface.z = (-1)*z
                #TWT is -ve for attribute export
                twtAuto = row['TWT auto']
                if twtIsNegative:
                    surface.twtAuto = (-1)*twtAuto
                else:
                    surface.twtAuto = twtAuto
                surface.row = row
                surface.well = wellId

                surface.index = j
                if i == len(df.index)-1:
                    listCopy = copy.deepcopy(surfaceList)
                    wellSurfaceData[wellId] = listCopy
                elif wellId == oldWellId:
                    surfaceList.append(surface)
                else:
                    listCopy = copy.deepcopy(surfaceList)
                    wellSurfaceData[oldWellId] = listCopy
                    surfaceList = []
                    surfaceList.append(surface)
                    j = 0
                oldWellId = wellId
            except KeyError as ke:
                template = "KeyError. Arguments:\n{0!r}"
    	        message = template.format(ke.args)
                logger.debug("--getAttributeData() Column header name is missing. Can't parse data "+message)

            except AttributeError as e:
                print (e)

        return wellSurfaceData

    def getZones(self, df):
        '''df is a Pandas dataframe
        returns a zone list'''
        assert isinstance(df, pd.DataFrame) and len(df.index)>0
        zoneList = []
        for i, row in df.iterrows():
            try:
                zone  = row['Zone']
                zoneList.append(zone)


            except KeyError as ke:
                template = "KeyError. Arguments:\n{0!r}"
    	        message = template.format(ke.args)
                logger.debug("--getZones() Column header name is missing. Can't parse data "+message)
        return zoneList

    #deprecated
    def functionReader(self, df):
        assert isinstance(df, pd.DataFrame) and len(df.index)>0
        logger.debug(">>functionReader() dataframe shape: "+str(df.shape))
        functionList = []
        j = 0
        try:
            for i, row in df.iterrows():
                funct = Function()
                funct.row = i
                funct.index = j
                j += 1
                funct.top = row['Top']
                funct.base = row['Base']
                logger.debug("row: {0} top: {1} base: {2}".format(funct.row, funct.top, funct.base))
                functionList.append(funct)
        except AttributeError as e:
            template = "AttributeError. Arguments:\n{0!r}"
    	    message = template.format(e.args)
            logger.debug(message)
        except KeyError as ke:
            template = "KeyError. Arguments:\n{0!r}"
    	    message = template.format(ke.args)
            logger.debug("Column header name is missing. Can't parse data "+message)
        return functionList

    def topsReader(self, df):
        assert isinstance(df, pd.DataFrame) and len(df.index)>0
        topsList = []
        try:
            for i, row in df.iterrows():
                markerTop  = row["Tops"]
                topsList.append(markerTop)
        except AttributeError as e:
            template = "AttributeError. Arguments:\n{0!r}"
    	    message = template.format(e.args)
            logger.debug(message)
        except KeyError as ke:
            template = "KeyError. Arguments:\n{0!r}"
    	    message = template.format(ke.args)
            logger.debug("Column header 'TopsModel' not found. Can't parse data. "+message)
        return topsList

    def checkMissingSurfaces(self, dataDict, topsList):
        logger.debug(">>checkMissingSurfaces()")
        surface = SurfaceModel()
        wellSurfaces = {}

        for well in dataDict.keys():
            missingSurfaces = []
            for top in topsList:
                checkedSurface = surface.getSurface(dataDict[well], top)
                if checkedSurface == None :
                    missingSurfaces.append(top)
            wellSurfaces[well] = missingSurfaces
        if len(wellSurfaces) == 0:
            logger.info("No missing surfaces")
        return wellSurfaces


    def headers(self):
        HEADERS = ["row", "Well", "SurfaceModel", "SurfaceModel type", "Z", "TWT"]
        CALC_HEADERS = ["row", "Well", "Function", "IsoModel"]

