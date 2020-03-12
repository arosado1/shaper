# Comparison_diError.py (under construction)
# Compares both methods in Z to Invisible background

import ROOT
import math as m
import sys 
sys.dont_write_bytecode = True
sys.path.append('./modules')
from LoadHistograms import *
from TotalSyst import *
from CalebHistograms import *
from Prediction import *

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

################################################################################################################################

def Compare(location_a, location_c):
    """ Returns predictions table and z_score plot """

    binns       =  ['Validation']
    regions     =  ['High', 'Low']
    directions  =  ['up','down']

    # zscore[binn][region]
    zscore  =  { b: dict.fromkeys(regions) for b in binns }

    # histos[binn][region] (loading angel yield and stat)
    yield_a  =  Yield(location_a)
             
    # totalSyst[binn][direction][region] (loading angel syst)
    syst_a  =  TotalSyst(location_a)

    # histos[binn][region], syst[binn][region][direction] 
    yield_c, syst_c  =  CalebHists(location_c) 

    for binn in binns:
        for region in regions:

            nbins  =  yield_a[binn][region].GetNbinsX()

            zscore[binn][region]  =  yield_a[binn][region].Clone()

            for k in range(0, nbins):

                a   =  yield_a[binn][region].GetBinContent(k) 
                c   =  yield_c[binn][region].GetBinContent(k)

                ae  =  yield_a[binn][region].GetBinError(k)
                ce  =  yield_c[binn][region].GetBinError(k)

                d  =  a - c

                if ( d > 0 ):

                    asy  =  syst_a[binn]['down'][region].GetBinContent(k) -1 
                    csy  =  syst_c[binn][region]['up'].GetBinContent(k) -1

                elif ( d < 0 ):

                    asy  =  syst_a[binn]['up'][region].GetBinContent(k) -1 
                    csy  =  syst_c[binn][region]['down'].GetBinContent(k) -1

                elif ( d == 0 ):

                    print('\nd == 0 has occured\n')
                
                d /=  m.sqrt( ae**2 + ce**2 + asy**2  + csy**2 )

            #print('bin = {}\nay = {}    cy = {}\nae = {}    ce = {}\nasy = {}    csy = {}\nd = {}\n').format(k, ay, cy, ae, ce, asy, csy, d)

            zscore[binn][region].SetBinContent(k, d)
            zscore[binn][region].SetBinContent(k, d)

    print('zscore calculation completed')

    # zscore[binn][region]
    return zscore

################################################################################################################################

if __name__ == '__main__':

    binn       =  'Validation'
    methods    =  ['angel', 'caleb']
    regions    =  ['High', 'Low']
    direction  =  ['up','down']

    location_a  =  sys.argv[1]
    location_c  =  sys.argv[2]

    # histos[binn][region]
    zscore  =  Compare(location_a, location_c)

    for region in regions:

        # draw histograms
        c = ROOT.TCanvas("c", "c", 800, 800)
        c.Divide(1, 2)
    
        # histograms
        c.cd(1)
        ROOT.gPad.SetLogy(1)

        angel  =  Yield(location_a)
        caleb, nope  =  CalebHists(location_c)
       
        # ZInv MC and Prediction
        angel[binn][region].SetTitle( '{}#DeltaM Validation Bins Z#rightarrow#nu#nu comparison'.format(region) )

        angel[binn][region].Draw("hist error")
        angel[binn][region].SetLineColor(ROOT.kBlue)

        caleb[binn][region].Draw("hist error same")
        caleb[binn][region].SetLineWidth(1)
        caleb[binn][region].SetLineColor(ROOT.kRed)
    
        # legend: TLegend(x1,y1,x2,y2)
        legend = ROOT.TLegend( 0.75, 0.75, 0.9, 0.9)
        legend.AddEntry( angel[binn][region] , "Dilepton prediction", "l")
        legend.AddEntry( caleb[binn][region] , "Photon prediction", "l")
        legend.Draw()
    
        # ratios
        c.cd(2)
        zscore[binn][region].SetTitle('z-score')
        zscore[binn][region].GetYaxis().SetTitle('#sigma deviations')
        zscore[binn][region].SetLineColor(ROOT.kBlue)
        zscore[binn][region].Draw("hist")
    
        # save histograms
        c.Update()
        file_name = "outputs/z_score_validation_" + region + '.png'
        c.SaveAs(file_name)

        c.Close()

