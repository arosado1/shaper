# Load Histograms 

import ROOT       
from LowDMHighMET_merger import *

# make sure ROOT.TFile.Open(fileURL) does not seg fault when $ is in sys.argv (e.g. $ passed in as argument)
ROOT.PyConfig.IgnoreCommandLineOptions = True
# make plots faster without displaying them
ROOT.gROOT.SetBatch(ROOT.kTRUE)

#ROOT.PyConfig.fAddDirectory(kFalse)

#####################################################################################################################################

def LoadBinHisto(location):
    """Load validation bins histograms with different shape correction factors applied"""

    root_file = ROOT.TFile.Open(location)

    regions    =  ['High', 'Low']
    variables  =  ['', 'nj','ht','met']
    binns      =  ['Validation'] # need to add "Search"

    # histos[binn][variable][region]
    histos = {b: { v: dict.fromkeys(regions) for v in variables } for b in binns}
    for binn in binns:
        for variable in variables:
            for region in regions:

                # print("\nWe are now in: {} {} {}\n".format(binn, variable, region))

                branch     =   "n{b}Bin{r}DM_jetpt30".format( b = binn, r = region)
                histogram  = ( "ZNuNu_n{b}Bin_{r}DM_{v}"
                               "jetpt30n{b}Bin{r}DM"
                               "_jetpt30n{b}Bin{r}DM"
                               "_jetpt30ZJetsToNuNu {b} Bin {r} DMdata" 
                             ).format( b = binn, r = region, v = variable + '{}'.format('' if not variable else '_shape_') )

                histos[binn][variable][region] = root_file.Get(branch + "/" + histogram)
                if not histos[binn][variable][region]:
                    print("Error, histogram doesn't exist:\n    branch: {}\n    histogram: {}").format(branch, histogram)
                histos[binn][variable][region].SetDirectory(0)                

    #fixing LowDm and LowDMHighMET separation
    for variable in variables:

        branch    =       "nValidationBinLowDMHighMET_jetpt30"
        histogram = (     "ZNuNu_nValidationBin_LowDM_HighMET_{}"
			  "jetpt30nValidationBinLowDMHighMET_"
                          "jetpt30nValidationBinLowDMHighMET_"
                          "jetpt30ZJetsToNuNu Validation Bin Low DM High METdata"
                    ).format('' if not variable else "_".join([variable,'shape_']) ) 

        lowHighMet = root_file.Get(branch + "/" + histogram)

        if not lowHighMet:
            print("Error, histogram doesn't exist: branch: {} \nhistogram: {}").format(branch, histogram)
        
        temp = LowDMMergerValidationBins(histos['Validation'][variable]['Low'], lowHighMet)

        histos['Validation'][variable]['Low'] = temp.Clone()
        histos['Validation'][variable]['Low'].SetDirectory(0)

    root_file.Close()

    print("Loading histograms has been successful")

    # histos[binn][variable][region]
    return histos

#####################################################################################################################################
   
def ForShapeNorm(location):
    """Load variable distributions in order to calculate shape and normalization factor"""

    root_file = ROOT.TFile.Open(location)

    branches   =  ['nJets_drLeptonCleaned_jetpt30', 'HT_drLeptonCleaned_jetpt30', 'metWithLL']
    variables  =  ['nj','ht','met']
    regions    =  ['HighDM', 'LowDM']
    particles  =  ['Electron','Muon']
    metcuts    =  ['', 'Loose']
    mcdata     =  ['Datadata','DYstack','Single tstack','t#bar{t}stack','Rarestack']
    mcdnew     =  ['Data','DY','Sint','TTbar','Rare']

    # histos[variable][region][particle][metcut][mcdata]
    histos = {v: { r: { p: { m: dict.fromkeys(mcdata) for m in metcuts } for p in particles} for r in regions } for v in variables }


    for variable, branch in zip(variables, branches):
        for region in regions:
            for particle in particles:
                for metcut in metcuts:
                    for mcd, mcdn in zip(mcdata, mcdnew):

                        # print("We are now in: {} {} {} {} {}").format(variable, region, particle, metcut, mcdn )

                        histogram  = ( "DataMC_{p}_{r}_{met}{v}_jetpt30{b}{b}{md}"
                                     ).format( p    =  particle,
                                               r    =  region, 
                                               v    =  variable, 
                                               b    =  branch, 
                                               md   =  mcd,
                                               met  =  "".format( '' if not metcut else (metcut + '_') )
                                     )

                        histos[variable][region][particle][metcut][mcdn] = root_file.Get(branch + "/" + histogram)

                        if not histos[variable][region][particle][metcut][mcdn]:
                            print("Error, histogram doesn't exist: branch: {} \nhistogram: {}").format(branch, histogram)

                        histos[variable][region][particle][metcut][mcdn].SetDirectory(0)                

    root_file.Close()

    print("Loading histograms has been successful")

    # histos[variable][region][particle][metcut][mcdata]
    return histos

