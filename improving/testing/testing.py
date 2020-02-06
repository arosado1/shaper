# plot nValidation bins with different shapes factors applied (aka shape systematics) 

import sys 
import os
import ROOT
from LoadHistograms import *

# from ROOT import kBlue, kRed

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

#--------------------------------------------------------------------------------------------------------------
# Open root file
#--------------------------------------------------------------------------------------------------------------

location       =  sys.argv[1]
year           =  sys.argv[2] 

regions    =  ['High', 'Low']
variables  =  ['','nj','ht','met']

histo = LoadBinHisto(location)

if not histo["Validation"]["ht"]["Low"]:
    print('\n\nits empty!!!!\n\n')

#--------------------------------------------------------------------------------------------------------------
# merging LowDM with LowDMHighMET 
#--------------------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------------------
# Systematics 
#--------------------------------------------------------------------------------------------------------------

for region in regions:
    c = ROOT.TCanvas("c", "c", 800, 800)
    syst = dict.fromkeys(variables) 
    syst['met'] = histo['Validation']['met'][region].Clone()
    syst['met'].Add(histo['Validation']['nj'][region], -1)
    syst['met'].Divide(histo['Validation']['nj'][region]) 

    syst['ht'] = histo['Validation']['ht'][region].Clone()
    syst['ht'].Add(histo['Validation']['nj'][region], -1)
    syst['ht'].Divide(histo['Validation']['nj'][region]) 

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
        histo['Validation'][''][region].Draw("hist error")
        histo['Validation'][''][region].SetLineColor(ROOT.kBlack)

        histo['Validation']['nj'][region].Draw("hist error same")
        histo['Validation']['nj'][region].SetLineColor(ROOT.kBlue)
    
        histo['Validation']["ht"][region].Draw("error same hist")
        histo['Validation']["ht"][region].SetLineColor(ROOT.kRed)
        
        histo['Validation']["met"][region].Draw("error same hist")
        histo['Validation']["met"][region].SetLineColor(ROOT.kGreen)

        # legend: TLegend(x1,y1,x2,y2)
        legend = ROOT.TLegend(legend_x1, legend_y1, legend_x2, legend_y2)
        legend.AddEntry(histo['Validation'][''][region], "data ", "l")
        legend.AddEntry(histo['Validation']['nj'][region], "nj ", "l")
        legend.AddEntry(histo['Validation']['ht'][region], "ht ", "l")
        legend.AddEntry(histo['Validation']['met'][region], "met ", "l")
        legend.Draw()
        
        # save histograms
        c.Update()
        file_name = "validations_" + region
        c.SaveAs(file_name + ".png")
