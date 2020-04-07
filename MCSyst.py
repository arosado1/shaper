# MCSyst.py (under construction)
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
    systematics  =  ['pdf', 'metres', 'jes', 'btag', 'eff_restoptag', 'eff_sb', 'eff_toptag', 'eff_wtag', 'met_trig', 'pileup']
    directions   =  ['down', 'up']
    binns        =  ['Validation', 'Search']

    # shape[binn][direction][region]
    totalSyst = { b: { d: dict.fromkeys(regions) for d in directions } for b in binns }

    # histos[binn][syst][direction][region]
    histos = MCSyst(location)

    for binn in binns:
        for region in regions:
            for direction in directions:

                print("We are now in: {} {} {}".format(binn, region, direction))

                nbins = histos[binn][''][direction][region].GetNbinsX() 
                totalSyst[binn][direction][region]  =  histos[binn][''][direction][region].Clone()

                for k in range(0, nbins + 1):
                    
                    s  =  0 # we can include shape systematic here
                    n  =  histos[binn][ '' ][direction][region].GetBinContent(k)
                    if n != 0:
                        for syst in systematics:
                            a  =  histos[binn][syst][direction][region].GetBinContent(k)

                            a = ( abs(a) - abs(n) )/n
                            s  +=  a**2 

                            #print('n = {:10.4f},  a = {:10.4f},  s = {:10.4f}'.format(n, a, s) )
                    s  =  m.sqrt(s)
                    if direction == 'up':
                        s  =  1 + s
                    else:
                        s  =  1 - s

                    #print('\n--new line--')
                    totalSyst[binn][direction][region].SetBinContent(k, s)
                    
    # totalSyst[binn][direction][region]
    return totalSyst

################################################################################################################################

if __name__ == '__main__':

    location       =  sys.argv[1]
    year           =  sys.argv[2] 

    regions      =  ['High', 'Low']
    directions   =  ['down', 'up']
    binns        =  ['Validation', 'Search']

    # histos[binn][direction][region]
    histos = TotalSyst(location)

    #--------------
    # Making Plot 
    #--------------
    for binn in binns: 
        for region in regions:

            c = ROOT.TCanvas("c", "c", 800, 800)
            legend = ROOT.TLegend(0.75, 0.75, 0.9, 0.9)

            histos[binn]['up'][region].GetYaxis().SetRangeUser(0.3, 1.7)

            histos[binn]['up'][region].Draw(" hist ")
            histos[binn]['down'][region].Draw(" hist same ")

            histos[binn]['up'][region].SetLineColor(ROOT.kRed)
            histos[binn]['down'][region].SetLineColor(ROOT.kBlue)
            histos[binn]['up'][region].SetLineWidth(2)
            histos[binn]['down'][region].SetLineWidth(2)

            legend.AddEntry(histos[binn]['up'][region], 'up', "l")
            legend.AddEntry(histos[binn]['down'][region], 'down', "l")

            legend.Draw()
            c.Update()
            c.SaveAs( 'outputs/{}_{}_{}_Total_syst.png'.format(binn, region, year ) )

