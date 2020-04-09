# Prediction.py (result table and plot) 
# Make Z to invisible prediction table and histograms 

import ROOT
import math as m
import sys 
sys.dont_write_bytecode = True
sys.path.append('./modules')
from LoadHistograms import *
from ShapeNormGen import *
from ShapeSyst import *
from MCSyst import *

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

################################################################################################################################

def Prediction(location):
    """Combines all 3 years and make Z to invisible prediction table and histogram"""

    regions     =  ['Low', 'High']
    plots       =  ['mc', 'pred']
    directions  =  ['up', 'down']
    binns       =  ['Validation', 'Search']

    # histo[binn][variable][region]
    temp_1  =  LoadBinHisto(location)
    # shape[binn][variable][region]
    temp_2  =  ShapeSyst(location)
    # histos[binn][direction][region]
    temp_3  =  TotalSyst(location)
    # factors[variable][region][particle][fattore]
    norm  =  ShapeNormFactors(location)

    pred       =  { b: dict.fromkeys(regions) for b in binns }
    stat       =  { b: { r: dict.fromkeys(directions) for r in regions } for b in binns }
    shapesyst  =  { b: { r: dict.fromkeys(directions) for r in regions } for b in binns }
    mcsyst     =  { b: { r: dict.fromkeys(directions) for r in regions } for b in binns }

    # loading histograms
    for binn in binns:
        for region in regions:

            pred[binn][region]  =  temp_1[binn]['nj'][region].Clone()

            stat[binn][region]['up']    =  pred[binn][region].Clone() 
            stat[binn][region]['down']  =  pred[binn][region].Clone() 

            nbins = pred[binn][region].GetNbinsX()

            for k in range(1, nbins):

                u  =  pred[binn][region].GetBinContent(k)  +  pred[binn][region].GetBinError(k)
                d  =  pred[binn][region].GetBinContent(k)  -  pred[binn][region].GetBinError(k)
                stat[binn][region]['up'].SetBinContent(k, u) 
                stat[binn][region]['down'].SetBinContent(k, d)

            mcsyst[binn][region]['up']  =  pred[binn][region].Clone()
            mcsyst[binn][region]['up'].Multiply(temp_3[binn]['up'][region])
            mcsyst[binn][region]['up'].Add(pred[binn][region], -1)
            
            mcsyst[binn][region]['down']  =  pred[binn][region].Clone()
            mcsyst[binn][region]['down'].Multiply(temp_3[binn]['down'][region])
            mcsyst[binn][region]['down'].Scale(-1)
            mcsyst[binn][region]['down'].Add(pred[binn][region], 1)

            shapesyst[binn][region]['up']  =  pred[binn][region].Clone()
            shapesyst[binn][region]['up'].Multiply(temp_2[binn]['total'][region]['up'])

            shapesyst[binn][region]['down']  =  pred[binn][region].Clone()
            shapesyst[binn][region]['down'].Multiply(temp_2[binn]['total'][region]['down'])

    return pred, stat, shapesyst, mcsyst

################################################################################################################################

#    with open('outputs/Results.txt', 'w') as sheet:
#        for binn in binns:
#            for region in regions:
#
#                histos[binn]['nj'][region].Scale( factors['nj'][region]['Combined']['norm'] )
#                rz  =  factors['nj'][region]['Combined']['norm']
#
#                nbins = histos[binn]['nj'][region].GetNbinsX()
#
#                sheet.write( '\n{} {}DM table, R_z = {}\n\n'.format(binn, region, rz) )
#                sheet.write('{:<10s}{:<9s}{:<12s}{:<11s}{:<11s}{:<11s}\n'.format('bin', 'yield', 'Stat unc', 'MCsyst unc', 'Shape unc', 'total_unc') ) 
#
#                print('bin counting, nbins = {}'.format(nbins)) # for debugging purposes
#
#                for k in range(1, nbins + 1): 
#
#                    val       =  histos[binn]['nj'][region].GetBinContent(k)
#                    stat      =  histos[binn]['nj'][region].GetBinError(k)
#                    shape_s   =  shapeSyst[binn]['total'][region]['up'].GetBinContent(k) 
#                    mc_s      =  mcsysts[binn]['up'][region].GetBinContent(k) 
#                    tot       =  m.sqrt( (stat**2) + (shape_s**2) + (mc_s**2) )
#
#                    line = '{:<3d}  {:10.4f}  {:10.4f}  {:10.4f}   {:10.4f}   {:10.4f}\n'.format(k, val, stat, mc_s, shape_s, tot)
#                    sheet.write(line) 
#                sheet.write('\n'+80*'#'+'\n')
#
#                # prediction plots
#                canvas = ROOT.TCanvas('c', 'c', 800, 800)
#
#                legend = ROOT.TLegend(0.5, 0.7, 0.9, 0.9)
#                legend.AddEntry(pred[binn][region], 'what?', 'l' )
#                legend.Draw()

################################################################################################################################

if __name__ == '__main__':

    location  =  sys.argv[1]
    year      =  sys.argv[2] 

    pred, stat, shapesyst, mcsyst  =  Prediction(location)

    regions     =  ['Low', 'High']
    plots       =  ['mc', 'pred']
    directions  =  ['up', 'down']
    binns       =  ['Validation', 'Search']

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

            pred[binn][region].SetTitle("Prediction")
            pred[binn][region].SetLineColor(ROOT.kBlack)
            pred[binn][region].SetLineWidth(2)

            statunc.SetFillColor(ROOT.kRed)
            otherunc.SetFillColor(ROOT.kBlue)
            shapeunc.SetFillColor(ROOT.kGreen)
            shapeunc.SetTitle('Prediction')

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
         
            file_name = '{}_{}_{}_prediction.png'.format(binn, region, year)
            canvas.SaveAs('outputs/' + file_name)


