# Comparison_diError.py (under construction)
# Compares both methods in Z to Invisible background

import ROOT
import math as m
import sys 
sys.dont_write_bytecode = True
sys.path.append('./modules')
from CalebHistograms import *
from Run2Prediction import *
from LoadHistograms import *
from Prediction import *

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

################################################################################################################################

def Compare(location_c):
    """ Returns predictions table and z_score plot """

    binns       =  ['Validation', 'Search']
    regions     =  ['Low', 'High']
    directions  =  ['up','down']

    location_2016  =  "../condor/DataMC_2016_submission_2020-04-01_02-48-55/result.root"
    location_2017  =  "../condor/DataMC_2017_submission_2020-04-01_02-51-55/result.root"
    location_2018  =  "../condor/DataMC_2018_submission_2020-04-01_02-53-31/result.root"
  
    yield_a, stat, shapesyst, mcsyst  =  Run2Prediction(location_2016, location_2017, location_2018)

    # zscore[binn][region]
    zscore  =  { b: dict.fromkeys(regions) for b in binns }
             
    # histos[binn][region], syst[binn][region][direction] 
    yield_c, syst_c  =  CalebHists(location_c) 

    for binn in binns:
        for region in regions:

            nbins  =  yield_a[binn][region].GetNbinsX()

            zscore[binn][region]  =  yield_a[binn][region].Clone()

            for k in range(1, nbins):

                ae  =  ( yield_a[binn][region].GetBinError(k) )**2
                asy =  ae

                m_u  =  ( mcsyst[binn][region]['up'].GetBinContent(k)   )**2
                m_d  =  ( mcsyst[binn][region]['down'].GetBinContent(k) )**2
                if m_u > m_d :
                    ae  +=  m_u 
                else:
                    ae  +=  m_d 
    
                s_u  =  ( shapesyst[binn][region]['up'].GetBinContent(k)   )**2
                s_d  =  ( shapesyst[binn][region]['down'].GetBinContent(k) )**2
                if s_u > s_d :
                    ae  +=  s_u 
                else:
                    ae  +=  s_d 
 
                ae  =  m.sqrt(ae)
                yield_a[binn][region].SetBinError(k, ae)

                #zscore
                a   =  yield_a[binn][region].GetBinContent(k) 
                c   =  yield_c[binn][region].GetBinContent(k)

                d  =  a - c

                ce  =  yield_c[binn][region].GetBinError(k)


                if ( d >= 0 ):

                    asy  =  ( m_d )**2 + ( s_d )**2
                    csy  =  ( syst_c[binn][region]['up'].GetBinContent(k) - 1 )*c

                elif ( d < 0 ):

                    asy  =  ( m_u )**2 + ( s_u )**2
                    csy  =  ( syst_c[binn][region]['down'].GetBinContent(k) - 1 )*c
                
                d /=  m.sqrt( asy  + csy**2 + ce**2 )

                yield_c[binn][region].SetBinError(k, m.sqrt( csy**2 + ce**2 ) )

                zscore[binn][region].SetBinContent(k, d)

    print('zscore calculation completed')

    # zscore[binn][region]
    return zscore, yield_c

################################################################################################################################

if __name__ == '__main__':

    binns      =  ['Validation', 'Search']
    regions    =  ['High', 'Low']
    direction  =  ['up','down']

    location_c  =  sys.argv[1]

    #histos[binn][region]
    zscore, caleb  =  Compare(location_c)

    for binn in binns:
        for region in regions:

            # draw histograms
            c = ROOT.TCanvas("c", "c", 800, 800)
            c.Divide(1, 2)
        
            # histograms
            c.cd(1)
            ROOT.gPad.SetLogy(1)

            location_2016  =  "../condor/DataMC_2016_submission_2020-04-01_02-48-55/result.root"
            location_2017  =  "../condor/DataMC_2017_submission_2020-04-01_02-51-55/result.root"
            location_2018  =  "../condor/DataMC_2018_submission_2020-04-01_02-53-31/result.root"
            angel, stat, shapesyst, mcsyst  =  Run2Prediction(location_2016, location_2017, location_2018)
          
            # ZInv MC and Prediction
            # angel[binn][region].SetTitle( '{}#DeltaM Validation Bins Z#rightarrow#nu#nu comparison'.format(region) )
            angel[binn][region].SetTitle( '{}#DeltaM Validation Bins methods comparison'.format(region) )

            angel[binn][region].Draw("hist error")
            angel[binn][region].SetLineColor(ROOT.kBlue)
            angel[binn][region].SetLineWidth(2)

            caleb[binn][region].Draw("hist error same")
            caleb[binn][region].SetLineWidth(2)
            caleb[binn][region].SetLineColor(ROOT.kRed)
        
            # legend: TLegend(x1,y1,x2,y2)
            legend = ROOT.TLegend( 0.75, 0.75, 0.9, 0.9)
            legend.AddEntry( angel[binn][region] , "Dilepton prediction", "l")
            legend.AddEntry( caleb[binn][region] , "Photon prediction", "l")
            legend.Draw()
        
            # ratios
            c.cd(2)
            zscore[binn][region].SetTitle('z-score')
            zscore[binn][region].GetYaxis().SetTitle('#sigma deviations')
            zscore[binn][region].SetLineColor(ROOT.kBlue)
            zscore[binn][region].SetLineWidth(2)
            zscore[binn][region].Draw("hist")
        
            # save histograms
            c.Update()
            file_name = "outputs/z_score_{}_{}.png".format(binn, region)
            c.SaveAs(file_name)

            c.Close()

