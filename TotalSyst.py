# TotalSyst.py (under construction)
# Calculate the total systematics uncertainty

import ROOT
import math as m
import sys 
sys.dont_write_bytecode = True
sys.path.append('./modules')
from LoadHistograms import *

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

################################################################################################################################

def TotalSyst(location):
    """Calculate the total systematics uncertainty"""

    regions      =  ['High', 'Low']
    systematics  =  ['', 'pdf', 'metres', 'jes', 'btag', 'eff_restoptag', 'eff_sb', 'eff_toptag', 'eff_wtag', 'met_trig', 'pileup']
    directions   =  ['down', 'up']
    binns        =  ['Validation']

    # shape[binn][direction][region]
    totalSyst = { b: { d: dict.fromkeys(regions) for d in directions } for b in binns }

    # histos[binn][syst][direction][region]
    histos = MCsyst(location)

    for binn in binns:
        for region in regions:
            for direction in directions:

                nbins = histos[binn][''][direction][region].GetNbinsX() 

                for k in range(0, nbins):
                    
                    s  =  'ShapeSyst'.GetBinContent(k)
                    
                    for syst in systematics:
                   
                        a  =  histos[binn][syst][direction][region].GetBinContent(k)
                        s  =  m.sqrt( ( s**2 ) + ( a**2 ) )

                    totalSyst[binn][direction][region].SetBinContent(k, s)



################################################################################################################################

    for binn in binns:
        for region in regions:
 
            #for total syst
            nbins = temp[binn][''][region].GetNbinsX()
            shapeSyst[binn]['total'][region] = temp['Validation'][''][region].Clone()
            for k in range(0, nbins):
                shapeSyst[binn]['total'][region].SetBinContent(k, 0)

            for variable in variables:
                if (variable == 'total'):
                    continue

                shapeSyst[binn][variable][region] = temp[binn][variable][region].Clone()
                shapeSyst[binn][variable][region].Add(temp[binn]['nj'][region], -1)
                shapeSyst[binn][variable][region].Divide(temp[binn]['nj'][region])

                # total here is the envelople
                for k in range(0, nbins):
                    a = abs( shapeSyst[binn][variable][region].GetBinContent(k) )
                    b = abs( shapeSyst[binn]['total'][region].GetBinContent(k) )
                    if a > b:
                        shapeSyst[binn]['total'][region].SetBinContent(k, a)

    # shape[binn][variable][region]
    return shapeSyst

################################################################################################################################

if __name__ == '__main__':

    location       =  sys.argv[1]
    year           =  sys.argv[2] 

    variables  =  ['ht', 'met'] 
    regions    =  ['High', 'Low']
    colors     =  [ROOT.kBlue, ROOT.kRed, ROOT.kBlack]

    histos = ShapeSyst(location)

    #--------------
    # Making Plot 
    #--------------
    
    for region in regions:

        c = ROOT.TCanvas("c", "c", 800, 800)
        legend = ROOT.TLegend(0.75, 0.75, 0.9, 0.9)

        for variable, color in zip(variables, colors):
            histos['Validation'][variable][region].GetYaxis().SetRangeUser(-0.6,0.6)
            histos['Validation'][variable][region].Draw("hist same")
            histos['Validation'][variable][region].SetLineColor(color)
            legend.AddEntry(histos['Validation'][variable][region], variable, "l")

        legend.Draw()
        c.Update()
        c.SaveAs('outputs/validation_' + region + '_shape_systematics.png')

