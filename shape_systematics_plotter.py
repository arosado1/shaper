# plot nValidation bins with different shapes factors applied (aka shape systematics) 

import sys 
import os
import ROOT
import math as m
# from ROOT import kBlue, kRed

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

#--------------------------------------------------------------------------------------------------------------
# Open root file
#--------------------------------------------------------------------------------------------------------------

file_location  =  sys.argv[1]
year           =  sys.argv[2] 

rootfile = ROOT.TFile.Open(file_location, 'read')

#--------------------------------------------------------------------------------------------------------------
# Setting histo maps 
#--------------------------------------------------------------------------------------------------------------
val        =  'nValidationBin'
variables  =  ['', 'nj', 'ht', 'met']
regions    =  ['LowDM', 'LowDMHighMET', 'HighDM']
branches   =  [ val + s for s in [ 'LowDM_jetpt30', 'LowDM_HighMET_jetpt30', 'HighDM_jetpt30']]

# histo[variable][region]
histo = {v:dict.fromkeys(regions) for v in variables}

# ZNuNu_nValidationBin_HighDM_nj_shape_jetpt30nValidationBinHighDM_jetpt30nValidationBinHighDM_jetpt30ZJetsToNuNu Validation Bin High DMdata

#--------------------------------------------------------------------------------------------------------------
# Loading histograms
#--------------------------------------------------------------------------------------------------------------

for branch, region in zip(branches,regions):
    for variable in variables:
      
        err = "{}".format("" if not variable else "_shape_")
        histo[variable]['HighDM'] = rootfile.Get('nValidationBinHighDM_jetpt30/ZNuNu_nValidationBin_HighDM_' + variable + err + 'jetpt30nValidationBinHighDM_jetpt30nValidationBinHighDM_jetpt30ZJetsToNuNu Validation Bin High DMdata')
        histo[variable]['LowDMHighMET'] = rootfile.Get('nValidationBinLowDMHighMET_jetpt30/ZNuNu_nValidationBin_LowDM_HighMET_' + variable + err + 'jetpt30nValidationBinLowDMHighMET_jetpt30nValidationBinLowDMHighMET_jetpt30ZJetsToNuNu Validation Bin Low DM High METdata')
        histo[variable]['LowDM'] = rootfile.Get('nValidationBinLowDM_jetpt30/ZNuNu_nValidationBin_LowDM_' + variable + err + 'jetpt30nValidationBinLowDM_jetpt30nValidationBinLowDM_jetpt30ZJetsToNuNu Validation Bin Low DMdata')

        if not (histo[variable][region]):
            print("Error, histogram doesn't exist: {}, {}").format(region, variable)

#--------------------------------------------------------------------------------------------------------------
# merging LowDM with LowDMHighMET 
#--------------------------------------------------------------------------------------------------------------

for variable in variables:

    temp_histo  =  ROOT.TH1F( "nValidationBinLowDM_jetpt30",  "nValidationBinLowDM_jetpt30", 19, 0, 19)

    for k in range(1,20):

        if k >= 16:
            a   =  histo[variable]['LowDMHighMET'].GetBinContent(k-15)
            da  =  histo[variable]['LowDMHighMET'].GetBinError(k-15)
        else:
            a   =  histo[variable]['LowDM'].GetBinContent(k)
            da  =  histo[variable]['LowDM'].GetBinError(k)

        temp_histo.SetBinContent( k, a )
        temp_histo.SetBinError( k, da )

    histo[variable]['LowDM'] = temp_histo.Clone()

#--------------------------------------------------------------------------------------------------------------
# Systematics 
#--------------------------------------------------------------------------------------------------------------
for region in regions:
    c = ROOT.TCanvas("c", "c", 800, 800)
    syst = dict.fromkeys(variables) 
    syst['met'] = histo['met'][region].Clone()
    syst['met'].Add(histo['nj'][region], -1)
    syst['met'].Divide(histo['nj'][region]) 

    syst['ht'] = histo['ht'][region].Clone()
    syst['ht'].Add(histo['nj'][region], -1)
    syst['ht'].Divide(histo['nj'][region]) 

    syst['ht'].Draw(" hist")
    syst['ht'].SetLineColor(ROOT.kBlue)
    syst['met'].Draw(" same hist")
    syst['met'].SetLineColor(ROOT.kRed)
    legend_x1 = 0.7
    legend_x2 = 0.9 
    legend_y1 = 0.7 
    legend_y2 = 0.9 
    legend = ROOT.TLegend(legend_x1, legend_y1, legend_x2, legend_y2)
    legend.AddEntry(syst['met'], "met ", "l")
    legend.AddEntry(syst['ht'], "ht ", "l")
    legend.Draw()
    c.Update()
    file_name = "systematic_" + region
    c.SaveAs(file_name + ".png")

#--------------------------------------------------------------------------------------------------------------
# Canvas 
#--------------------------------------------------------------------------------------------------------------

for region in regions:

        # draw histograms
        c = ROOT.TCanvas("c", "c", 800, 800)
        
        # legend: TLegend(x1,y1,x2,y2)
        legend_x1 = 0.7
        legend_x2 = 0.9 
        legend_y1 = 0.7 
        legend_y2 = 0.9 
        
        # setupHist(hist, title, x_title, y_title, color, y_min, y_max)
        # setupHist(h_ratio, "Z to Invisible Prediction / MC", "x_tiTle", "Pred / MC", "aqua", 0.5, 1.5)
        
        # histograms
        # set log y-axis
        ROOT.gPad.SetLogy(1)
    
        # ZInv MC and Prediction
        histo[''][region].Draw("hist error")
        histo[''][region].SetLineColor(ROOT.kBlack)

        histo['nj'][region].Draw("hist error same")
        histo['nj'][region].SetLineColor(ROOT.kBlue)
    
        histo["ht"][region].Draw("error same hist")
        histo["ht"][region].SetLineColor(ROOT.kRed)
        
        histo["met"][region].Draw("error same hist")
        histo["met"][region].SetLineColor(ROOT.kGreen)

        # legend: TLegend(x1,y1,x2,y2)
        legend = ROOT.TLegend(legend_x1, legend_y1, legend_x2, legend_y2)
        legend.AddEntry(histo[''][region], "data ", "l")
        legend.AddEntry(histo['nj'][region], "nj ", "l")
        legend.AddEntry(histo['ht'][region], "ht ", "l")
        legend.AddEntry(histo['met'][region], "met ", "l")
        legend.Draw()
        
        # save histograms
        c.Update()
        file_name = "validations_" + region
        c.SaveAs(file_name + ".png")
    
rootfile.Close()
