# ShapeNormGen.py
# Calcualte shape and normalization factors for different variables

import ROOT       
import math as m
import sys
sys.dont_write_bytecode = True
sys.path.append('./modules')
from WeightedAverager import *
from LoadHistograms import *

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

################################################################################################################################

def ShapeNormFactors(location):
    """Calculate shape and normalization factors with different variables.
       The output is a dictionary: factors[variable][region][particle][fattore]."""

    #---------------
    # definitions
    #---------------
    
    # for histos
    metcuts    =  ['', 'Loose']
    mcdata     =  ['Data', 'DY', 'Sint', 'TTbar', 'Rare']
    
    # for factors
    variables  =  ['nj','ht','met', 'ptb', 'nw', 'nrt', 'nmt', 'nb', 'mtb'] #, 'isr']
    fattori    =  ['shape', 'norm', 'normunc']
    particles  =  ['Electron', 'Muon', 'Combined']
    regions    =  ['High', 'Low']

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

    num_error = ROOT.Double(0)
    den_error = ROOT.Double(0)

    for variable in variables:
        for region in regions:
            for particle in particles:
                if (particle == 'Combined'):
                    continue 
    
                #print("we are in: {} {} {}".format(variable, region, particle))
    
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
                start  =  1 
                end    =  nbins
                
                # numerator
                h_norm  =   histos[variable][region][particle]['']['Data'].Clone()
                h_norm.Add( histos[variable][region][particle]['']['TTbar'], -1)
                h_norm.Add( histos[variable][region][particle]['']['Rare'] , -1)
                h_norm.Add( histos[variable][region][particle]['']['Sint'] , -1)
                numerator = h_norm.IntegralAndError(start, end, num_error)
                #print("numerator = {} and error = {}".format(numerator, num_error))        

                # denominator
                h_norm = histos[variable][region][particle]['']['DY'].Clone()
                h_norm.Multiply(factors[variable][region][particle]['shape'])
                denominator = h_norm.IntegralAndError(start, end, den_error)
                #print("denominator = {} and error = {}".format(denominator, den_error))        
        
                # norm
                factors[variable][region][particle]['norm'] = numerator/denominator

                # uncertainty

                abe = (num_error/numerator)**2 + (den_error/denominator)**2
                factors[variable][region][particle]['normunc'] = factors[variable][region][particle]['norm'] * m.sqrt(abe)

                #print("Normalization factor for {} {} {} is: {} +- {}".format(variable, region, particle, numerator/denominator, factors[variable][region][particle]['normunc']) )
        
            #----------------------------------------------------
            # merging electron and muons (weighted average) 
            #----------------------------------------------------

            # combined shape factors
            name  =  '{}_shape_Combined_{}DM'.format(variable, region)
            #factors[variable][region]['Combined']['shape']  =  ROOT.TH1F( name, name, nbins, 0, 1000)
            factors[variable][region]['Combined']['shape']  =  factors[variable][region]['Electron']['shape'].Clone()
            factors[variable][region]['Combined']['shape'].SetName(name)
                
            for k in range(start, end):
            
                e   =  factors[variable][region]['Electron']['shape'].GetBinContent(k)
                de  =  factors[variable][region]['Electron']['shape'].GetBinError(k)
                u   =  factors[variable][region]['Muon']['shape'].GetBinContent(k)
                du  =  factors[variable][region]['Muon']['shape'].GetBinError(k)
            
                if de == 0:
                    factors[variable][region]['Combined']['shape'].SetBinContent(k, u)
                    factors[variable][region]['Combined']['shape'].SetBinError(k, du)
                    continue
                elif du == 0:
                    factors[variable][region]['Combined']['shape'].SetBinContent(k, e)
                    factors[variable][region]['Combined']['shape'].SetBinError(k, de)
                    continue
                else:
                    we = (1/de)**2
            
                wu = (1/du)**2
            
                c   =  (e * we + u * wu)/(we + wu) 
                dc  =   1/m.sqrt(we + wu)
            
                factors[variable][region]['Combined']['shape'].SetBinContent(k, c)
                factors[variable][region]['Combined']['shape'].SetBinError(k, dc)

            # combined norm factors

            e   =  factors[variable][region]['Electron']['norm']    
            de  =  factors[variable][region]['Electron']['normunc'] 
            u   =  factors[variable][region]['Muon']['norm']        
            du  =  factors[variable][region]['Muon']['normunc']     

            c, dc  =  WeightedAverage(e, de, u, du)

            factors[variable][region]['Combined']['norm']     =  c
            factors[variable][region]['Combined']['normunc']  =  dc

    print("Calculation of shape and norm factors has been successful")

    # factors[variable][region][particle][fattore]
    return factors
    
################################################################################################################################

if __name__ == '__main__':

    #----------------------------------------------------
    # create root and png of shape factor
    #----------------------------------------------------
    fattore = 'shape'

    variables  =  ['nj','ht','met', 'ptb', 'nw', 'nrt', 'nmt', 'nb', 'mtb'] #, 'isr']
    particles  =  ['Electron', 'Muon', 'Combined']
    regions    =  ['High', 'Low']

    location  =  sys.argv[1]
    year      =  sys.argv[2]

    factors  =  ShapeNormFactors(location)
    
    f = ROOT.TFile('outputs/factors_' + year + '.root', 'recreate')
    
    for variable in variables: 
        for particle in particles:
            for region in regions:
    
                #print("we are in: {} {} {} {}".format(variable, particle, region, fattore))
    
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
                file_name = 'outputs/{}_{}_{}_{}'.format(variable, particle, fattore, region) + '.png'
                canvas.SaveAs(file_name)
    
                print(file_name)
    
    f.Close()

    #----------------------------------------------------
    # create text of normalization factor
    #----------------------------------------------------
    fattore = 'norm'

    with open('outputs/norm.txt', 'w') as sheet:
        sheet.write('###########################\n')
        sheet.write('{}\n'.format(year))
        sheet.write('###########################\n\n')
        sheet.write('{:<24s} {:<9s} {:<8s}\n\n'.format('selection', 'norm', 'stat_unc') )
        for variable in variables: 
            for particle in particles:
                for region in regions:

                    sheet.write( '{:<4s} {:<9s} {:<5s} {:10.5f} {:10.5f}\n'.format(variable, particle, region, factors[variable][region][particle][fattore], factors[variable][region][particle]['normunc']) )


