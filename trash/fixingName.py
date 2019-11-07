# Fixing name of Electron LowDM histograms

import sys
import os
import ROOT
import numpy as np

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

#--------------------------------------------------------------------------------------------------------------
# Open root file
#--------------------------------------------------------------------------------------------------------------

year = sys.argv[1] 

f = ROOT.TFile.Open(year + '/result.root', 'update')
f.cd('nJets_drLeptonCleaned_jetpt20')

mcdata = ['Datadata', 'DYstack', 'Single tstack', 't#bar{t}stack', 'Rarestack'] 

prefix_wrong = 'DataMC_Electron_LowDM_njetWeight_Loose_nj_jetpt20_' + year + 'nJets_drLeptonCleaned_jetpt20nJets_drLeptonCleaned_jetpt20' 
prefix_right = 'DataMC_Electron_LowDM_Loose_njetWeight_nj_jetpt20_' + year + 'nJets_drLeptonCleaned_jetpt20nJets_drLeptonCleaned_jetpt20' 

#--------------------------------------------------------------------------------------------------------------
# Fix Names of Electron LowDM histograms
#--------------------------------------------------------------------------------------------------------------
# nJets_drLeptonCleaned_jetpt20/DataMC_Electron_LowDM_njetWeight_Loose_nj_jetpt20_2016nJets_drLeptonCleaned_jetpt20nJets_drLeptonCleaned_jetpt20Datadata

for mcd in mcdata:
    histo = f.Get('nJets_drLeptonCleaned_jetpt20/' + prefix_wrong + mcd) 
    if not histo:
        print(prefix_wrong + mcd + ' does not exist\n\n')

    histo.SetName(prefix_right + mcd)
    histo.Write() 

f.Close
