
from matplotlib import pyplot as plt
from velocityhelper.api.dataio import DataIO
from velocityhelper.api.calculations import Calculations
from settings import ISOCALCSPATH, ISOCALCSOUTPUTPATH, PLOTSOUTPUTPATH
import pandas as pd
import numpy as np
import os
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class IsoPlots(object):
    '''Uses output file from IsoCalcs as input
    Generates a series of crossplots for each zone '''

    #if want to run on single zone
    SINGLE_ZONE_FILE = "ANGL-DNGO.csv"


    def runSingleZonePlot(self):
        dataDf = self.readData(self.SINGLE_ZONE_FILE)
        self.runPlots(dataDf, self.SINGLE_ZONE_FILE)

    def runPlotsOnAllFiles(self):
        dataFiles = []
        for file in os.listdir(ISOCALCSOUTPUTPATH):
            if file.endswith(".csv"):
                logger.debug("Found file: "+str(file))
                dataFiles.append(file)
        if len(dataFiles)>0:
            for file in dataFiles:
                dataDf = self.readData(file)
                self.runPlots(dataDf, file)

    def readData(self, dataFile):
        logger.debug(">>readData() Reading file: "+str(dataFile))
        dataIO = DataIO()
        fullPath = ISOCALCSOUTPUTPATH + dataFile
        dataDf = dataIO.readCSV(fullPath)
        assert isinstance(dataDf, pd.DataFrame) and len(dataDf.index)>0
        return dataDf


    def runPlots(self, dataDf, fileName):
        logger.debug(">>runPlots() Creating plots for: "+str(fileName))
        isochrons = []
        isochronOWTs = []
        isopachs = []
        vints = []
        midPointDepths = []
        midPointOWTs = []
        OWTs = []
        wells = []
        for i, row in dataDf.iterrows():
            well = row['Well']
            isochron = row['Isochron']
            isochronOWT = row['IsochronOWTsec']
            isopach = row['Isopach']
            vint = row['Vint']
            midPointDepth = row['MidPointDepth']
            midPointOWT = row['MidPointOWT']
            OWT = row['OWT']
            wells.append(well)
            isochrons.append(isochron)
            isochronOWTs.append(isochronOWT)
            isopachs.append(isopach)
            vints.append(vint)
            midPointDepths.append(midPointDepth)
            midPointOWTs.append(midPointOWT)
            OWTs.append(OWT)

        calcs = Calculations()
        recipOWTsec = calcs.reciprocal(isochronOWTs)

        baseFile = fileName.split('.', 1)[0]
        chronPachPlotFile = baseFile+'_IsochronIsopach'
        chronVintPlotFile = baseFile+'_IsochronVint'
        pachVintPlotFile = baseFile+'_IsopachVint'
        mpdVintPlotFile = baseFile+'_MPDVint'
        mptVintPlotFile = baseFile+'_MPTVint'
        owtVintPlotFile = baseFile+'_OWTVint'
        recipDelTVintPlotFile = baseFile+'_1DelTVint'

        self.plotFig(isochrons, isopachs, chronPachPlotFile, 'Isochron', 'Isopach', wells)
        self.plotFig(isochrons, vints, chronVintPlotFile, 'Isochron', 'Vint', wells)
        self.plotFig(isopachs, vints, pachVintPlotFile, 'Isopach', 'Vint', wells)

        self.plotFig(midPointDepths, vints, mpdVintPlotFile, 'MidPointDepth', 'Vint', wells)
        self.plotFig(midPointOWTs, vints, mptVintPlotFile, 'MidPointOWT', 'Vint', wells)
        self.plotFig(OWTs, vints, owtVintPlotFile, 'OWT', 'Vint', wells)
        self.plotFig(OWTs, vints, owtVintPlotFile, 'OWT', 'Vint', wells)
        chronOWTsecPachPlotFile = baseFile+'_IsochronOWTsecIsopach'
        self.plotFig(isochronOWTs, isopachs, chronOWTsecPachPlotFile, 'IsochronOWTsec', 'Isopach', wells)
        self.plotFig(recipOWTsec, vints, recipDelTVintPlotFile, '1/DeltaTsec', 'Vint', wells)




    def plotFig(self, x, y, plotFile, xLabel, yLabel, wells):
        #logger.debug(">>plotFig() Plotting graph: "+str(plotFile))
        fig0 = plt.figure()
        ax0 = fig0.add_subplot(111)
        plt.scatter(x,y)
        ax0.set_title(plotFile)
        ax0.set_xlabel(xLabel)
        ax0.set_ylabel(yLabel)
        for i, well in enumerate(wells):
            ax0.annotate(well, (x[i],y[i]), alpha=0.3)
        # fit with np.polyfit
        npx = np.asarray(x)
        npy = np.asarray(y)
        idx = np.isfinite(npx) & np.isfinite(npy)
        coefficients = np.polyfit(npx[idx], npy[idx], 1)
        polynomial = np.poly1d(coefficients)

        calcs = Calculations()

        r2 = calcs.regression(npx[idx], npy[idx], 1)['r2']
        polyAndFit = str(polynomial)+" "+'r2'+" "+str(r2)
        ys = polynomial(npx[idx])
        ax0.text(.95, .01, polyAndFit, verticalalignment='bottom', horizontalalignment='right',
        transform=ax0.transAxes, fontsize=15)
        #print coefficients
        #print polynomial
        #print r2
        plt.plot(npx[idx], ys)

        plt.tight_layout()
        plt.grid()
        #plt.show()

        plt.savefig(PLOTSOUTPUTPATH+plotFile)
        plt.close(fig0)


if __name__ == '__main__':

    isoPlots = IsoPlots()
    #for single zone plots uncomment this
    #isoPlots.runSingleZonePlot()

    #for all zone csv's in directory plots uncomment this
    isoPlots.runPlotsOnAllFiles()