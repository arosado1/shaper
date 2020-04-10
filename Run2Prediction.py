# Run2Prediction.py (result table and plot) 
# Make Z to invisible prediction table and histograms 

import ROOT
import math as m
import sys 
sys.dont_write_bytecode = True
from Prediction import *

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

################################################################################################################################

def Run2Prediction(location_1, location_2, location_3):
    """Combines all 3 years and make Z to invisible prediction table and histogram"""

    regions     =  ['Low', 'High']
    plots       =  ['mc', 'pred']
    directions  =  ['up', 'down']
    binns       =  ['Validation', 'Search']

    pred,   stat,   shapesyst,   mcsyst  =  Prediction(location_1)
    pred_2, stat_2, shapesyst_2, mcsyst_2  =  Prediction(location_2)
    pred_3, stat_3, shapesyst_3, mcsyst_3  =  Prediction(location_3)

    #pred       =  [binn][region]
    #stat       =  [binn][region][direction] 
    #shapesyst  =  [binn][region][direction] 
    #mcsyst     =  [binn][region][direction] 

    # loading histograms
    for binn in binns:
        for region in regions:

            pred[binn][region].Add(pred_2[binn][region])
            pred[binn][region].Add(pred_3[binn][region])

            nbins  =  pred[binn][region].GetNbinsX()

            for direction in directions:
                for k in range(1, nbins + 1):
 
                    a   =  ( stat[binn][region][direction].GetBinContent(k) )**2
                    a  +=  ( stat_2[binn][region][direction].GetBinContent(k) )**2
                    a  +=  ( stat_3[binn][region][direction].GetBinContent(k) )**2
                    a   =  m.sqrt(a) 
                    stat[binn][region][direction].SetBinContent(k, a)

                    a   =  ( shapesyst[binn][region][direction].GetBinContent(k) )**2
                    a  +=  ( shapesyst_2[binn][region][direction].GetBinContent(k) )**2
                    a  +=  ( shapesyst_3[binn][region][direction].GetBinContent(k) )**2
                    a   =  m.sqrt(a) 
                    shapesyst[binn][region][direction].SetBinContent(k, a)

                    a   =  ( mcsyst[binn][region][direction].GetBinContent(k) )**2
                    a  +=  ( mcsyst_2[binn][region][direction].GetBinContent(k) )**2
                    a  +=  ( mcsyst_3[binn][region][direction].GetBinContent(k) )**2
                    a   =  m.sqrt(a) 
                    mcsyst[binn][region][direction].SetBinContent(k, a)

    return pred, stat, shapesyst, mcsyst

################################################################################################################################

if __name__ == '__main__':

    location_1  =  sys.argv[1]
    location_2  =  sys.argv[2]
    location_3  =  sys.argv[3]

    regions     =  ['Low', 'High']
    plots       =  ['mc', 'pred']
    directions  =  ['up', 'down']
    binns       =  ['Validation', 'Search']

    
    pred, stat, shapesyst, mcsyst  =  Run2Prediction(location_1, location_2, location_3)

    for binn in binns:
        for region in regions:
    
            #print("We are now in: {} {}".format(binn, region))

            # canvas
            canvas = ROOT.TCanvas('c', 'c', 800, 800)
            ROOT.gPad.SetLogy()
         
            statunc   =  pred[binn][region].Clone()
            otherunc  =  pred[binn][region].Clone()
            shapeunc  =  pred[binn][region].Clone()

            nbins  =  pred[binn][region].GetNbinsX()

            for k in range(1, nbins + 1):

                #print("bin {}".format(k))

                a  =   0
                a  =   pred[binn][region].GetBinError(k)

                m_u  =  abs(mcsyst[binn][region]['up'].GetBinContent(k))
                m_d  =  abs(mcsyst[binn][region]['down'].GetBinContent(k))
                if m_u > m_d :
                    a  +=  m_u
                else:
                    a  +=  m_d
                otherunc.SetBinError(k, a)

                #print("firts a = {}".format(a))
                    
                s_u  =  abs(shapesyst[binn][region]['up'].GetBinContent(k))
                s_d  =  abs(shapesyst[binn][region]['down'].GetBinContent(k))
                if s_u > s_d :
                    a  +=  s_u
                else:
                    a  +=  s_d
                shapeunc.SetBinError(k, a)

                #print("second a = {}".format(a))

            pred[binn][region].SetTitle("Run 2 Prediction")
            pred[binn][region].SetLineColor(ROOT.kBlack)
            pred[binn][region].SetLineWidth(2)

            statunc.SetFillColor(ROOT.kRed)
            otherunc.SetFillColor(ROOT.kBlue)
            shapeunc.SetFillColor(ROOT.kGreen)
            shapeunc.SetTitle('Run 2 Prediction')

            shapeunc.Draw('e2')
            otherunc.Draw('e2 same')
            statunc.Draw('e2 same')
            pred[binn][region].Draw("hist same")

            #shapesyst[binn][region]['up'].Draw("same hist") 
            #shapesyst[binn][region]['up'].SetLineColor(ROOT.kBlue) 
            #shapesyst[binn][region]['down'].Draw("same hist") 
            #shapesyst[binn][region]['down'].SetLineColor(ROOT.kBlue) 

            #mcsyst[binn][region]['up'].Draw("same hist")
            #mcsyst[binn][region]['up'].SetLineColor(ROOT.kGreen)
            #mcsyst[binn][region]['down'].Draw("same hist")
            #mcsyst[binn][region]['down'].SetLineColor(ROOT.kGreen)

            # legend
            legend = ROOT.TLegend(0.5, 0.7, 0.9, 0.9)
            legend.AddEntry(pred[binn][region], 'yield', 'l' )
            legend.AddEntry(statunc, 'statistics unc', 'l' )
            legend.AddEntry(otherunc, 'others', 'l' )
            legend.AddEntry(shapeunc, 'shape unc', 'l' )
            legend.Draw()
         
            canvas.Update()
         
            file_name = '{}_{}_Run2_prediction.png'.format(binn, region)
            canvas.SaveAs('outputs/' + file_name)


