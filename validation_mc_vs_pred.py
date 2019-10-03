# plot prediction vs data (validation bins) from results.root 

import sys 
import os
import ROOT
# from tools import setupHist, getMultiplicationErrorList, removeCuts, getBinError, ERROR_ZERO, getTexSelection, getTexMultiCut

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

#--------------------------------------------------------------------------------------------------------------
# Open root file
#--------------------------------------------------------------------------------------------------------------

file_location = sys.argv[1]
year = sys.argv[2] 

root_file = ROOT.TFile.Open(file_location, 'read')

#--------------------------------------------------------------------------------------------------------------
# HighDM histo 
#--------------------------------------------------------------------------------------------------------------

regions = ['LowDM', 'HighDM']
plots = ['mc', 'pred']

histo = {}
for region in regions:
    histo[region] = dict.fromkeys(plots)

#--------------------------------------------------------------------------------------------------------------
# Load histograms
#--------------------------------------------------------------------------------------------------------------

lowdm_lower_file  =  "nValidationBinLowDM_jetpt20"
lowdm_upper_file  =  "nValidationBinLowDMHighMET_jetpt20"
highdm_file       =  "nValidationBinHighDM_jetpt20"

histo["HighDM"]["mc"]  =  root_file.Get(highdm_file + "/" + "ZNuNu_nValidationBin_HighDM_jetpt20_" + year + "nValidationBinHighDM_jetpt20nValidationBinHighDM_jetpt20ZJetsToNuNu Validation Bin High DMdata")
histo["HighDM"]["pred"]  =  root_file.Get(highdm_file + "/" + "ZNuNu_nValidationBin_HighDM_njetWeight_jetpt20_" + year + "nValidationBinHighDM_jetpt20nValidationBinHighDM_jetpt20ZJetsToNuNu Validation Bin High DMdata")

h_lowdm_lower = dict.fromkeys(plots)
h_lowdm_upper = dict.fromkeys(plots)

h_lowdm_lower["mc"]    = root_file.Get( lowdm_lower_file + "/" + "ZNuNu_nValidationBin_LowDM_jetpt20_" + year + "nValidationBinLowDM_jetpt20nValidationBinLowDM_jetpt20ZJetsToNuNu Validation Bin Low DMdata")
h_lowdm_lower["pred"]  = root_file.Get( lowdm_lower_file + "/" + "ZNuNu_nValidationBin_LowDM_njetWeight_jetpt20_" + year + "nValidationBinLowDM_jetpt20nValidationBinLowDM_jetpt20ZJetsToNuNu Validation Bin Low DMdata")

h_lowdm_upper["mc"]    = root_file.Get( lowdm_upper_file + "/" + "ZNuNu_nValidationBin_LowDM_HighMET_jetpt20_" + year + "nValidationBinLowDMHighMET_jetpt20nValidationBinLowDMHighMET_jetpt20ZJetsToNuNu Validation Bin Low DM High METdata") 
h_lowdm_upper["pred"]  = root_file.Get( lowdm_upper_file + "/" + "ZNuNu_nValidationBin_LowDM_HighMET_njetWeight_jetpt20_" + year + "nValidationBinLowDMHighMET_jetpt20nValidationBinLowDMHighMET_jetpt20ZJetsToNuNu Validation Bin Low DM High METdata")

#--------------------------------------------------------------------------------------------------------------
# LowDM lower-upper merge 
#--------------------------------------------------------------------------------------------------------------

for plot in plots:

    histo["LowDM"][plot] =  ROOT.TH1F( "LowDM_" + plot , "LowDM_" + plot , 19, 0, 19)

    for k in range(1,20):
    
        if k >= 16: 
            a   =  h_lowdm_upper[plot].GetBinContent(k-15)
            da  =  h_lowdm_upper[plot].GetBinError(k-15) 
        else:
            a   =  h_lowdm_lower[plot].GetBinContent(k)
            da  =  h_lowdm_lower[plot].GetBinError(k) 
    
        histo["LowDM"][plot].SetBinContent( k, a )
        histo["LowDM"][plot].SetBinError( k, da )

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
    
    h_ratio = histo[region]["pred"].Clone("h_ratio")
    h_ratio.Divide(histo[region]["mc"])
    
    # setupHist(h_ratio, "Z to Invisible Prediction / MC", "x_tiTle", "Pred / MC", "aqua", 0.5, 1.5)
    h_ratio.SetLineColor(ROOT.kBlue)
    
    # histograms
    c.cd(1)
    ROOT.gPad.SetLogy(1) # set log y

    # ZInv MC and Prediction
    histo[region]["mc"].Draw("hist error")
    histo[region]["mc"].SetLineColor(ROOT.kRed)
    
    histo[region]["pred"].SetLineColor(ROOT.kBlue)
    histo[region]["pred"].Draw("error same hist")
    
    # legend: TLegend(x1,y1,x2,y2)
    legend = ROOT.TLegend(legend_x1, legend_y1, legend_x2, legend_y2)
    legend.AddEntry( histo[region]["mc"],   "Z#rightarrow#nu#nu MC",   "l")
    legend.AddEntry( histo[region]["pred"], "Z#rightarrow#nu#nu Pred", "l")
    legend.Draw()
    
    # ratios
    c.cd(2)
    h_ratio.Draw("hist error")
        
    # save histograms
    c.Update()
    c.SaveAs("validation_" + region +  "_" + year + "_mc_pred_comparison.png")

root_file.Close()
