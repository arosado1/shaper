# Load Caleb's Histograms (under construction) 
# A search Bin version need to be done
# we want histos[binn][region] for yield
# we want histos[binn][region][direction] for syst

import ROOT       
import sys

# make sure ROOT.TFile.Open(fileURL) does not seg fault when $ is in sys.argv (e.g. $ passed in as argument)
ROOT.PyConfig.IgnoreCommandLineOptions = True
# make plots faster without displaying them
ROOT.gROOT.SetBatch(ROOT.kTRUE)

#ROOT.PyConfig.fAddDirectory(kFalse)

#####################################################################################################################################

def CalebValHistos(location):
    """Load Caleb's validation bins histograms"""

    root_yield = ROOT.TFile.Open(location_1)

    Regions  =  ['lowdm', 'highdm']
    regions  =  ['Low', 'High']
    
    # histos[region]
    histos  =  dict.fromkeys(regions)

    for Region, region in zip(Regions, regions):

        name  =  'pred_' + Region

        histos[region]  =  root_yield.Get( name )

        if not histos[region]:
            print( "Error, histogram doesn't exist: " + name )
        histos[region].SetDirectory(0)                

    print("Loading histograms has been successful")

    # histos[region]
    return histos

#####################################################################################################################################

def CalebValSyst(location):
    """Load Caleb's validation bins systematics"""

    root_yield = ROOT.TFile.Open(location)

    Regions     =  ['lowdm', 'highdm']
    regions     =  ['Low', 'High']
    directions  =  ['up', 'down']
    
    # histos[region][direction]
    histos  =  dict.fromkeys(regions)

    for Region, region in zip(Regions, regions):
        for direction in directions:

            name  =  'syst_{}_{}'.format(direction, Region)
    
            histos[region][direction]  =  root_syst.Get( name ) 
    
                if not histos[region][direction]:
                    print("Error, histogram doesn't exist: " + name)
                histos[region][direction].SetDirectory(0)                
    
    print("Loading histograms has been successful")

    # histos[region][direction]
    return histos

#####################################################################################################################################

#if __name__ == '__main__':
#
#    regions  =  ['Low', 'High']
#    data     =  ['yield', 'syst']
#
#    location_1  =  sys.argv[1]
#    location_2  =  sys.argv[2]
#
#    # histos[region][datum]
#    histos  =  CalebValHistos(location_1, location_2)
#
#    for region in regions:
#        for datum in data:
#
#            # canvas
#            canvas = ROOT.TCanvas('c', 'c', 800, 800)
#    
#            ROOT.gPad.SetLogy(1)
#
#            # legend
#            #legend = ROOT.TLegend(0.5, 0.7, 0.9, 0.9)
#            #legend.AddEntry(histos[region][datum], region + '_' + datum, 'l' )
#            #legend.Draw()
#    
#            histos[region][datum].Draw('error')
#    
#            canvas.Update()
#            histos[region][datum].Write()
#    
#            file_name = '../outputs/CalebVal_{}_{}'.format(region, datum) + '.png'
#            canvas.SaveAs(file_name)
#    
#            print(file_name)



