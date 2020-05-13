# Calculate the weighted average 

import ROOT
import math as m

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

def WeightedAverage(a, da, b, db):
    """Returns the weighted average"""
    
    if da == 0:
        return b, db
    elif db == 0:
        return a, da
    else:

        wa  =  (1/da)**2
        wb  =  (1/db)**2
    
        c   =  (a * wa + b * wb)/(wa + wb)
        dc  =  1/m.sqrt(wa + wb)

        return c, dc
            
