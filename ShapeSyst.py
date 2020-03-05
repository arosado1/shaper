# Calculate shape factor systematics (under construction)(this will replace shape_systematic_plotter.py) 

import ROOT
import sys 
sys.path.append('./modules')
from LoadHistograms import *

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

################################################################################################################################

def ShapeSyst(location):
    """Calculate shape factor systematic uncertainty"""

    variables  =  ['ht', 'met', 'total'] #total is appended later
    regions    =  ['High', 'Low']
    binns      =  ['Validation']

    # shape[binn][variable][region]
    shapeSyst = { b: { v: dict.fromkeys(regions) for v in variables } for b in binns }

    # histos[binn][variable][region]
    temp = LoadBinHisto(location)

    # calculating systematics
    for binn in binns:
        for region in regions:
            for variable in variables:
                if (variable == 'total'):
                    continue

                shapeSyst[binn][variable][region] = temp[binn][variable][region].Clone()
                shapeSyst[binn][variable][region].Add(temp[binn]['nj'][region], -1)
                shapeSyst[binn][variable][region].Divide(temp[binn]['nj'][region])

            # some calculation for the total systematic here (for now is nominal)
            shapeSyst[binn]['total'][region] = temp['Validation'][''][region].Clone()

    # shape[binn][variable][region]
    return shapeSyst

################################################################################################################################

if __name__ == '__main__':

    location       =  sys.argv[1]
    year           =  sys.argv[2] 

    variables  =  ['ht', 'met'] 
    regions    =  ['High', 'Low']
    colors     =  [ROOT.kBlue, ROOT.kRed]

    histos = ShapeSyst(location)

    #--------------
    # Making Plot 
    #--------------
    
    for region in regions:

        c = ROOT.TCanvas("c", "c", 800, 800)
        legend = ROOT.TLegend(0.8, 0.8, 0.9, 0.9)

        for variable, color in zip(variables, colors):
            histos['Validation'][variable][region].GetYaxis().SetRangeUser(-0.6,0.6)
            histos['Validation'][variable][region].Draw("hist same")
            histos['Validation'][variable][region].SetLineColor(color)
            legend.AddEntry(histos['Validation'][variable][region], variable, "l")

        legend.Draw()
        c.Update()
        c.SaveAs('validation_' + region + '_shape_systematics.png')

