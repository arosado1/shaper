# Calculate shape factor systematics (under construction)(this will replace shape_systematic_plotter.py) 

import ROOT
import sys 
sys.path.append('./modules')
from LoadHistograms import *

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

location       =  sys.argv[1]
year           =  sys.argv[2] 

def ShapeSyst(location):
    """Calculate shape factor systematic uncertainty"""

    #--------------
    # Definitions 
    #--------------
    
    variables  =  ['nj', 'ht', 'met'] #total is appended later
    regions    =  ['High', 'Low']

    # shape[variable][region]
    shapeSyst = { v: dict.fromkeys(regions) for v in variables }

    temp = LoadBinHisto(location)

    for variable in variables:
        for region in regions:
            shapeSyst[variable][region] = temp['Validation'][variable][region]

    # calculating systematics
    for region in regions:
        for variable in variables:
            if (variable == 'nj'):
                continue
            shapeSyst[variable][region] = temp['Validation'][variable][region].Clone()
            shapeSyst[variable][region].Add(temp['Validation']['nj'][region], -1)
            shapeSyst[variable][region].Divide(temp['Validation']['nj'][region])

        shapeSyst['total'][region] = temp['Validation'][''][region].Clone()
        
        # some calculation for the total systematic here


    # shape[variable][region]
    return shapeSyst

################################################################################################################################

if __name__ == '__main__':

        syst['ht'].GetYaxis().SetRangeUser(-0.6,0.6)
    
        syst['ht'].Draw(" hist")
        syst['ht'].SetLineColor(ROOT.kBlue)
        syst['met'].Draw(" same hist")
        syst['met'].SetLineColor(ROOT.kRed)
    
    
        legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
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
    
            histo['Validation']['nj'][region].Draw("hist same")
            histo['Validation']['nj'][region].SetLineColor(ROOT.kBlue)
        
            histo['Validation']["ht"][region].Draw("same hist")
            histo['Validation']["ht"][region].SetLineColor(ROOT.kRed)
            
            histo['Validation']["met"][region].Draw("same hist")
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
