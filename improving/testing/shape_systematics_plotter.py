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

file_location = sys.argv[1]
year          = sys.argv[2] 

angel_file = ROOT.TFile.Open(file_1_location, 'read')

#--------------------------------------------------------------------------------------------------------------
# Setting histo maps 
#--------------------------------------------------------------------------------------------------------------
val        =  'nValidationBin'
variables  =  ['', 'nj', 'ht', 'met']
regions    =  ['LowDM', 'LowDMHighMET', 'HighDM']
branches   =  [ val + s for s in [ r + '_jetpt30' for r in regions ] ]

# histo[variable][region]
histo = {v:dict.fromkeys(region) for v in variables}

# ZNuNu_nValidationBin_HighDM_nj_shape_jetpt30nValidationBinHighDM_jetpt30nValidationBinHighDM_jetpt30ZJetsToNuNu Validation Bin High DMdata

#--------------------------------------------------------------------------------------------------------------
# Load angel histograms
#--------------------------------------------------------------------------------------------------------------

for branch, region in zip(branches,regions):
    for variable in variables:
      
        dash = ['ZNuNu', val, region, variable, 'shape_jetpt30', branch, branch]
        histo_name = '_'.join(dash) + "ZJetsToNuNu Validation Bin High DMdata"
        histo[variable][region]  =  file_location.Get(branch + "/" + histo_name)

        if (histo[variable][region]):
            print("Error, histogram doesn't exist: " + branch + '/' + histo_name)

#--------------------------------------------------------------------------------------------------------------
# LowDM lower-upper merge 
#--------------------------------------------------------------------------------------------------------------

for plot in plots:

    histo["angel"]["LowDM"][plot] =  ROOT.TH1F( "nValidationBinLowDM_jetpt30",  "nValidationBinLowDM_jetpt30", 19, 0, 19)

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
# Load caleb's histograms
#--------------------------------------------------------------------------------------------------------------

histo["caleb"]["HighDM"]["data"]  =  caleb_file.Get("data_highdm")
histo["caleb"]["HighDM"]["mc"]    =  caleb_file.Get("mc_highdm")
histo["caleb"]["HighDM"]["pred"]  =  caleb_file.Get("pred_highdm")

histo["caleb"]["LowDM"]["data"]  =  caleb_file.Get("data_lowdm")
histo["caleb"]["LowDM"]["mc"]    =  caleb_file.Get("mc_lowdm")
histo["caleb"]["LowDM"]["pred"]  =  caleb_file.Get("pred_lowdm")

#--------------------------------------------------------------------------------------------------------------
# z-score 
#--------------------------------------------------------------------------------------------------------------

z_score = {region:dict.fromkeys(plots) for region in regions}

for region in regions:
    for plot in plots:

        if region == "LowDM":
            nbins = 19 
            start = 0
            end   = 19
        else:
            nbins = 24
            start = 19
            end   = 43

        z_score[region][plot] = ROOT.TH1F( 'z_score', 'z-score ' + region + '_' + plot, nbins, start, end )

        for k in range(1, nbins + 1):
        
            a  = histo['angel'][region][plot].GetBinContent(k)
            da = histo['angel'][region][plot].GetBinError(k)

            b  = histo['caleb'][region][plot].GetBinContent(k)
            db = histo['caleb'][region][plot].GetBinError(k)

            # print("bin = {}  |  a = {} +- {}  |  b = {} +- {}".format(k, a, da, b, db) ) # debbuging

            z = (a-b)/m.sqrt((da**2) + (db**2))
           
            # print( "z_score value for bin {} is: {}".format(k, z) ) # debbuging

            z_score[region][plot].SetBinContent(k, z)


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
        
        # setupHist(hist, title, x_title, y_title, color, y_min, y_max)
        # setupHist(h_ratio, "Z to Invisible Prediction / MC", "x_tiTle", "Pred / MC", "aqua", 0.5, 1.5)
        
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
        z_score[region][plot].Draw("hist")
            
        # save histograms
        c.Update()
        file_name = "validation_" + region + "_" + year + "_" + plot + "_angel_caleb_comparison" 
        c.SaveAs(file_name + ".png")
    
caleb_file.Close()
angel_file.Close()
