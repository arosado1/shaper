# MET normalization, shape, and validation

import os
import numpy as np
import ROOT

# make sure ROOT.TFile.Open(fileURL) does not seg fault when $ is in sys.argv (e.g. $ passed in as argument)
ROOT.PyConfig.IgnoreCommandLineOptions = True
# make plots faster without displaying them
ROOT.gROOT.SetBatch(ROOT.kTRUE)

# Get root file explicitly

year  = input("Enter year: ")
year = str(year)

root_file = ROOT.TFile.Open("/uscms/home/arosado/nobackup/YOURWORKINGAREA/CMSSW_10_2_9/src/ZInvisible/Tools/condor/sixth_run/" + year + "/result.root", 'read')
in_root = 'metWithLL'

particles  =  ['Electron', 'Muon', 'Combine']
regions    =  ['HighDM', 'LowDM']
metcuts    =  ["", 'Mid', 'Loose']

#--------------------------------------------------------------------------------------------------------------

# Load Histograms

histos =  {}

for particle in particles:
    histos[particle] = {}
    for region in regions:
        histos[particle][region] = {}
        for metcut in metcuts: 
            histos[particle][region][metcut] = {}

            # Histograms names

            err = "{}".format("" if not metcut else "_")
            Data  = 'DataMC_' + particle + '_' + region + '_' + metcut + err + 'met_' + year + 'metWithLLmetWithLL' + 'Datadata',
            DY    = 'DataMC_' + particle + '_' + region + '_' + metcut + err + 'met_' + year + 'metWithLLmetWithLL' + 'DYstack',
            Sint  = 'DataMC_' + particle + '_' + region + '_' + metcut + err + 'met_' + year + 'metWithLLmetWithLL' + 'Single tstack',
            TTbar = 'DataMC_' + particle + '_' + region + '_' + metcut + err + 'met_' + year + 'metWithLLmetWithLL' + 't#bar{t}stack',
            Rare  = 'DataMC_' + particle + '_' + region + '_' + metcut + err + 'met_' + year + 'metWithLLmetWithLL' + 'Rarestack'

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

# Calculating shape factors

f = ROOT.TFile("shapes_mets.root", 'recreate')

shapes = {}

for particle in particles:
    shapes[particle] = {}
    for region in regions:
        shapes[particle][region] = {}
        for metcut in metcuts: 
            shapes[particle][region][metcut] = {}

                h_Data   =  root_file.Get(in_root + '/' + histos[particle][region][metcut]['Data'])
                h_DY     =  root_file.Get(in_root + '/' + histos[particle][region][metcut]['DY'])
                h_Sint   =  root_file.Get(in_root + '/' + histos[particle][region][metcut]['Sint'])
                h_TTbar  =  root_file.Get(in_root + '/' + histos[particle][region][metcut]['TTbar'])
                h_Rare   =  root_file.Get(in_root + '/' + histos[particle][region][metcut]['Rare'])

                h_Data.Rebin(2)
                h_DY.Rebin(2)
                h_Sint.Rebin(2)
                h_TTbar.Rebin(2)
                h_Rare.Rebin(2)

                h_Shape = h_Data.Clone()
                h_Shape.Add(h_TTbar, -1)
                h_Shape.Add(h_Rare, -1)
                h_Shape.Add(h_Sint, -1)

                shapes[particle][region][metcut]['Numerator']   =  h_Shape.Clone()
                shapes[particle][region][metcut]['Denominator'] =  h_DY.Clone()

	        h_Shape.Divide(h_DY)
                shapes[particle][region][metcut]['Shape']  =  h_Shape.Clone()

                # Create a canvas
	        canvas = ROOT.TCanvas("c", "c", 800, 800)
                h_Shape.GetXaxis().SetRangeUser(100,1000)
                h_Shape.GetYaxis().SetRangeUser(-0.2,3)
                # Draw legend
	        legend = ROOT.TLegend(0.5, 0.7, 0.9, 0.9)
	        legend.AddEntry(h_Shape, 'Shape', '1')
	        legend.AddEntry(h_Data, 'Data', '1')
	        legend.Draw()
                # Draw histogram
	        h_Shape.Draw('error')
	        canvas.Update()
                # Save new Histogram as png and root
                err = "{}".format("" if not metcut else "_")
                file_name = 'DataMC_' + particle + '_' + region + '_' + metcut + err + 'met_' + year + 'metWithLL_Shape.png'
	        canvas.SaveAs(file_name)
                # Write histogram in root file
                h_Shape.Write()

#--------------------------------------------------------------------------------------------------------------

# Calculating Normalization

norms = {}

bin_1  = 0 
bin_2 = shapes['Electron']['LowDM']['']['Data'].GetNbinsX()

for particle in particles:
    norms[particle] = {}
    for region in regions:
        norms[particle][region] = {}

            I_Numerator   = shapes[particle][region][""]['Numerator'].Integral(bin_1, bin_2)
            I_Denominator = shapes[particle][region][""]['Denominator'].Integral(bin_1, bin_2)

#--------------------------------------------------------------------------------------------------------------

            print "In " + particle + " " + region + " " + metcut
            print "I_Numerator = " + str(I_Numerator)
            print "I_Denominator = " + str(I_Denominator)
            print "R_Z = " + str(norms[particle][region][metcut]['R_Z'])

# Canvas

            h_Shape.GetXaxis().SetRangeUser(100,1000)
            h_Shape.GetYaxis().SetRangeUser(-0.2,3)

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

# Save new Histogram as png and root

	    if not metcut:
                file_name = prefix + 'met_' + year + 'metWithLL_Shape.png'
            else:
                file_name = prefix + '_met_' + year + 'metWithLL_Shape.png'

	    canvas.SaveAs(file_name)

            h_Shape.Write()

            print "\n\nafter saving histogram in root file\n\n"

# End of loop--------------------------------------------------------------------------------

# Combine normalization and shape factors

for region in regions:
    for metcut in metcuts:
        if metcut == 'MidHT' and region == 'LowDM':
            continue
    
	print 'We are now in: ' + region + ' ' + metcut  #debbuging
        print 'Combine: ' + str(norms['Combine'][region][metcut]['Numerator']) + " " + str(norms['Combine'][region][metcut]['Denominator']) + " " + str(norms['Combine'][region][metcut]['R_Z'])
        print 'Electron: ' + str(norms['Electron'][region][metcut]['Numerator']) + " " + str(norms['Electron'][region][metcut]['Denominator']) + " " + str(norms['Electron'][region][metcut]['R_Z'])
        print 'Muon: ' + str(norms['Muon'][region][metcut]['Numerator']) + " " + str(norms['Muon'][region][metcut]['Denominator']) + " " + str(norms['Muon'][region][metcut]['R_Z'])


        norms['Combine'][region][metcut]['Numerator'] = norms['Electron'][region][metcut]['Numerator'] +  norms['Muon'][region][metcut]['Numerator'] 
        norms['Combine'][region][metcut]['Denominator'] =  norms['Electron'][region][metcut]['Denominator'] +  norms['Muon'][region][metcut]['Denominator']
        norms['Combine'][region][metcut]['R_Z'] = norms['Combine'][region][metcut]['Numerator'] / norms['Combine'][region][metcut]['Denominator']

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
            with open('normalizations_mets.txt', 'a+') as sheet:
                sheet.write(year + " " + region + " " + particle + " " + metcut + " : " + str(norms[particle][region][metcut]['R_Z']) + "\n")

f.Close()
