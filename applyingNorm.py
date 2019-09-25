# Applying normalization factors to Drell Yan 

import sys
import os
import ROOT

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

#--------------------------------------------------------------------------------------------------------------
# Open root file
#--------------------------------------------------------------------------------------------------------------

year = sys.argv[1] 

root_file = ROOT.TFile.Open(year + "/result.root", 'read')
in_root = 'nJets_drLeptonCleaned_jetpt20'

particles  =  ["Electron", 'Muon']
regions    =  ['HighDM', 'LowDM']
metcuts    =  ['', 'Mid', 'Loose']
mcdata     =  ['Data', 'DY', 'Sint', 'TTbar', 'Rare']

f = ROOT.TFile("result.root", 'recreate')
f.mkdir('nJets_drLeptonCleaned_jetpt20')
f.cd('nJets_drLeptonCleaned_jetpt20')

#--------------------------------------------------------------------------------------------------------------
# Normalization Library
#--------------------------------------------------------------------------------------------------------------

norms = {}
for particle in particles:
    norms[particle] = {}
    for region in regions:
        norms[particle][region] = {}
        for y in ('2016','2017','2018_PreHEM','2018_PostHEM'):
            norms[particle][region][y] = 0

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

histos =  {}

for particle in particles:
    histos[particle] = {}
    for region in regions:
        histos[particle][region] = {}
        for metcut in metcuts: 
            histos[particle][region][metcut] = {}

            #-----------------------------
            # loading histograms
            #-----------------------------

            err = "{}".format("" if not metcut else "_")
            prefix = 'DataMC_' + particle + '_' + region + '_' + metcut + err + 'njetWeight_' + 'nj_jetpt20_' + year + 'nJets_drLeptonCleaned_jetpt20nJets_drLeptonCleaned_jetpt20' 

            for sufix, mcd in zip(('Datadata', 'DYstack', 'Single tstack', 't#bar{t}stack', 'Rarestack'), mcdata):
                histos[particle][region][metcut][mcd]  =  root_file.Get(in_root + '/' + prefix + sufix)
	        if not histos[particle][region][metcut][mcd]:
	            print(in_root + '/' + prefix + sufix + " doesn't exist!\n")

            #------------------------------------
            # applying normalization and saving
            #-----------------------------------

            histos[particle][region][metcut]['DY'].Scale(norms[particle][region][year]) 

            for mcd in mcdata:
                histos[particle][region][metcut][mcd].Write()

f.Close
