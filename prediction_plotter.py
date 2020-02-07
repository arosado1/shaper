# plot prediction vs data (validation bins) from results.root 

import ROOT
import sys 
sys.path.append('./modules')
from LoadHistograms import *
# from tools import setupHist, getMultiplicationErrorList, removeCuts, getBinError, ERROR_ZERO, getTexSelection, getTexMultiCut

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

#--------------------------------------------------------------------------------------------------------------
# Load Histograms
#--------------------------------------------------------------------------------------------------------------

location  =  sys.argv[1]
year      =  sys.argv[2] 

regions    =  ['Low', 'High']
variables  =  ['','nj','ht','met']
plots      =  ['mc', 'pred']

# histo['Validation'][variable][region]
histo = LoadBinHisto(location)

#--------------------------------------------------------------------------------------------------------------
# Canvas 
#--------------------------------------------------------------------------------------------------------------

for region in regions:
    
    # draw histograms
    c = ROOT.TCanvas("c", "c", 800, 800)
    c.Divide(1, 2)

    # legend: TLegend(x1,y1,x2,y2)
    legend_x1 = 0.7
    legend_x2 = 0.9 
    legend_y1 = 0.7 
    legend_y2 = 0.9 
    
    h_ratio = histo['Validation']['nj'][region].Clone("h_ratio")
    h_ratio.Divide(histo['Validation'][''][region])
    
    # setupHist(h_ratio, "Z to Invisible Prediction / MC", "x_tiTle", "Pred / MC", "aqua", 0.5, 1.5)
    h_ratio.SetLineColor(ROOT.kBlue)
    
    # histograms
    c.cd(1)
    ROOT.gPad.SetLogy(1) # set log y

    # ZInv MC and Prediction
    histo['Validation'][""][region].SetLineColor(ROOT.kRed)
    histo['Validation'][""][region].Draw("hist error")
    
    histo['Validation']["nj"][region].SetLineColor(ROOT.kBlue)
    histo['Validation']["nj"][region].Draw("error same hist")
    
    # legend: TLegend(x1,y1,x2,y2)
    legend = ROOT.TLegend(legend_x1, legend_y1, legend_x2, legend_y2)
    legend.AddEntry( histo['Validation'][""][region],   "Z#rightarrow#nu#nu MC",   "l")
    legend.AddEntry( histo['Validation']["nj"][region], "Z#rightarrow#nu#nu Pred", "l")
    legend.Draw()
    
    # ratios
    c.cd(2)
    h_ratio.Draw("hist error")
        
    # save histograms
    c.Update()
    c.SaveAs("validation_" + region +  "_" + year + "_mc_pred_ratio.png")
