# merge LowDM and LowDMHighMET bins 

import ROOT

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

def LowDMMergerValidationBins(lowMET, highMET):
    """Merge LowDM with LowDMHighMET in the validation bins"""

    merged = ROOT.TH1F( "nValidationBinLowDM_jetpt30", "nValidationBinLowDM_jetpt30", 19, 0, 19 )
    
    for k in range(1,20):
        if k >= 16: 
            a   =  highMET.GetBinContent(k-15)
            da  =  highMET.GetBinError(k-15) 
        else:
            a   =  lowMET.GetBinContent(k)
            da  =  lowMET.GetBinError(k) 
    
        merged.SetBinContent( k, a ) 
        merged.SetBinError( k, da )
    
    #print('LowDM High MET merge successful')
 
    return merged

