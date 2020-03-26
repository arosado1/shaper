# Run2Merger.py (under construction) 

import ROOT
import math as m
import sys 
sys.dont_write_bytecode = True
#from ShapeSyst import *
from Prediction import *
from TotalSyst import *

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

################################################################################################################################

def AllYearMerger( l_2016, l_2017, l_2018 ):
    """Merged yield and systematics for all three years"""

    binns       =  ['Validation']
    years       =  [2016, 2017, 2018]
    regions     =  ['Low', 'High']
    directions  =  ['up', 'down']
    locations   =  [l_2016, l_2017, l_2018] 
    
    yields     =  dict.fromkeys(years)
    systs      =  dict.fromkeys(years)

    # totalyield[binn][region]
    totalyield  =  { b: dict.fromkeys(regions) for b in binns }

    # totalsyst[binn][direction][region]
    totalsyst  =  { b: { d: dict.fromkeys(regions) for d in directions } for b in binns }
    
    # loading histograms
    for year, location in zip(years, locations):

        print('we are now in year = {}, and location = {}'.format(year, location))

        # yields[year][binn][region]
        yields[year]  =  Yield(location)
    
        # systs[year][binn][direction][region]
        systs[year]   =  TotalSyst(location)
    
    for binn in binns:
        for region in regions:
        
            totalyield[binn][region]  =  yields[2016][binn][region].Clone()
            totalyield[binn][region].Add(yields[2017][binn][region], 1.0)
            totalyield[binn][region].Add(yields[2018][binn][region], 1.0)

            for direction in directions:

                totalsyst[binn][direction][region]  =  systs[2016][binn][direction][region].Clone()
                nbins  =  totalsyst[binn][direction][region].GetNbinsX()

                for k in range(0, nbins):
                    a   =  0
                    a  +=  ( systs[2016][binn][direction][region].GetBinContent(k) )**2
                    a  +=  ( systs[2017][binn][direction][region].GetBinContent(k) )**2
                    a  +=  ( systs[2018][binn][direction][region].GetBinContent(k) )**2
                    a   =  m.sqrt(a) 
                    totalsyst[binn][direction][region].SetBinContent(k, a)
     
    # totalyield[binn][region], totalsyst[binn][direction][region]
    return totalyield, totalsyst


################################################################################################################################

if __name__ == '__main__':

    l_2016  =  sys.argv[1]
    l_2017  =  sys.argv[2]
    l_2018  =  sys.argv[3]
    
    binns       =  ['Validation']
    regions     =  ['Low', 'High']
    directions  =  ['up', 'down']

    totalyield, totalsyst  =  AllYearMerger(l_2016, l_2017, l_2018)
    
    for binn in binns:
        for region in regions:

            # canvas
            canvas = ROOT.TCanvas('c', 'c', 800, 800)
         
            # legend
            #legend = ROOT.TLegend(0.5, 0.7, 0.9, 0.9)
            #legend.AddEntry( pred[binn][region], 'what?', 'l' )
            #legend.Draw()
         
            totalyield[binn][region].Draw('error')
         
            canvas.Update()
         
            # png
            file_name = '{}_{}_total_yield.png'.format(binn, region)
            canvas.SaveAs('outputs/' + file_name)

            canvas = ROOT.TCanvas('c', 'c', 800, 800)

            totalsyst[binn]['up'][region].Draw("hist error")
            totalsyst[binn]['up'][region].SetLineWidth(1)
            totalsyst[binn]['up'][region].SetLineColor(ROOT.kRed)

            totalsyst[binn]['down'][region].Draw("hist error same")
            totalsyst[binn]['down'][region].SetLineWidth(1)
            totalsyst[binn]['down'][region].SetLineColor(ROOT.kBlue) 

            # legend
            legend = ROOT.TLegend(0.5, 0.7, 0.9, 0.9)
            legend.AddEntry( totalsyst[binn]['up'][region],   'up',   'l' )
            legend.AddEntry( totalsyst[binn]['down'][region], 'down', 'l' )
            legend.Draw()
     
            canvas.Update()
     
            # png
            file_name = '{}_{}_total_syst.png'.format(binn, region)
            canvas.SaveAs('outputs/' + file_name)


