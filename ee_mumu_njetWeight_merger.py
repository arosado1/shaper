# ee mumu shapeWeight merger 

import sys
import os
import ROOT
import math as m

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

#--------------------------------------------------------------------------------------------------------------
# Open root file
#--------------------------------------------------------------------------------------------------------------

file_location = sys.argv[1]
year = sys.argv[2] 

root_file = ROOT.TFile.Open(file_location, 'update')

#--------------------------------------------------------------------------------------------------------------
# Definitions
#--------------------------------------------------------------------------------------------------------------

particles     =  ["Electron", 'Muon']
regions       =  ['HighDM', 'LowDM']
metcuts       =  ['', 'Mid', 'Loose']

nbins  =  10
start  =  0
end    =  10

#--------------------------------------------------------------------------------------------------------------
# Upload bin content
#--------------------------------------------------------------------------------------------------------------
for region in regions:
    for metcut in metcuts:

        err = "{}".format("" if not metcut else "_")

        #-----------------------------
        # crate and load histograms
        #-----------------------------

        h_electron  =  root_file.Get("njets_shape_" + year + "_Electron_" + region + err + metcut)
        h_muon      =  root_file.Get("njets_shape_" + year + "_Muon_"     + region + err + metcut)

        name        =  "njets_shape_" + year + "_Combine_"  + region + err + metcut
        h_combine   =  ROOT.TH1F( name, name, nbins, start, end)

        #-----------------------------
        # calculate average 
        #-----------------------------

        for k in range(1, 11):

            e    =  h_electron.GetBinContent(k)
            de   =  h_electron.GetBinError(k)

            if de == 0:
                h_combine.SetBinContent(k, 0)
                h_combine.SetBinError(k, 0)
                continue
            else:
                we = (1/de)**2

            mu   =  h_muon.GetBinContent(k)
            dmu  =  h_muon.GetBinError(k)
            wmu = (1/dmu)**2

            c    =  (e * we + mu * wmu)/(we + wmu) 

            dc   =   1/m.sqrt(we + wmu)

            h_combine.SetBinContent(k, c)
            h_combine.SetBinError(k, dc)

        #-----------------------------
        # Save h_combine 
        #-----------------------------

        canvas = ROOT.TCanvas("c", "c", 800, 800)

        h_combine.Draw('error')

        h_combine.GetYaxis().SetRangeUser(0,3)
        h_combine.GetXaxis().SetRangeUser(2,10)

        canvas.Update()
     
        h_combine.Write()


root_file.Close
