# njets all

import os
import numpy as np
import ROOT
import json

# make sure ROOT.TFile.Open(fileURL) does not seg fault when $ is in sys.argv (e.g. $ passed in as argument)
ROOT.PyConfig.IgnoreCommandLineOptions = True
# make plots faster without displaying them
ROOT.gROOT.SetBatch(ROOT.kTRUE)

# Get root file explicitly

year  = input("Enter year: ")
year = str(year)

root_file = ROOT.TFile.Open("/uscms/home/arosado/nobackup/YOURWORKINGAREA/CMSSW_10_2_9/src/ZInvisible/Tools/condor/eighth_run/" + year + "/result.root", 'read')
in_root = 'nJets_drLeptonCleaned_jetpt20'
f = ROOT.TFile("shapes_njets.root", 'recreate')

# Get histograms

particles  =  ['Electron', 'Muon', 'Combine']
regions    =  ['HighDM', 'LowDM']
metcuts    =  ["", 'Mid', 'Loose']

norms  =  {}
histos =  {}
shapes =  {}

for particle in particles:

    histos[particle] = {}
    shapes[particle] = {}

    for region in regions:

        histos[particle][region] = {}
        shapes[particle][region] = {}

        for metcut in metcuts: 
            shapes[particle][region][metcut] = {
                'Numerator'    :  0,
                'Denominator'  :  0,
                'Shape'        :  0
                }        

            if particle == 'Combine':
                continue
            if metcut == 'MidHT' and region == 'LowDM':
                continue

            prefix = 'DataMC_' + particle + '_' + region + '_' + metcut
            err = "{}".format("" if not metcut else "_")

            histos[particle][region][metcut] = {
		'Data'  :  prefix + err + 'nj_jetpt20_' + year + 'nJets_drLeptonCleaned_jetpt20nJets_drLeptonCleaned_jetpt20' + 'Datadata',
		'DY'    :  prefix + err + 'nj_jetpt20_' + year + 'nJets_drLeptonCleaned_jetpt20nJets_drLeptonCleaned_jetpt20' + 'DYstack',
		'Sint'  :  prefix + err + 'nj_jetpt20_' + year + 'nJets_drLeptonCleaned_jetpt20nJets_drLeptonCleaned_jetpt20' + 'Single tstack',
		'TTbar' :  prefix + err + 'nj_jetpt20_' + year + 'nJets_drLeptonCleaned_jetpt20nJets_drLeptonCleaned_jetpt20' + 't#bar{t}stack',
		'Rare'  :  prefix + err + 'nj_jetpt20_' + year + 'nJets_drLeptonCleaned_jetpt20nJets_drLeptonCleaned_jetpt20' + 'Rarestack'
		}

	    print('We are now in: ' + particle + ' ' + region + ' ' + metcut) #debbuging

# Retriving histograms

	    h_Data   =  root_file.Get(in_root + '/' + histos[particle][region][metcut]['Data'])
	    h_DY     =  root_file.Get(in_root + '/' + histos[particle][region][metcut]['DY'])
	    h_Sint   =  root_file.Get(in_root + '/' + histos[particle][region][metcut]['Sint'])
	    h_TTbar  =  root_file.Get(in_root + '/' + histos[particle][region][metcut]['TTbar'])
	    h_Rare   =  root_file.Get(in_root + '/' + histos[particle][region][metcut]['Rare'])

            # print str(h_Data.GetNbinsX()) + ' bins when retriving histograms' #bins counter

# Verify if histograms exist

	    if not h_Data:
		print(in_root + '/' + histos[particle][region][metcut]['Data'] + " doesn't exist!")
	    if not h_DY:
		print(in_root + '/' + histos[particle][region][metcut]['DY'] + " doesn't exist!")
	    if not h_Sint:
		print(in_root + '/' + histos[particle][region][metcut]['Sint'] + " doesn't exist!")
	    if not h_TTbar:
		print(in_root + '/' + histos[particle][region][metcut]['TTbar'] + " doesn't exist!")
	    if not h_Rare:
		print(in_root + '/' + histos[particle][region][metcut]['Rare'] + " doesn't exist!")

# Rebining

     #       h_Data.Rebin(2)
     #       h_DY.Rebin(2)
     #       h_Sint.Rebin(2)
     #       h_TTbar.Rebin(2)
     #       h_Rare.Rebin(2)

            bin_1  = 0 
            bin_2 = h_Data.GetNbinsX()

            # print str(h_Data.GetNbinsX()) + ' bins after rebinning ' #bins counter

