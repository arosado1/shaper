# Comparison.py (under construction)
# Compares both methods in Z to Invisible background

import ROOT
import math as m
import sys 
sys.dont_write_bytecode = True
sys.path.append('./modules')
from LoadHistograms import *
from TotalSyst import *
from CalebHistograms import *

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

################################################################################################################################

def Compare(location_1, location_2, location_3):
    """ Returns predictions (with systematics) and z_score """

    binn     =  'Validation'
    methods  =  ['angel', 'caleb']
    regions  =  ['High', 'Low']
    data     =  ['yield', 'syst', 'zscore']

    # histo[method][region][datum]
    histos  =  { m: { r: dict.fromkeys(data) for r in regions } for m in methods } 

    # loading angel yield and stat
    # histos[binn][variable][region]
    temp1 = LoadBinHisto(location_1)
             
    # loading angel syst
    # totalSyst[binn][direction][region]
    temp2 = TotalSyst(location_1)

    #loading caleb yield and syst
    # histos[region][datum]
    temp3 = CalebValHistos(location_2, location_3) 

    # setting histos[method][region][datum]
    for region in regions:

        histos['angel'][region]['yield']  =  temp1[binn]['nj'][region].Clone()
        histos['angel'][region]['syst']   =  temp2[binn]['up'][region].Clone()

        for datum in data:
            if datum == 'zscore':
                continue
            histos['caleb'][region][datum]  =  temp3[region][datum].Clone()

        nbins  =  histos['angel'][region]['yield'].GetNbinsX()
        histos['angel'][region]['zscore']  =  histos['angel'][region]['yield'].Clone()
        histos['caleb'][region]['zscore']  =  histos['caleb'][region]['yield'].Clone()

        for k in range(0, nbins):

            ay  =  histos['angel'][region]['yield'].GetBinContent(k) 
            cy  =  histos['caleb'][region]['yield'].GetBinContent(k)

            ae  =  histos['angel'][region]['yield'].GetBinError(k)
            ce  =  histos['caleb'][region]['yield'].GetBinError(k)

            asy  =  histos['angel'][region]['syst'].GetBinContent(k) -1 
            csy  =  histos['caleb'][region]['syst'].GetBinContent(k) -1

            d  =  ay - cy 
            d /=  m.sqrt(ae**2 + ce**2 + asy**2  + csy**2 )

            #print('bin = {}\nay = {}    cy = {}\nae = {}    ce = {}\nasy = {}    csy = {}\nd = {}\n').format(k, ay, cy, ae, ce, asy, csy, d)

            histos['angel'][region]['yield'].SetBinError(k, m.sqrt( ae**2 + asy**2 ) )
            histos['caleb'][region]['yield'].SetBinError(k, m.sqrt( ce**2 + csy**2 ) )

            histos['angel'][region]['zscore'].SetBinContent(k, d)
            histos['caleb'][region]['zscore'].SetBinContent(k, d)

    # histo[method][region][datum]
    return histos

################################################################################################################################

if __name__ == '__main__':

    methods  =  ['angel', 'caleb']
    regions  =  ['High', 'Low']
    data     =  ['yield', 'syst', 'zscore']

    location_1  =  sys.argv[1]
    location_2  =  sys.argv[2]
    location_3  =  sys.argv[3]

    # histo[method][region][datum]
    histos  =  Compare(location_1, location_2, location_3)

    for region in regions:

        # draw histograms
        c = ROOT.TCanvas("c", "c", 800, 800)
        c.Divide(1, 2)
    
        # histograms
        c.cd(1)
        ROOT.gPad.SetLogy(1)
       
        # ZInv MC and Prediction
        histos['angel'][region]['yield'].SetTitle( '{}#DeltaM Validation Bins Z#rightarrow#nu#nu comparison'.format(region) )

        histos['angel'][region]['yield'].Draw("hist error")
        histos['angel'][region]['yield'].SetLineColor(ROOT.kBlue)

        histos['caleb'][region]['yield'].Draw("hist error same")
        histos['caleb'][region]['yield'].SetLineWidth(1)
        histos['caleb'][region]['yield'].SetLineColor(ROOT.kRed)
    
        # legend: TLegend(x1,y1,x2,y2)
        legend = ROOT.TLegend( 0.75, 0.75, 0.9, 0.9)
        legend.AddEntry( histos['angel'][region]['yield'] , "Dilepton prediction", "l")
        legend.AddEntry( histos['caleb'][region]['yield'] , "Photon prediction", "l")
        legend.Draw()
    
        # ratios
        c.cd(2)
        histos['angel'][region]['zscore'].SetTitle('z-score')
        histos['angel'][region]['zscore'].GetYaxis().SetTitle('#sigma deviations')
        histos['angel'][region]['zscore'].Draw("hist")
    
        # save histograms
        c.Update()
        file_name = "outputs/z_score_validation_" + region + '.png'
        c.SaveAs(file_name)

