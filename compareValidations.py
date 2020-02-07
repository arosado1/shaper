# comparison between angel and caleb data, mc and pred in the validation bins 

import ROOT
import math as m
import sys 
sys.path.append('./modules')
from LoadHistograms import *
# from ROOT import kBlue, kRed

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)


file_1_location = sys.argv[1]
file_2_location = sys.argv[2]
year = sys.argv[3] 

names    =  ['angel', 'caleb']
regions  =  ['Low', 'High']
plots    =  ['mc', 'pred']

# histo[name][region][plot]
histo = { n:{ r: dict.fromkeys(plots) for r in regions } for n in names }

#--------------------------------------------------------------------------------------------------------------
# Loading Angel's Histograms 
#--------------------------------------------------------------------------------------------------------------

# histo['Validation'][variable][region]
temp = LoadBinHisto(file_1_location)

histo['angel']['High']['mc']    = temp['Validation']['']['High'] 
histo['angel']['High']['pred']  = temp['Validation']['nj']['High']

histo['angel']['Low']['mc']     = temp['Validation']['']['Low'] 
histo['angel']['Low']['pred']   = temp['Validation']['nj']['Low']

#--------------------------------------------------------------------------------------------------------------
# Loading's Caleb Histograms 
#--------------------------------------------------------------------------------------------------------------

caleb_file = ROOT.TFile.Open(file_2_location, 'read')

histo['caleb']["High"]["data"]  =  caleb_file.Get("data_highdm")
histo['caleb']["High"]["mc"]    =  caleb_file.Get("mc_highdm")
histo['caleb']["High"]["pred"]  =  caleb_file.Get("pred_highdm")

histo['caleb']["Low"]["data"]   =  caleb_file.Get("data_lowdm")
histo['caleb']["Low"]["mc"]     =  caleb_file.Get("mc_lowdm")
histo['caleb']["Low"]["pred"]   =  caleb_file.Get("pred_lowdm")

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

            if (da == 0 and db == 0):
                da = 1

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
