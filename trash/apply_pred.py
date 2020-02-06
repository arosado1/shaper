# produce png and root of:
#    shape factor
#    prediction factor = shape factor x normalization factor
# normalization factor is display in pred factor

import sys
import os          #what is this???
import ROOT       
import math as m

# make sure ROOT.TFile.Open(fileURL) does not seg fault when $ is in sys.argv (e.g. $ passed in as argument)
ROOT.PyConfig.IgnoreCommandLineOptions = True
# make plots faster without displaying them
ROOT.gROOT.SetBatch(ROOT.kTRUE)

#----------------------------------------------------
# open root file and create factors.root
#----------------------------------------------------

location = sys.argv[1]
year  = sys.argv[2]

root_file = ROOT.TFile.Open(location)
in_root = 'nJets_drLeptonCleaned_jetpt30'

#----------------------------------------------------
# load histograms
#----------------------------------------------------

particles  =  ['Electron', 'Muon']
regions    =  ['HighDM', 'LowDM']
metcuts    =  ['', 'Loose']
mcdata     =  ['Data', 'DY', 'Sint', 'TTbar', 'Rare']
factores   =  ['norm', 'shape', 'pred', 'combine']

# histos[particle][region][metcut][mcdata]
histos = {p: {r: {m: dict.fromkeys(mcdata) for m in metcuts} for r in regions} for p in particles}

for particle in particles:
    for region in regions:
        for metcut in metcuts: 

	    print('We are now in: ' + particle + ' ' + region + ' ' + metcut) #debbuging

            err = "{}".format("" if not metcut else "_")
            prefix = 'DataMC_' + particle + '_' + region + '_' + metcut + err

            for mcd, mcds in zip(mcdata, ['Datadata', 'DYstack', 'Single tstack', 't#bar{t}stack', 'Rarestack']):
                histos[particle][region][metcut][mcd] = root_file.Get(in_root + '/' + prefix + 'nj_jetpt30_' + year + 'nJets_drLeptonCleaned_jetpt30nJets_drLeptonCleaned_jetpt30' + mcds)
                
                if not histos[particle][region][metcut][mcd]:
		    print(in_root + '/' + histos[particle][region][metcut][mcd] + " doesn't exist!") 

#----------------------------------------------------
# calculate factors
#----------------------------------------------------

# shapes[particle][region][factor]
factors = {p: {r: dict.fromkeys(factores) for r in regions} for p in particles}

for particle in particles:
    for region in regions:

        #----------------------------------------------------
        # shape factor
        #----------------------------------------------------

        factors[particle][region]['shape'] = histos[particle][region]['Loose']['Data'].Clone()
        factors[particle][region]['shape'].SetName("shape_njets_" + year + "_" + particle + '_' + region + 'Loose')
        factors[particle][region]['shape'].Add(histos[particle][region]['Loose']['TTbar'], -1)
        factors[particle][region]['shape'].Add(histos[particle][region]['Loose']['Rare'], -1)
        factors[particle][region]['shape'].Add(histos[particle][region]['Loose']['Sint'], -1)
        factors[particle][region]['shape'].Divide( histos[particle][region]['Loose']['DY'] )

        #----------------------------------------------------
        # normalization factor
        #----------------------------------------------------

        bin_1  = 0 
        bin_2 = histos[particle][region]['']['Data'].GetNbinsX()
        
        # numerator
        h_norm = histos[particle][region]['']['Data'].Clone()
        h_norm.Add(histos[particle][region]['']['TTbar'], -1)
        h_norm.Add(histos[particle][region]['']['Rare'], -1)
        h_norm.Add(histos[particle][region]['']['Sint'], -1)
        numerator = h_norm.Integral(bin_1, bin_2)

        # denominator
        h_norm = histos[particle][region]['']['DY'].Clone()
        h_norm.Multiply(factors[particle][region]['shape'])
        denominator = h_norm.Integral(bin_1, bin_2)

        factors[particle][region]['norm'] = numerator/denominator

        #----------------------------------------------------
        # prediction factor
        #----------------------------------------------------

        factors[particle][region]['pred'] = factors[particle][region]['shape'].Clone()
        factors[particle][region]['pred'].Scale(factors[particle][region]['norm'])

#----------------------------------------------------
# create root and png
#----------------------------------------------------
          
stack = ROOT.THStack("Is this the name?", "what is this???")

histos[particle][region]['']['DY'].SetFillColor(ROOT.kBlue)
histos[particle][region]['']['Sint'].SetFillColor(ROOT.kGreen)
histos[particle][region]['']['Rare'].SetFillColor(ROOT.kYellow)
histos[particle][region]['']['TTbar'].SetFillColor(ROOT.kPink)

stack.Add(histos[particle][region]['']['TTbar'])
stack.Add(histos[particle][region]['']['Rare'])
stack.Add(histos[particle][region]['']['Sint'])
stack.Add(histos[particle][region]['']['DY'])

#----------------------------------------------------
# create canvas
#----------------------------------------------------

print("we are in: " + particle + " " + region)

# canvas
canvas = ROOT.TCanvas("c", "c", 800, 900)
canvas.Divide(1,2)

# setting first gPad
canvas.cd(1)
ROOT.gPad.SetPad("p1", "p1", 0, 2.5 / 9.0, 1, 1, ROOT.kWhite, 0, 0)
ROOT.gPad.SetBottomMargin(0.01)
ROOT.gPad.SetLogy()
ROOT.gPad.SetLeftMargin(0.15)
ROOT.gPad.SetRightMargin(0.06)
ROOT.gPad.SetTopMargin(0.06 * (8.0 / 6.5))

canvas.cd(2)
ROOT.gPad.SetPad("p2", "p2", 0, 0, 1, 2.5 / 9.0, ROOT.kWhite, 0, 0);

factors[particle][region]['shape'].Draw()

canvas.cd(1)

# legend
legend = ROOT.TLegend(0.5, 0.7, 0.9, 0.9)
legend.AddEntry(stack, '1')
legend.Draw()


# histogram
# stack.GetXaxis().SetRangeUser(2,10)

stack.Draw('histo')

#-----------------------------------------------------------------

canvas.Update()

# png
file_name = 'stack_' + particle + '_' + region + '_' + year + '.png'
canvas.SaveAs(file_name)

print(file_name)
    

