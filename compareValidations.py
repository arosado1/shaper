# comparison between angel and caleb data, mc and pred in the validation bins 

import sys 
import os
import ROOT
# from ROOT import kBlue, kRed

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
# Setting histo maps 
#--------------------------------------------------------------------------------------------------------------

names =    ['angel', 'caleb']
regions =  ['LowDM', 'HighDM']
plots =    ['data', 'mc', 'pred']

histo = {name:{region:dict.fromkeys(plots) for region in regions} for name in names} # histo[name][region][plot] 
h_lowdm_lower = dict.fromkeys(plots)
h_lowdm_upper = dict.fromkeys(plots)

#--------------------------------------------------------------------------------------------------------------
# Load angel histograms
#--------------------------------------------------------------------------------------------------------------


lowdm_lower_file  =  "nValidationBinLowDM_jetpt20"
lowdm_upper_file  =  "nValidationBinLowDMHighMET_jetpt20"
highdm_file       =  "nValidationBinHighDM_jetpt20"


histo["angel"]['HighDM']["data"]  =  angel_file.Get(highdm_file + "/" + "MET_nValidationBin_HighDM_jetpt20_" + year + "nValidationBinHighDM_jetpt20nValidationBinHighDM_jetpt20Data MET Validation Bin High DMdata")
histo["angel"]["HighDM"]["mc"]    =  angel_file.Get(highdm_file + "/" + "ZNuNu_nValidationBin_HighDM_jetpt20_" + year + "nValidationBinHighDM_jetpt20nValidationBinHighDM_jetpt20ZJetsToNuNu Validation Bin High DMdata")
histo["angel"]["HighDM"]["pred"]  =  angel_file.Get(highdm_file + "/" + "ZNuNu_nValidationBin_HighDM_njetWeight_jetpt20_" + year + "nValidationBinHighDM_jetpt20nValidationBinHighDM_jetpt20ZJetsToNuNu Validation Bin High DMdata")


h_lowdm_lower["data"]  =  angel_file.Get( lowdm_lower_file + "/" + "MET_nValidationBin_LowDM_jetpt20_" + year + "nValidationBinLowDM_jetpt20nValidationBinLowDM_jetpt20Data MET Validation Bin Low DMdata")
h_lowdm_lower["mc"]    =  angel_file.Get( lowdm_lower_file + "/" + "ZNuNu_nValidationBin_LowDM_jetpt20_" + year + "nValidationBinLowDM_jetpt20nValidationBinLowDM_jetpt20ZJetsToNuNu Validation Bin Low DMdata")
h_lowdm_lower["pred"]  =  angel_file.Get( lowdm_lower_file + "/" + "ZNuNu_nValidationBin_LowDM_njetWeight_jetpt20_" + year + "nValidationBinLowDM_jetpt20nValidationBinLowDM_jetpt20ZJetsToNuNu Validation Bin Low DMdata")


h_lowdm_upper["data"]  =  angel_file.Get( lowdm_upper_file + "/" + "MET_nValidationBin_LowDM_HighMET_jetpt20_" + year + "nValidationBinLowDMHighMET_jetpt20nValidationBinLowDMHighMET_jetpt20Data MET Validation Bin Low DM High METdata")
h_lowdm_upper["mc"]    =  angel_file.Get( lowdm_upper_file + "/" + "ZNuNu_nValidationBin_LowDM_HighMET_jetpt20_" + year + "nValidationBinLowDMHighMET_jetpt20nValidationBinLowDMHighMET_jetpt20ZJetsToNuNu Validation Bin Low DM High METdata")
h_lowdm_upper["pred"]  =  angel_file.Get( lowdm_upper_file + "/" + "ZNuNu_nValidationBin_LowDM_HighMET_njetWeight_jetpt20_" + year + "nValidationBinLowDMHighMET_jetpt20nValidationBinLowDMHighMET_jetpt20ZJetsToNuNu Validation Bin Low DM High METdata")


if not histo["angel"]["HighDM"]["data"]:
    print("angel_highDM_data empty")
if not histo["angel"]["HighDM"]["mc"]:
    print("angel_highDM_mc empty")
if not histo["angel"]["HighDM"]["pred"]:
    print("angel_highDM_pred empty")