#####################################################################################################################################
   
def MCSyst(location):
    """Load validation bins with different systematic uncertainties applied"""

    root_file = ROOT.TFile.Open(location)

    regions      =  ['High', 'Low']
    systematics  =  ['', 'pdf', 'metres', 'jes', 'btag', 'eff_restoptag', 'eff_sb', 'eff_toptag', 'eff_wtag', 'met_trig', 'pileup']
    directions   =  ['down', 'up']
    binns        =  ['Validation'] # need to add "Search"

    # histos[binn][syst][direction][region]
    histos = {b: {s: {d: dict.fromkeys(regions) for d in directions } for s in systematics } for b in binns}
    for binn in binns:
        for syst in systematics:
            for direction in directions:
                for region in regions:
    
                    #print("\nWe are now in: {} {} {} {}\n".format(binn, syst, direction, region))
    
                    branch     =   "n{b}Bin{r}DM_jetpt30".format( b = binn, r = region)
                    histogram  = ( "ZNuNu_n{b}Bin_{r}DM_{s}"
                                   "jetpt30n{b}Bin{r}DM"
                                   "_jetpt30n{b}Bin{r}DM"
                                   "_jetpt30ZJetsToNuNu {b} Bin {r} DMdata" 
                                 ).format( b = binn, r = region, s = '{}'.format('' if not syst else (syst + '_syst_' + direction + '_')) )
    
                    histos[binn][syst][direction][region] = root_file.Get(branch + "/" + histogram)
                    if not histos[binn][syst][direction][region]:
                        print("Error, histogram doesn't exist:\n     branch: {}\n    histogram: {}").format(branch, histogram)
                    histos[binn][syst][direction][region].SetDirectory(0)                
    
        #fixing LowDm and LowDMHighMET separation
        for syst in systematics:
    
            branch    =    "nValidationBinLowDMHighMET_jetpt30"
            histogram = (  "ZNuNu_nValidationBin_LowDM_HighMET_{}"
    			   "jetpt30nValidationBinLowDMHighMET_"
                           "jetpt30nValidationBinLowDMHighMET_"
                           "jetpt30ZJetsToNuNu Validation Bin Low DM High METdata"
                        ).format('' if not syst 
                                    else   (syst + '_syst_' + direction + '_') 
                                ) 
    
            lowHighMet = root_file.Get(branch + "/" + histogram)
    
            if not lowHighMet:
                print("Error, histogram doesn't exist:\n    branch: {} \n    histogram: {}").format(branch, histogram)
            
            temp = LowDMMergerValidationBins(histos['Validation'][syst][direction]['Low'], lowHighMet)
    
            histos['Validation'][syst][direction]['Low'] = temp.Clone()
            histos['Validation'][syst][direction]['Low'].SetDirectory(0)
    
        root_file.Close()
    
        print("Loading histograms has been successful")

    # histos[binn][syst][direction][region]
    return histos

#####################################################################################################################################
if __name__ == '__main__':
    print( "Modules information:\n\n"
           "LoadBinHito: {}\n"
           "ForShapeNorm: {}\n"
           "MCSyst: {}\n"
         ).format(LoadBinHisto.__doc__, ForShapeNorm.__doc__, MCSyst.__doc__)

