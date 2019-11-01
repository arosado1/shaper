# njets all

import sys
import os
import numpy as np
import ROOT
import json

# make sure ROOT.TFile.Open(fileURL) does not seg fault when $ is in sys.argv (e.g. $ passed in as argument)
ROOT.PyConfig.IgnoreCommandLineOptions = True
# make plots faster without displaying them
ROOT.gROOT.SetBatch(ROOT.kTRUE)

#-----------------------------
# Get root file explicitly
#-----------------------------

location = sys.argv[1]
year  = sys.argv[2]

root_file = ROOT.TFile.Open(location)
in_root = 'nJets_drLeptonCleaned_jetpt30'
f = ROOT.TFile("shapes_njets_" + year + ".root", 'recreate')

#-----------------------------
# Get histograms
#-----------------------------

particles  =  ['Electron', 'Muon']
regions    =  ['HighDM', 'LowDM']
metcuts    =  ['', 'Mid', 'Loose']
mcdata     =  ['Data', 'DY', 'Sint', 'TTbar', 'Rare']

histos =  {p: {r: {m: dict.fromkeys(mcdata) for m in metcuts} for r in regions} for p in particles} # histos[particle][region][metcut][mcdata]
shapes =  {p: {r: dict.fromkeys(metcuts) for r in regions} for p in particles}                      # shapes[particle][region][metcut]

for particle in particles:
    for region in regions:
        for metcut in metcuts: 

	    print('We are now in: ' + particle + ' ' + region + ' ' + metcut) #debbuging

            "{}".format("" if not metcut else "_").
            prefix = 'DataMC_' + particle + '_' + region + '_' + metcut + err

            for mcd, mcds in zip(mcdata, ['Datadata', 'DYstack', 'Single tstack', 't#bar{t}stack', 'Rarestack']):
                histos[particle][region][metcut][mcd] = root_file.Get(in_root + '/' + prefix + 'nj_jetpt30_' + year + 'nJets_drLeptonCleaned_jetpt30nJets_drLeptonCleaned_jetpt30' + mcds)
                
                if not histos[particle][region][metcut][mcd]:
		    print(in_root + '/' + histos[particle][region][metcut][mcd] + " doesn't exist!")
            
            bin_1  = 0 
            bin_2 = histos[particle][region][metcut]['Data'].GetNbinsX()

            #-----------------------------
            # Shape factor
            #-----------------------------

            h_Shape = histos[particle][region][metcut]['Data'].Clone()
            h_Shape.SetName("njets_shape_" + year + "_" + particle + '_' + region + err + metcut)
            h_Shape.Add(histos[particle][region][metcut]['TTbar'], -1)
            h_Shape.Add(histos[particle][region][metcut]['Rare'], -1)
            h_Shape.Add(histos[particle][region][metcut]['Sint'], -1)
            h_Shape.Divide( histos[particle][region][metcut]['DY'] )

            #-----------------------------
            # Corroboration sheet
            #-----------------------------

            if False:
	        with open('corroboration_sheet_' + particle + '_' + region + '_' + metcut + '.txt', 'w') as sheet:
		    sheet.write("bins: 1 to 40\n\n")
		    for mcd in mcdata:
		        for binn in range(1,40):
                            bin_value = str( histos[particle][region][metcut][mcd].GetBinContent(binn) )
		            sheet.write( bin_value + '  ')
		        sheet.write('\n\n')

            #-----------------------------
            # Create a canvas
            #-----------------------------

            h_Shape.GetXaxis().SetRangeUser(2,10)
            h_Shape.GetYaxis().SetRangeUser(0,3)

	    canvas = ROOT.TCanvas("c", "c", 800, 800)

	    legend = ROOT.TLegend(0.5, 0.7, 0.9, 0.9)
	    legend.AddEntry(h_Shape, 'Shape', '1')
	    legend.AddEntry(h_Data, 'Data', '1')
	    legend.Draw()

	    h_Shape.Draw('error')
	    canvas.Update()

            file_name = prefix + 'nj_' + year + 'metWithLL_Shape.png'

	    canvas.SaveAs(file_name)

            h_Shape.Write()

f.Close()