if not h_lowdm_lower["data"]:
    print("lowdm_lower_data empty")
if not h_lowdm_lower["mc"]:
    print("lowdm_lower_mc empty")
if not h_lowdm_lower["pred"]:
    print("lowdm_lower_pred empty")

if not h_lowdm_upper["data"]:
    print("lowdm_upper_data empty")
if not h_lowdm_upper["mc"]:
    print("lowdm_upper_mc empty")
if not h_lowdm_upper["pred"]:
    print("lowdm_upper_pred empty")

#--------------------------------------------------------------------------------------------------------------
# LowDM lower-upper merge 
#--------------------------------------------------------------------------------------------------------------

for plot in plots:

    histo["angel"]["LowDM"][plot] =  ROOT.TH1F( "nValidationBinLowDM_jetpt20",  "nValidationBinLowDM_jetpt20", 19, 0, 19)

    for k in range(1,20):

        if k >= 16:
            a   =  h_lowdm_upper[plot].GetBinContent(k-15)
            da  =  h_lowdm_upper[plot].GetBinError(k-15)
        else:
            a   =  h_lowdm_lower[plot].GetBinContent(k)
            da  =  h_lowdm_lower[plot].GetBinError(k)

        histo["angel"]["LowDM"][plot].SetBinContent( k, a )
        histo["angel"]["LowDM"][plot].SetBinError( k, da )

#--------------------------------------------------------------------------------------------------------------
# Load caleb histograms
#--------------------------------------------------------------------------------------------------------------

histo["caleb"]["HighDM"]["data"]  =  caleb_file.Get("data_highdm")
histo["caleb"]["HighDM"]["mc"]    =  caleb_file.Get("mc_highdm")
histo["caleb"]["HighDM"]["pred"]  =  caleb_file.Get("pred_highdm")

histo["caleb"]["LowDM"]["data"]  =  caleb_file.Get("data_lowdm")
histo["caleb"]["LowDM"]["mc"]    =  caleb_file.Get("mc_lowdm")
histo["caleb"]["LowDM"]["pred"]  =  caleb_file.Get("pred_lowdm")

#--------------------------------------------------------------------------------------------------------------
# Canvas 
#--------------------------------------------------------------------------------------------------------------
for region in regions:
    for plot in plots:

        # draw histograms
        c = ROOT.TCanvas("c", "c", 800, 800)
        c.Divide(1, 2)
        
        # legend: TLegend(x1,y1,x2,y2)
        legend_x1 = 0.7
        legend_x2 = 0.9 
        legend_y1 = 0.7 
        legend_y2 = 0.9 
        
        h_ratio = histo["angel"][region][plot].Clone("h_ratio")
        h_ratio.Divide(histo["caleb"][region][plot])
        
        #setupHist(hist, title, x_title, y_title, color, y_min, y_max)
        # setupHist(h_ratio, "Z to Invisible Prediction / MC", "x_tiTle", "Pred / MC", "aqua", 0.5, 1.5)
        h_ratio.SetLineColor(ROOT.kBlue)
        
        # histograms
        c.cd(1)
        ROOT.gPad.SetLogy(1) # set log y
    
        # ZInv MC and Prediction
        histo["angel"][region][plot].Draw("hist error")
        histo["angel"][region][plot].SetLineColor(ROOT.kBlue)
    
        histo["caleb"][region][plot].Draw("error same hist")
        histo["caleb"][region][plot].SetLineColor(ROOT.kRed)
        
        # legend: TLegend(x1,y1,x2,y2)
        legend = ROOT.TLegend(legend_x1, legend_y1, legend_x2, legend_y2)
        legend.AddEntry(histo["angel"][region][plot], "Z#rightarrow#nu#nu angel " + plot, "l")
        legend.AddEntry(histo["caleb"][region][plot], "Z#rightarrow#nu#nu caleb " + plot, "l")
        legend.Draw()
        
        # ratios
        c.cd(2)
        h_ratio.Draw("hist error")
            
        # save histograms
        c.Update()
        file_name = "validation_" + region + "_" + year + "_" + plot + "_angel_caleb_comparison" 
        c.SaveAs(file_name + ".png")
    
caleb_file.Close()
angel_file.Close()
