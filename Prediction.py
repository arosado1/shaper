# Prediction.py 
# Make Z to invisible prediction table and histograms 


import ROOT
import math as m
import sys 
sys.dont_write_bytecode = True
sys.path.append('./modules')
from LoadHistograms import *
from ShapeSyst import *

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

























#--------------------------------------------------------------------------------------------------------------
# Canvas 
#--------------------------------------------------------------------------------------------------------------
#
#for region in regions:
#    
#    # draw histograms
#    c = ROOT.TCanvas("c", "c", 800, 800)
#    c.Divide(1, 2)
#
#    # legend: TLegend(x1,y1,x2,y2)
#    legend_x1 = 0.7
#    legend_x2 = 0.9 
#    legend_y1 = 0.7 
#    legend_y2 = 0.9 
#    
#    h_ratio = histo['Validation']['nj'][region].Clone("h_ratio")
#    h_ratio.Divide(histo['Validation'][''][region])
#    
#    # setupHist(h_ratio, "Z to Invisible Prediction / MC", "x_tiTle", "Pred / MC", "aqua", 0.5, 1.5)
#    h_ratio.SetLineColor(ROOT.kBlue)
#    
#    # histograms
#    c.cd(1)
#    ROOT.gPad.SetLogy(1) # set log y
#
#    # ZInv MC and Prediction
#    histo['Validation'][""][region].SetLineColor(ROOT.kRed)
#    histo['Validation'][""][region].Draw("hist error")
#    
#    histo['Validation']["nj"][region].SetLineColor(ROOT.kBlue)
#    histo['Validation']["nj"][region].Draw("error same hist")
#    
#    # legend: TLegend(x1,y1,x2,y2)
#    legend = ROOT.TLegend(legend_x1, legend_y1, legend_x2, legend_y2)
#    legend.AddEntry( histo['Validation'][""][region],   "Z#rightarrow#nu#nu MC",   "l")
#    legend.AddEntry( histo['Validation']["nj"][region], "Z#rightarrow#nu#nu Pred", "l")
#    legend.Draw()
#    
#    # ratios
#    c.cd(2)
#    h_ratio.Draw("hist error")
#        
#    # save histograms
#    c.Update()
#    c.SaveAs("validation_" + region +  "_" + year + "_mc_pred_ratio.png")
