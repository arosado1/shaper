# plot prediction vs data (validation bins) from results.root 

import sys 
import os
import ROOT
from ROOT import kBlue, kRed

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

#--------------------------------------------------------------------------------------------------------------
# Open root file
#--------------------------------------------------------------------------------------------------------------

file_1_location = sys.argv[1]
file_2_location = sys.argv[2]
year = sys.argv[3] 

angel_file = ROOT.TFile.Open(file_1_location, 'read')
caleb_file = ROOT.TFile.Open(file_2_location, 'read')

#--------------------------------------------------------------------------------------------------------------
# Load histograms
#--------------------------------------------------------------------------------------------------------------
names = ["angel","caleb"]
plots = ["data", "mc", "pred"]

in_root  =  "nValidationBinHighDM_jetpt20"

histo = {}
for name in names:
    histo[name] = dict.fromkeys(plots)

histo["angel"]["data"] = angel_file.Get(in_root + "/" + "MET_nValidationBin_HighDM_jetpt20_" + year + "nValidationBinHighDM_jetpt20nValidationBinHighDM_jetpt20Data MET Validation Bin High DMdata")
histo["angel"]["mc"]   =  angel_file.Get(in_root + "/" + "ZNuNu_nValidationBin_HighDM_jetpt20_" + year + "nValidationBinHighDM_jetpt20nValidationBinHighDM_jetpt20ZJetsToNuNu Validation Bin High DMdata")
histo["angel"]["pred"] =  angel_file.Get(in_root + "/" + "ZNuNu_nValidationBin_HighDM_njetWeight_jetpt20_" + year + "nValidationBinHighDM_jetpt20nValidationBinHighDM_jetpt20ZJetsToNuNu Validation Bin High DMdata")

histo["caleb"]["data"] = caleb_file.Get("data_highdm")
histo["caleb"]["mc"] = caleb_file.Get("mc_highdm")
histo["caleb"]["pred"] = caleb_file.Get("pred_highdm")

#--------------------------------------------------------------------------------------------------------------
# Canvas 
#--------------------------------------------------------------------------------------------------------------

for plot in plots:

    # draw histograms
    c = ROOT.TCanvas("c", "c", 800, 800)
    c.Divide(1, 2)
    
    # legend: TLegend(x1,y1,x2,y2)
    legend_x1 = 0.7
    legend_x2 = 0.9 
    legend_y1 = 0.7 
    legend_y2 = 0.9 
    
    h_ratio = histo["angel"][plot].Clone("h_ratio")
    h_ratio.Divide(histo["caleb"][plot])
    
    #setupHist(hist, title, x_title, y_title, color, y_min, y_max)
    # setupHist(h_ratio, "Z to Invisible Prediction / MC", "x_tiTle", "Pred / MC", "aqua", 0.5, 1.5)
    h_ratio.SetLineColor(ROOT.kBlue)
    
    # histograms
    c.cd(1)
    ROOT.gPad.SetLogy(1) # set log y

    # ZInv MC and Prediction
    histo["angel"][plot].Draw("hist error")
    histo["angel"][plot].SetLineColor(ROOT.kBlue)

    histo["caleb"][plot].Draw("error same hist")
    histo["caleb"][plot].SetLineColor(ROOT.kRed)
    
    # legend: TLegend(x1,y1,x2,y2)
    legend = ROOT.TLegend(legend_x1, legend_y1, legend_x2, legend_y2)
    legend.AddEntry(histo["angel"][plot], "Z#rightarrow#nu#nu angel " + plot, "l")
    legend.AddEntry(histo["caleb"][plot], "Z#rightarrow#nu#nu caleb " + plot, "l")
    legend.Draw()
    
    # ratios
    c.cd(2)
    h_ratio.Draw("hist error")
        
    # save histograms
    c.Update()
    file_name = "validation_HighDM_" + year + "_" + plot + "_comparison" 
    c.SaveAs(file_name + ".png")
    
angel_file.Close()
caleb_file.Close()
