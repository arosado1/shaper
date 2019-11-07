# calculating normalization 

import os
import sys
import ROOT

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

#--------------------------------------------------------------------------------------------------------------
# Open root file
#--------------------------------------------------------------------------------------------------------------

year = sys.argv[1] 

root_file = ROOT.TFile.Open("/uscms/home/arosado/nobackup/YOURWORKINGAREA/CMSSW_10_2_9/src/ZInvisible/Tools/condor/eighth_run/" + year + "/result.root", 'read')
in_root = 'nJets_drLeptonCleaned_jetpt20'

particles  =  ['Electron', 'Muon']
regions    =  ['HighDM', 'LowDM']
metcuts    =  ['']

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

            # Histograms names

            err = "{}".format("" if not metcut else "_")
            Data  = 'DataMC_' + particle + '_' + region + '_' + metcut + err + 'njetWeight_' + 'nj_jetpt20_' + year + 'nJets_drLeptonCleaned_jetpt20nJets_drLeptonCleaned_jetpt20' + 'Datadata'
            DY    = 'DataMC_' + particle + '_' + region + '_' + metcut + err + 'njetWeight_' + 'nj_jetpt20_' + year + 'nJets_drLeptonCleaned_jetpt20nJets_drLeptonCleaned_jetpt20' + 'DYstack'
            Sint  = 'DataMC_' + particle + '_' + region + '_' + metcut + err + 'njetWeight_' + 'nj_jetpt20_' + year + 'nJets_drLeptonCleaned_jetpt20nJets_drLeptonCleaned_jetpt20' + 'Single tstack'
            TTbar = 'DataMC_' + particle + '_' + region + '_' + metcut + err + 'njetWeight_' + 'nj_jetpt20_' + year + 'nJets_drLeptonCleaned_jetpt20nJets_drLeptonCleaned_jetpt20' + 't#bar{t}stack'
            Rare  = 'DataMC_' + particle + '_' + region + '_' + metcut + err + 'njetWeight_' + 'nj_jetpt20_' + year + 'nJets_drLeptonCleaned_jetpt20nJets_drLeptonCleaned_jetpt20' + 'Rarestack'

            # Retriving histograms

            histos[particle][region][metcut]['Data']  = root_file.Get(in_root + '/' + Data)
            histos[particle][region][metcut]['DY']    = root_file.Get(in_root + '/' + DY)
            histos[particle][region][metcut]['Sint']  = root_file.Get(in_root + '/' + Sint)
            histos[particle][region][metcut]['TTbar'] = root_file.Get(in_root + '/' + TTbar)
            histos[particle][region][metcut]['Rare']  = root_file.Get(in_root + '/' + Rare)

            # Verify if histograms exist

	    if not histos[particle][region][metcut]['Data']:
		print(in_root + '/' + Data + " doesn't exist!")
	    if not histos[particle][region][metcut]['DY']:
		print(in_root + '/' + DY + " doesn't exist!")
	    if not histos[particle][region][metcut]['Sint']:
		print(in_root + '/' + Sint + " doesn't exist!")
	    if not histos[particle][region][metcut]['TTbar']:
		print(in_root + '/' + TTbar + " doesn't exist!")
	    if not histos[particle][region][metcut]['Rare']:
		print(in_root + '/' + Rare + " doesn't exist!")

#--------------------------------------------------------------------------------------------------------------
# Calculating Normalization
#--------------------------------------------------------------------------------------------------------------
metcut = ''
norms = {}
bin_1  = 0 
bin_2 = histos['Muon']['HighDM'][metcut]['Data'].GetNbinsX()

for region in regions:
    norms[region] = {}
    Num = 0
    Dem = 0
    for particle in particles:

        h_Numerator = histos[particle][region][metcut]['Data'].Clone() 
        h_Numerator.Add( histos[particle][region][metcut]['Sint'] , -1)  
        h_Numerator.Add( histos[particle][region][metcut]['TTbar'], -1) 
        h_Numerator.Add( histos[particle][region][metcut]['Rare'] , -1)  
        h_Denominator = histos[particle][region][metcut]['DY'].Clone()
        I_Numerator = h_Numerator.Integral(bin_1, bin_2) 
        I_Denominator = h_Denominator.Integral(bin_1, bin_2)
    
        Num += I_Numerator
        Dem += I_Denominator

        norms[region][particle] =  I_Numerator/I_Denominator
        
    norms[region]["Combine"] = Num/Dem

#--------------------------------------------------------------------------------------------------------------
# print normalization factors
#--------------------------------------------------------------------------------------------------------------
#   particles.append("Combine")
#   
#   for particle in particles:
#       for region in regions:
#           print("\n" + particle + " " + region + ": " + str(norms[region][particle]))
#           with open('normalizations.txt', 'a+') as sheet:
#               sheet.write("\hline" + region + " & " + particle + " & " + year + " & " + str(norms[region][particle]) + " \n") 

