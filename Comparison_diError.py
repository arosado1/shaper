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

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

################################################################################################################################

def Compare(location_1, location_2, location_3):
    """ Returns predictions table and z_score plot """

    binn       =  'Validation'
    regions    =  ['High', 'Low']
    direction  =  ['up','down']

    # zscore[binn][region]
    zscore  =  { b: dict.fromkeys(regions) for b in binns }

    # histos[binn][region] (loading angel yield and stat)
    yield_a = Yield(location_1)
             
    # totalSyst[binn][region][direction] (loading angel syst)
    syst_a = TotalSyst(location_1)

    # histos[binn][region]loading (caleb yield and stat)
    yield_c = CalebYield(location_2) 

    # histos[binn][region][direction] (loading caleb syst)
    syst_c = CalebSyst(location_3) 

    for binn in binns:
        for region in regions:

            nbins  =  temp1[binn][region].GetNbinsX()
            print('nbins = {}\nnbins = {}\n'.format(nbins, yield_c[binn][region].GetNbinsX() ) )

            zscore[binn][region]  =  yield_a[binn][region].Clone()

            for k in range(0, nbins):

            a   =  yield_a[binn][region].GetBinContent(k) 
            c   =  yield_c[binn][regin].GetBinContent(k)

            ae  =  yield_a[binn][region].GetBinError(k)
            ce  =  yield_c[binn][region].GetBinError(k)

            d  =  a - c

            if ( d > 0 ):

                asy  =  syst_a[binn][region]['down'].GetBinContent(k) -1 
                csy  =  syst_c[binn][region]['up'].GetBinContent(k) -1

            elif ( d < 0 ):

                asy  =  syst_a[binn][region]['up'].GetBinContent(k) -1 
                csy  =  syst_c[binn][region]['down'].GetBinContent(k) -1

            elif ( d == 0 ):

                print('\nd == 0 has occured\n')
            
            d /=  m.sqrt( ae**2 + ce**2 + asy**2  + csy**2 )

            #print('bin = {}\nay = {}    cy = {}\nae = {}    ce = {}\nasy = {}    csy = {}\nd = {}\n').format(k, ay, cy, ae, ce, asy, csy, d)

            histos[binn][region].SetBinContent(k, d)
            histos[binn][region].SetBinContent(k, d)

    # zscore[binn][region]
    return zscore

################################################################################################################################

if __name__ == '__main__':

    binn       =  'Validation'
    methods    =  ['angel', 'caleb']
    regions    =  ['High', 'Low']
    direction  =  ['up','down']

    location_1  =  sys.argv[1]
    location_2  =  sys.argv[2]
    location_3  =  sys.argv[3]
    location_4  =  sys.argv[3]

    # histos[binn][region]
    histos  =  Compare(location_1, location_2, location_3)

    for region in regions:

        # draw histograms
        c = ROOT.TCanvas("c", "c", 800, 800)
        c.Divide(1, 2)
    
        # histograms
        c.cd(1)
        ROOT.gPad.SetLogy(1)

        angel  =  Yield(location_1)
        caleb  =  CalebYield(location_2)
       
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

