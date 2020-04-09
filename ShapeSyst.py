# ShapeSyst.py
# Calculate shape factor systematics uncertainty

import ROOT
import sys 
sys.dont_write_bytecode = True
sys.path.append('./modules')
from LoadHistograms import *

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

################################################################################################################################

def ShapeSyst(location):
    """Calculate shape factor systematic uncertainty"""

    variables   =  ['', 'nj','ht','met', 'ptb', 'nw', 'nrt', 'nmt', 'nb', 'mtb'] #total is appended later
    regions     =  ['High', 'Low']
    binns       =  ['Validation', 'Search']
    directions  =  ['up', 'down']

    # shape[binn][variable][region]
    shapeSyst = { b: { v: dict.fromkeys(regions) for v in (variables + ['total']) } for b in binns }

    # histos[binn][variable][region]
    temp = LoadBinHisto(location)

    # calculating shape systematics
    for binn in binns:
        for region in regions:
 
            nbins = temp[binn][''][region].GetNbinsX()

            for variable in variables:

                # ROOT.gStyle.SetOptStat(0)
                shapeSyst[binn][variable][region] = temp[binn][variable][region].Clone()
                shapeSyst[binn][variable][region].Add(temp[binn]['nj'][region], -1)
                shapeSyst[binn][variable][region].Divide(temp[binn]['nj'][region])
                #print('binn = {}, region = {}, variable = {}'.format(binn, region, variable))

            # total here is the envelople
            shapeSyst[binn]['total'][region]          =  dict.fromkeys(directions) 
            shapeSyst[binn]['total'][region]['up']    =  shapeSyst[binn]['met'][region].Clone()
            shapeSyst[binn]['total'][region]['down']  =  shapeSyst[binn]['met'][region].Clone()
            for variable in variables:
                for k in range(0, nbins + 1):
                    a = shapeSyst[binn][variable][region].GetBinContent(k)
                    u = shapeSyst[binn]['total'][region]['up'].GetBinContent(k)
                    d = shapeSyst[binn]['total'][region]['down'].GetBinContent(k)
                    #print('bin = {}  a = {}  b = {}'.format(k, a, b))

                    if a > u:
                        shapeSyst[binn]['total'][region]['up'].SetBinContent(k, a)
                    elif a < d:
                        shapeSyst[binn]['total'][region]['down'].SetBinContent(k, a)

    # shape[binn][variable][region]
    return shapeSyst

################################################################################################################################

if __name__ == '__main__':

    location       =  sys.argv[1]
    year           =  sys.argv[2] 

    variables   =  ['ht','met', 'ptb', 'nw', 'nrt', 'nmt', 'nb', 'mtb'] 
    regions     =  ['High', 'Low']
    binns       =  ['Validation', 'Search']
    directions  =  ['up', 'down']
    colors      =  [ROOT.kBlue, ROOT.kRed, ROOT.kGreen, ROOT.kOrange, ROOT.kMagenta, ROOT.kAzure, ROOT.kTeal, ROOT.kViolet]

    # shape[binn][variable][region]
    histos = ShapeSyst(location)

    for binn in binns:
        for region in regions:
    
            c = ROOT.TCanvas("c", "c", 800, 800)
            legend = ROOT.TLegend(0.75, 0.75, 0.9, 0.9)
            stack = ROOT.THStack("stack", "stack2")    

            for variable, color in zip(variables, colors):
                histos[binn][variable][region].GetYaxis().SetRangeUser(-1.2, 1.2)
                histos[binn][variable][region].Draw("same histo ")
                histos[binn][variable][region].SetLineWidth(2)
                #histos[binn][variable][region].SetFillColor(color)
                histos[binn][variable][region].SetLineColor(color)
                legend.AddEntry(histos[binn][variable][region], variable, "l")

            flat  =  histos[binn]['total'][region]['up'].Clone()
            flat.Scale(0)
            flat.SetLineWidth(1)
            flat.SetLineColor(ROOT.kBlack)
            flat.Draw("hist same")

            for direction in directions:
                histos[binn]['total'][region][direction].Draw("same histo")
                histos[binn]['total'][region][direction].SetLineWidth(2)
                histos[binn]['total'][region][direction].SetLineColorAlpha(ROOT.kBlack, 1)
                histos[binn]['total'][region][direction].SetLineStyle(2)
                legend.AddEntry(histos[binn]['total'][region][direction], 'total_' + direction, "l")

            legend.Draw()
            c.Update()
            c.SaveAs('outputs/{}_{}_shape_systematics.png'.format(binn, region))