# Shape factor

            h_Shape = h_Data.Clone()
            h_Shape.SetName("njets_shape_" + year + "_" + particle + '_' + region + err + metcut)
            h_Shape.Add(h_TTbar, -1)
            h_Shape.Add(h_Rare, -1)
            h_Shape.Add(h_Sint, -1)

            shapes[particle][region][metcut]['Numerator']   =  h_Shape.Clone()
            shapes[particle][region][metcut]['Denominator'] =  h_DY.Clone()

            I_Numerator = h_Shape.Integral(bin_1, bin_2)

	    h_Shape.Divide(h_DY)

            shapes[particle][region][metcut]['Shape']  =  h_Shape.Clone()

# Normalization factor

            h_Denominator = h_DY.Clone()
            h_Denominator.Multiply(h_Shape)
            I_Denominator = h_Denominator.Integral(bin_1, bin_2)

            print "In " + particle + " " + region + " " + metcut
            print "I_Numerator = " + str(I_Numerator)
            print "I_Denominator = " + str(I_Denominator)

# Canvas

            h_Shape.GetXaxis().SetRangeUser(2,10)
            h_Shape.GetYaxis().SetRangeUser(0,3)

# Corroboration sheet

            if False:
	        table = {}
	        for binn in range(0,40):
	            table[binn] = {
		        'data'  :  h_Data.GetBinContent(binn),
		        'sine'  :  h_Sint.GetBinContent(binn),
		        'ttbar' :  h_TTbar.GetBinContent(binn),
		        'rare'  :  h_Rare.GetBinContent(binn),
		        'dy'    :  h_DY.GetBinContent(binn),
		        'shape' :  h_Shape.GetBinContent(binn)
	            }

                print str(h_Rare.GetNbinsX()) + ' bins after rebinning'

	        with open('corroboration_sheet_' + particle + '_' + region + '_' + metcut + '.txt', 'w') as sheet:
		    sheet.write("bins: 1 to 40\n\n")
		    for h in ['data', 'sine', 'ttbar', 'rare', 'dy', 'shape']:
		        for n in range(1,40):
		            sheet.write(str(table[n][h]) + '  ')
		        sheet.write('\n\n')

# Create a canvas

	    canvas = ROOT.TCanvas("c", "c", 800, 800)

# Draw legend

	    legend = ROOT.TLegend(0.5, 0.7, 0.9, 0.9)
	    legend.AddEntry(h_Shape, 'Shape', '1')
	    legend.AddEntry(h_Data, 'Data', '1')
	    legend.Draw()

# Draw histogram

	    h_Shape.Draw('error')
	    canvas.Update()

# Save new Histogram as png and root

	    if not metcut:
                file_name = prefix + 'nj_' + year + 'metWithLL_Shape.png'
            else:
                file_name = prefix + '_nj_' + year + 'metWithLL_Shape.png'

	    canvas.SaveAs(file_name)

            h_Shape.Write()

# End of loop--------------------------------------------------------------------------------

# Combine shape factors


for region in regions:
    for metcut in metcuts:
        if metcut == 'MidHT' and region == 'LowDM':
            continue
    
	print 'We are now in: ' + region + ' ' + metcut  #debbuging

        shapes['Combine'][region][metcut]['Numerator']  =  shapes['Electron'][region][metcut]['Numerator'].Clone()
        shapes['Combine'][region][metcut]['Numerator'].Add(shapes['Muon'][region][metcut]['Numerator'])

        shapes['Combine'][region][metcut]['Denominator']  =  shapes['Electron'][region][metcut]['Denominator'].Clone()
        shapes['Combine'][region][metcut]['Denominator'].Add(shapes['Muon'][region][metcut]['Denominator'])

        shapes['Combine'][region][metcut]['Shape']  =  shapes['Combine'][region][metcut]['Numerator'].Clone()
        shapes['Combine'][region][metcut]['Shape']  =  shapes['Combine'][region][metcut]['Shape'].Divide(shapes['Combine'][region][metcut]['Denominator'])

# Save Normalization and shape factors

for region in regions:
    for particle in particles:
        for metcut in metcuts:
            if metcut == 'MidHT' and region == 'LowDM':
                continue
            with open('normalizations.txt', 'a+') as sheet:
                sheet.write(year + " " + region + " " + particle + " " + metcut + " : " + str(norms[particle][region][metcut]['R_Z']) + "\n")

f.Close()
