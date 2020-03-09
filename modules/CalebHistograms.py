# Load Caleb's Histograms 

import ROOT       
import sys

# make sure ROOT.TFile.Open(fileURL) does not seg fault when $ is in sys.argv (e.g. $ passed in as argument)
ROOT.PyConfig.IgnoreCommandLineOptions = True
# make plots faster without displaying them
ROOT.gROOT.SetBatch(ROOT.kTRUE)

#ROOT.PyConfig.fAddDirectory(kFalse)

#####################################################################################################################################

def CalebValHistos(location_1, location_2):
    """Load Caleb's validation bins histograms"""

    root_yield = ROOT.TFile.Open(location_1)
    root_syst  = ROOT.TFile.Open(location_2)

    Regions  =  ['lowdm', 'highdm']
    regions  =  ['Low', 'High']
    data     =  ['yield', 'syst']
    
    # histos[region][datum]
    histos  =  { r : dict.fromkeys(data) for r in regions }

    for Region, region in zip(Regions, regions):

        histos[region]['yield']  =  root_yield.Get( 'pred_' +  Region )
        histos[region]['syst']   =  root_syst.Get( 'syst_up_' +  Region ) #something better than this needs to be done

        if not histos[region]['yield']:
            print("Error, histogram doesn't exist: pred_{}").format(Region)
        histos[region]['yield'].SetDirectory(0)                
        if not histos[region]['syst']:
            print("Error, histogram doesn't exist: syst_up_{}").format(Region)
        histos[region]['syst'].SetDirectory(0)                

    print("Loading histograms has been successful")

    # histos[region][datum]
    return histos

#####################################################################################################################################

if __name__ == '__main__':
    """Plot Caleb's prediction and systematics"""

    regions  =  ['Low', 'High']
    data     =  ['yield', 'syst']

    location_1  =  sys.argv[1]
    location_2  =  sys.argv[2]

    # histos[region][datum]
    histos  =  CalebValHistos(location_1, location_2)

    for region in regions:
        for datum in data:

            # canvas
            canvas = ROOT.TCanvas('c', 'c', 800, 800)
    
            ROOT.gPad.SetLogy(1)

            # legend
            #legend = ROOT.TLegend(0.5, 0.7, 0.9, 0.9)
            #legend.AddEntry(histos[region][datum], region + '_' + datum, 'l' )
            #legend.Draw()
    
            histos[region][datum].Draw('error')
    
            canvas.Update()
            histos[region][datum].Write()
    
            file_name = '../outputs/CalebVal_{}_{}'.format(region, datum) + '.png'
            canvas.SaveAs(file_name)
    
            print(file_name)



