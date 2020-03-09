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
    """ Compares method 1 with method 2 (Z value) """

    binn     =  'Validation'
    methods  =  ['angel', 'caleb']
    regions  =  ['High', 'Low']
    data     =  ['yield', 'syst']

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
    temp3 = CalebValHisto(location_2, location_3) 

    for region in regions:

        histos['angel'][region]['yield']  =  temp1[binn]['nj'][region]
        histos['angel'][region]['syst']   =  temp2[binn]['up'][region]

        for datum in data:
            histos['caleb'][region][datum]  =  temp3[region][datum]

    # histo[method][region][datum]
    return histos

################################################################################################################################

if __name__ == '__main__':

    methods  =  ['angel', 'caleb']
    regions  =  ['High', 'Low']
    data     =  ['yield', 'syst', 'stat']

    location_1  =  sys.argv[1]
    location_2  =  sys.argv[2]
    location_3  =  sys.argv[3]

    # histo[method][region][datum]
    histos  =  Compare(location_1, location_2, location_3)

    for region in regions:

        nbins    =  histos['angel'][region]['yield'].GetNbinsX()
        z_score  =  histos['angel']['Low']['yield'].Clone()

        for k in range(0, nbins):

            ay  =  histos['angel'][region]['yield'].GetBinContent(k) 
            cy  =  histos['caleb'][region]['yield'].GetBinContent(k)

            ae  =  histos['angel'][region]['yield'].GetBinError(k)
            ce  =  histos['caleb'][region]['yield'].GetBinError(k)

            asy  =  histos['angel'][region]['syst'].GetBinContent(k) 
            csy  =  histos['caleb'][region]['syst'].GetBinContent(k)

            d  =  ay - cy 
            d /=  m.sqrt(ae**2 + ce**2 + asy**2  + csy**2 )

            z_score.SetBinContent(k, d)

    # generating plots 

    # draw histograms
    c = ROOT.TCanvas("c", "c", 800, 800)
    c.Divide(1, 2)

    # histograms
    c.cd(1)
    ROOT.gPad.SetLogy(1) # set log y
   
    # ZInv MC and Prediction
    z_score.Draw("hist error")
    z_score.SetLineColor(ROOT.kBlue)

    # legend: TLegend(x1,y1,x2,y2)
    legend = ROOT.TLegend( 0.75, 0.75, 0.9, 0.9)
    legend.AddEntry(z_score, "Z#rightarrow#nu#nu angel ", "l")
    legend.Draw()

    # ratios
    c.cd(2)
    z_score.Draw("hist")

    # save histograms
    c.Update()
    file_name = "outputs/z_score_validation_" + region + '.png'
    c.SaveAs(file_name)

