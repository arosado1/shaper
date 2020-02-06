# Load Histograms 

import ROOT       

# make sure ROOT.TFile.Open(fileURL) does not seg fault when $ is in sys.argv (e.g. $ passed in as argument)
ROOT.PyConfig.IgnoreCommandLineOptions = True
# make plots faster without displaying them
ROOT.gROOT.SetBatch(ROOT.kTRUE)

#ROOT.PyConfig.fAddDirectory(kFalse)

def LoadBinHisto(location):
    """Load Validation and Search bins histograms"""

    root_file = ROOT.TFile.Open(location)

    regions    =  ['High', 'Low']
    variables  =  ['', 'nj','ht','met']
    binns      =  ['Validation'] # need to add Search

    # histos[variable][region]
    histos = {b: { v: dict.fromkeys(regions) for v in variables } for b in binns}

    for binn in binns:
        for variable in variables:
            for region in regions:

                print("\nWe are now in: {} {} {}\n".format(binn, variable, region))

                branch     =   "n{b}Bin{r}DM_jetpt30".format( b = binn, r = region)
                histogram  = ( "ZNuNu_n{b}Bin_{r}DM_{v}"
                               "jetpt30n{b}Bin{r}DM"
                               "_jetpt30n{b}Bin{r}DM"
                               "_jetpt30ZJetsToNuNu {b} Bin {r} DMdata" 
                             ).format( b = binn, r = region, v = variable + '{}'.format('' if not variable else '_shape_') )

                histos[binn][variable][region] = root_file.Get(branch + "/" + histogram)
                if not histos[binn][variable][region]:
                    print("Error, histogram doesn't exist: branch: {} \nhistogram: {}").format(branch, histogram)
                histos[binn][variable][region].SetDirectory(0)                

    root_file.Close()

    return histos

