#ShapeNormGen.py
# calcualte shape and normalization factors for different variables

import ROOT       
import math as m
import sys
sys.path.append('./modules')
from LoadHistograms import *

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)


location  =  sys.argv[1]
year      =  sys.argv[2]

################################################################################################################################

def ShapeNormFactors(location):
    """Load root file and calculate shape and normalization factors with different variables.
       The output is a dictionary: factors[variable][region][particle][fattore]."""

    #---------------
    # definitions
    #---------------
    
    # for histos
    metcuts    =  ['', 'Loose']
    mcdata     =  ['Data', 'DY', 'Sint', 'TTbar', 'Rare']
    
    # for factors
    variables  =  ['nj', 'ht', 'met'] # add more latter
    fattori    =  ['shape', 'norm']
    particles  =  ['Electron', 'Muon', 'Combined']
    regions    =  ['HighDM', 'LowDM']

    # factors[variable][region][particle][fattore]
    factors = {v: {r: {p: dict.fromkeys(fattori) for p in particles} for r in regions} for v in variables}

    #-------------------
    # load histograms
    #-------------------
    
    # histos[variable][region][particle][metcut][mcdata]
    histos = ForShapeNorm(location)

    #----------------------
    # calculate factors
    #----------------------

    for variable in variables:
        for region in regions:
            for particle in particles:
                if (particle == 'Combined'):
                    continue 
    
                # print("we are in: {} {} {}".format(variable, region, particle))
    
                #----------------------------------------------------
                # shape factors
                #----------------------------------------------------
    
                factors[variable][region][particle]['shape'] = histos[variable][region][particle]['Loose']['Data'].Clone()
                factors[variable][region][particle]['shape'].SetName('shape_' + variable + '_' + particle + '_' + region)
                factors[variable][region][particle]['shape'].Add(    histos[variable][region][particle]['Loose']['TTbar'], -1)
                factors[variable][region][particle]['shape'].Add(    histos[variable][region][particle]['Loose']['Rare'] , -1)
                factors[variable][region][particle]['shape'].Add(    histos[variable][region][particle]['Loose']['Sint'] , -1)
                factors[variable][region][particle]['shape'].Divide( histos[variable][region][particle]['Loose']['DY']       )
        
                #----------------------------------------------------
                # normalization factors
                #----------------------------------------------------
        
                nbins  =  histos[variable][region][particle]['']['Data'].GetNbinsX()
                start  =  0 
                end    =  nbins + 1
                
                # numerator
                h_norm  =   histos[variable][region][particle]['']['Data'].Clone()
                h_norm.Add( histos[variable][region][particle]['']['TTbar'], -1)
                h_norm.Add( histos[variable][region][particle]['']['Rare'] , -1)
                h_norm.Add( histos[variable][region][particle]['']['Sint'] , -1)
                numerator = h_norm.Integral(start, end)
        
                # denominator
                h_norm = histos[variable][region][particle]['']['DY'].Clone()
                h_norm.Multiply(factors[variable][region][particle]['shape'])
                denominator = h_norm.Integral(start, end)
        
                factors[variable][region][particle]['norm'] = numerator/denominator
        
            #----------------------------------------------------
            # merging electron and muons (weighted average) 
            #----------------------------------------------------
    
            name   =  '{}_shape_Combined_{}_{}'.format(variable, region, year)
            factors[variable][region]['Combined']['shape']  =  ROOT.TH1F( name, name, nbins, start, end)
                
            for k in range(start, end):
            
                e   =  factors[variable][region]['Electron']['shape'].GetBinContent(k)
                de  =  factors[variable][region]['Electron']['shape'].GetBinError(k)
                u   =  factors[variable][region]['Muon']['shape'].GetBinContent(k)
                du  =  factors[variable][region]['Muon']['shape'].GetBinError(k)
            
                if de == 0:
                    factors[variable][region]['Combined']['shape'].SetBinContent(k, 0)
                    factors[variable][region]['Combined']['shape'].SetBinError(k, 0)
                    continue
                else:
                    we = (1/de)**2
            
                wu = (1/du)**2
            
                c   =  (e * we + u * wu)/(we + wu) 
                dc  =   1/m.sqrt(we + wu)
            
                factors[variable][region]['Combined']['shape'].SetBinContent(k, c)
                factors[variable][region]['Combined']['shape'].SetBinError(k, dc)

    print("Calculation of shape and norm factors has been successful")

    return factors
    
################################################################################################################################

if __name__ == '__main__':

    #----------------------------------------------------
    # create root and png
    #----------------------------------------------------
    variables  =  ['nj', 'ht', 'met'] 
    particles  =  ['Electron', 'Muon', 'Combined']
    regions    =  ['HighDM', 'LowDM']
    
    factors  =  ShapeNormFactors(location)
    
    f = ROOT.TFile('factors_' + year + '.root', 'recreate')
    
    for variable in variables: 
        for particle in particles:
            for region in regions:
                fattore = 'shape'
    
                print("we are in: {} {} {} {}".format(variable, particle, region, fattore))
    
                # canvas
                canvas = ROOT.TCanvas('c', 'c', 800, 800)
        
                # legend
                legend = ROOT.TLegend(0.5, 0.7, 0.9, 0.9)
                legend.AddEntry(factors[variable][region][particle][fattore], fattore, 'l' )
                legend.Draw()
    
                factors[variable][region][particle][fattore].Draw('error')
    
                canvas.Update()
                factors[variable][region][particle][fattore].Write()
    
                # png
                #file_name = factor + '_' + particle + '_' + region + '_' + year + '_' + variable + '.png'
                file_name = '{}_{}_{}_{}'.format(variable, particle, fattore, region) + '.png'
                canvas.SaveAs(file_name)
    
                print(file_name)
    
    f.Close()
