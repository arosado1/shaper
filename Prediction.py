# Prediction.py (take away total uncertainty and put up and down) 
# Make Z to invisible prediction table and histograms 

import ROOT
import math as m
import sys 
sys.dont_write_bytecode = True
sys.path.append('./modules')
from LoadHistograms import *
from ShapeSyst import *
from ShapeNormGen import *

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

################################################################################################################################

def Prediction(location):
    """Make Z to invisible prediction table and histogram"""

    regions  =  ['Low', 'High']
    plots    =  ['mc', 'pred']
    binns    =  ['Validation']

    # histo[binn][variable][region]
    histos     =  LoadBinHisto(location)

    # shape[binn][variable][region]
    shapeSyst  =  ShapeSyst(location)

    # pred[binn][region]
    pred = {b: dict.fromkeys(regions) for b in binns}

    with open('outputs/PredictionTable.txt', 'w') as sheet:
        for binn in binns:
            for region in regions:

                sheet.write( '\n{} {}DM table\n\n'.format(binn, region) )
                sheet.write('{:<10s}{:<9s}{:<12s}{:<11s}{:<11s}\n'.format('bin', 'yield', 'stat_unc', 'syst_unc', 'total_unc') ) 

                nbins = histos[binn]['nj'][region].GetNbinsX()

                pred[binn][region] = histos[binn]['nj'][region].Clone()

                print('bin counting, nbins = {}'.format(nbins)) # for debugging purposes

                for k in range(0, nbins): 

                    val   =  histos[binn]['nj'][region].GetBinContent(k)
                    stat  =  histos[binn]['nj'][region].GetBinError(k)
                    syst  =  shapeSyst[binn]['total'][region].GetBinContent(k) 
                    unc   =  m.sqrt( (stat**2) + (syst**2) )
                    pred[binn][region].SetBinError(k, unc)

                    line = '{:<3d}  {:10.4f}  {:10.4f}  {:10.4f}  {:10.4f}\n'.format(k, val, stat, syst, unc)
                    sheet.write(line) 
                sheet.write('\n'+80*'#'+'\n')

    return pred             

################################################################################################################################

def Yield(location):
    """Z to invisible prediction histogram"""

    binns     =  ['Validation']
    regions   =  ['Low', 'High']

    # histos[binn][variable][region]
    histos   =  LoadBinHisto(location)

    # factors[variable][region][particle][fattore]
    factors  =  ShapeNormFactors(location)

    # yields[binn][region]
    yields = {b: dict.fromkeys(regions) for b in binns}

    for binn in binns:
        for region in regions:

            yields[binn][region]  =  histos[binn]['nj'][region].Clone()
            yields[binn][region].Scale( factors['nj'][region]['Combined']['norm'] )

    # yields[binn][region]
    return yields

################################################################################################################################

if __name__ == '__main__':

    location  =  sys.argv[1]
    #year      =  sys.argv[2] 

    regions  =  ['Low', 'High']
    plots    =  ['mc', 'pred']
    binns    =  ['Validation']

    # pred[binn][region]
    pred = Prediction(location)

    for binn in binns:
        for region in regions:
    
            # canvas
            canvas = ROOT.TCanvas('c', 'c', 800, 800)
         
            # legend
            legend = ROOT.TLegend(0.5, 0.7, 0.9, 0.9)
            legend.AddEntry(pred[binn][region], 'what?', 'l' )
            legend.Draw()
         
            pred[binn][region].Draw('error')
         
            canvas.Update()
            pred[binn][region].Write()
         
            # png
            file_name = '{}_{}.png'.format(binn, region)
            #canvas.SaveAs(file_name)


