# produce png and root of:
#    shape factor
#    prediction factor = shape factor x normalization factor
# normalization factor is display in pred factor

import sys
import os          #what is this for???
import ROOT       
import math as m

# make sure ROOT.TFile.Open(fileURL) does not seg fault when $ is in sys.argv (e.g. $ passed in as argument)
ROOT.PyConfig.IgnoreCommandLineOptions = True
# make plots faster without displaying them
ROOT.gROOT.SetBatch(ROOT.kTRUE)

#----------------------------------------------------
# open root file and create factors.root
#----------------------------------------------------

location  =  sys.argv[1]
year      =  sys.argv[2]

root_file = ROOT.TFile.Open(location)

#variable   =  'nJets_drLeptonCleaned_jetpt30'
#variable   =  'metWithLL'
variable    =  'HT_drLeptonCleaned_jetpt30'

f = ROOT.TFile('factors_' + year + '_' + variable + '.root', 'recreate')

#----------------------------------------------------
# load histograms
#----------------------------------------------------

particles     =  ['Electron', 'Muon']
regions       =  ['HighDM', 'LowDM']
metcuts       =  ['', 'Loose']
mcdata        =  ['Data', 'DY', 'Sint', 'TTbar', 'Rare']
factores      =  ['norm', 'shape', 'pred', 'combine']
# variables   =  ['nJets_drLeptonCleaned_jetpt30', 'HT_drLeptonCleaned_jetpt30', 'metWithLL']

# histosi[variable][particle][region][metcut][mcdata]
histos = {v: {p: {r: {m: dict.fromkeys(mcdata) for m in metcuts} for r in regions} for p in particles} for v in variable}

for variable in variables:
    for particle in particles:
        for region in regions:
            for metcut in metcuts: 
    
                print('\n')
    	        print('We are now in: ' + variable + ' ' + particle + ' ' + region + ' ' + metcut) #debbuging
                print('\n')
    
                err = "{}".format("" if not metcut else "_")
                prefix = 'DataMC_' + particle + '_' + region + '_' + metcut + err
    
                for mcd, mcds in zip(mcdata, ['Datadata', 'DYstack', 'Single tstack', 't#bar{t}stack', 'Rarestack']):
    
                    # example of name: DataMC_Electron_HighDM_njetWeight_met_jetpt30_2016metWithLLmetWithLLDatadata
    
                    histos[variable][particle][region][metcut][mcd] = root_file.Get(variable + '/' + prefix + 'ht_jetpt30_' + year + 2*variable + mcds)
                    
                    if not histos[variable][particle][region][metcut][mcd]:
    		        print(variable + '/' + prefix + 'ht_jetpt30_' + year + 2*variable + mcds + " doesn't exist!") 
    
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
            factors[particle][region]['shape'].SetName("shape_njets_" + year + "_" + particle + '_' + region + '_Loose')
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
            factors[particle][region]['pred'].SetName("prediction_njets_" + year + "_" + particle + '_' + region + '_Loose')
    
    #----------------------------------------------------
    # combined prediction factor
    #----------------------------------------------------
    
    for region in regions:
    
        nbins  =  10
        start  =  0
        end    =  10
        name   =  "prediction_njets_" + year + "_Combined_"  + region
    
        factors['Electron'][region]['combine']  =  ROOT.TH1F( name, name, nbins, start, end)
        factors['Muon'][region]['combine']  =  ROOT.TH1F( name, name, nbins, start, end)
        
        for k in range(1, 11):
        
            e   =  factors['Electron'][region]['pred'].GetBinContent(k)
            de  =  factors['Electron'][region]['pred'].GetBinError(k)
            u   =  factors['Muon'][region]['pred'].GetBinContent(k)
            du  =  factors['Muon'][region]['pred'].GetBinError(k)
        
            if de == 0:
                factors['Electron'][region]['combine'].SetBinContent(k, 0)
                factors['Electron'][region]['combine'].SetBinError(k, 0)
                factors['Muon'][region]['combine'].SetBinContent(k, 0)
                factors['Muon'][region]['combine'].SetBinError(k, 0)
                continue
            else:
                we = (1/de)**2
        
            wu = (1/du)**2
    
            c   =  (e * we + u * wu)/(we + wu) 
            dc  =   1/m.sqrt(we + wu)
        
            factors['Electron'][region]['combine'].SetBinContent(k, c)
            factors['Electron'][region]['combine'].SetBinError(k, dc)
            factors['Muon'][region]['combine'].SetBinContent(k, c)
            factors['Muon'][region]['combine'].SetBinError(k, dc)
    
    #----------------------------------------------------
    # create root and png
    #----------------------------------------------------
    
    for particle in particles:
        for region in regions:
            for factor in ('shape', 'pred', 'combine'):
    
                if (factor == 'combine' and particle == 'Muon'):
                    continue
          
                # canvas
                canvas = ROOT.TCanvas("c", "c", 800, 800)
        
                # legend
                legend = ROOT.TLegend(0.5, 0.7, 0.9, 0.9)
                legend.AddEntry(factors[particle][region][factor], factor, '1')
                legend.Draw()
    
                # normalization text box (not working)
                # norm_text = ROOT.TText(0.1, 0.1, "Normalization = " + str(factors[particle][region]['norm']))
                # norm_text.SetTextFont(20)
                # norm_text.DrawText(0.1, 0.1, "Normalization = " + str(factors[particle][region]['norm']))
                # t = ROOT.TLatex(-3,500,"TLatex at (-3,500)");
                # t.Draw();
        
                # histogram
                #factors[particle][region][factor].GetXaxis().SetRangeUser(2,10)
                #factors[particle][region][factor].GetYaxis().SetRangeUser(0,4)
                factors[particle][region][factor].Draw('error')
    
                canvas.Update()
                factors[particle][region][factor].Write()
    
                # png
                file_name = factor + '_' + particle + '_' + region + '_' + year + '_' + variable + '.png'
                canvas.SaveAs(file_name)
    
                print(file_name)
    

f.Close()
