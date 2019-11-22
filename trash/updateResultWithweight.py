# Applying normalization factors to shape factors

import sys
import os
import ROOT

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

#--------------------------------------------------------------------------------------------------------------
# Open root file
#--------------------------------------------------------------------------------------------------------------

file_location = sys.argv[1]
year = sys.argv[2] 

root_file = ROOT.TFile.Open( file_location, 'update')

particles  =  ["Electron", 'Muon']
regions    =  ['HighDM', 'LowDM']
years      =  ['2016', '2017', '2018_PreHEM', '2018_PostHEM']

#--------------------------------------------------------------------------------------------------------------
# Normalization factors map 
#--------------------------------------------------------------------------------------------------------------

norms = { particle: { region: dict.fromkeys(years) for region in regions } for particle in particles }

norms['Electron']['HighDM']['2016']          =  0.870256299765
norms['Electron']['LowDM']['2016']           =  0.940250693948
norms['Muon']['HighDM']['2016']              =  0.946845651999
norms['Muon']['LowDM']['2016']               =  0.928594335214
norms['Electron']['HighDM']['2017']          =  0.874880049725 
norms['Electron']['LowDM']['2017']           =  0.936733081525 
norms['Muon']['HighDM']['2017']              =  0.785858055299 
norms['Muon']['LowDM']['2017']               =  0.926679239207 
norms['Electron']['HighDM']['2018_PreHEM']   =  0.662135983423 
norms['Electron']['LowDM']['2018_PreHEM']    =  0.893424573777 
norms['Muon']['HighDM']['2018_PreHEM']       =  0.667294456568 
norms['Muon']['LowDM']['2018_PreHEM']        =  0.899232455653 
norms['Electron']['HighDM']['2018_PostHEM']  =  0.743013564313 
norms['Electron']['LowDM']['2018_PostHEM']   =  0.912979743347 
norms['Muon']['HighDM']['2018_PostHEM']      =  0.746547962512 
norms['Muon']['LowDM']['2018_PostHEM']       =  0.9332408103 

#--------------------------------------------------------------------------------------------------------------
# Load Histograms
#--------------------------------------------------------------------------------------------------------------

pred = { particle:dict.fromkeys(regions) for particle in particles }

for particle in particles:
    for region in regions:

        pred[particle][region]  =  root_file.Get( "njets_shape_" + year + "_" + particle + "_" + region + "_Loose" ) 

        if not pred[particle][region]:
           print("bad naming again")

        # njets_shape_2016_Electron_HighDM_Loose

        pred[particle][region].Scale( norms[particle][region][year] ) 

        pred[particle][region].GetYaxis().SetRangeUser(0,3)

        pred[particle][region].Write("njets_pred_" + year + "_" + particle + "_" + region + "_Loose", ROOT.TObject.kOverwrite)

root_file.Close
