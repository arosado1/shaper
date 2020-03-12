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

def CalebYield(validation_l, search_l):
    """Load Caleb's validation bins histograms"""

    binns      =  ['Validation', 'Search']
    locations  =  [validation_l, search_l]
    Regions    =  ['lowdm', 'highdm']
    regions    =  ['Low', 'High']
    
    # histos[binn][region]
    histos  = { b: dict.fromkeys(regions) for b in binns }

    for location, binn in zip(locations,binns):
        for Region, region in zip(Regions, regions):

            root_file = ROOT.TFile.Open(location)
    
            name  =  'pred_' + Region
            histos[binn][region]  =  root_file.Get( name )
    
            if not histos[binn][region]:
                print( "Error, histogram doesn't exist: " + name )
            histos[binn][region].SetDirectory(0)                

    print("Loading histograms has been successful")

    # histos[binn][region]
    return histos

#####################################################################################################################################

def CalebSyst(validation_l, search_l):
    """Load Caleb's validation bins systematics"""

    binns       =  ['Validation', 'Search']
    locations   =  [validation_l, search_l]
    Regions     =  ['lowdm', 'highdm']
    regions     =  ['Low', 'High']
    directions  =  ['up', 'down']
    
    # histos[binn][region][direction]
    histos  = { b: { r: dict.fromkeys(directions) for r in regions } for b in binns}

    for location, binn in zip(locations,binns):
        for Region, region in zip(Regions, regions):
            for direction in directions:

                root_file  =  ROOT.TFile.Open(location)

                name  =  'syst_{}_{}'.format(direction, Region)
                histos[binn][region][direction]  =  root_file.Get( name ) 
        
                if not histos[binn][region][direction]:
                    print("Error, histogram doesn't exist: " + name)
                histos[binn][region][direction].SetDirectory(0)                
    
    print("Loading histograms has been successful")

    # histos[binn][region][direction]
    return histos

#####################################################################################################################################

def CalebHists(location):
    """ An economic version to deal with"""

    val_yield  =  location + "/validationBinsZinv_2016.root"
    sea_yield  =  location + "/searchBinsZinv_2016.root"

    val_syst  =  location + "/validationBinsZinv_syst_Run2.root"
    sea_syst  =  location + "/searchBinsZinv_syst_Run2.root"

    y  =  CalebYield( val_yield, sea_yield )
    s  =  CalebSyst( val_syst, sea_syst )

    # CalebYield(), CalebSyst()
    return y, s

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

