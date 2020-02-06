//----------------------------------------------------------------------------------------
//  Search units parser
//----------------------------------------------------------------------------------------

#include <iostream>
#include <string>
#include <fstream>
#include "../../../json/single_include/nlohmann/json.hpp"
using json = nlohmann::json;

int main() {

    //initializing
    int  nMergedTops, nResolvedTops, nWs, nBottoms, nSoftBottoms, nJets;
    float ht, met, ptb, mtb, ISRJetPt;

    std::string nMergedTops_str, nResolvedTops_str, nWs_str, nBottoms_str, nSoftBottoms_str, nJets_str; 
    std::string ht_str, met_str, mtb_str, ISTJetPt; 


    //enter integers
    std::cout << "Enter nMergedTops, nResolvedTops, nWs, nBottoms, nSoftBottoms, nJets (in that order):" << std::endl;
    std::cin >> nMergedTops >> nResolvedTops >> nWs >> nBottoms >> nSoftBottoms >> nJets;

    //enter floats
    std::cout << "Enter ht, met, ptb, mtb, ISRJetPt (in that order):" << std::endl;
    std::cin >> ht >> met >> ptb >> mtb >> ISRJetPt; 

    //----------------------------------------------------------------------------------------
    //  Search units parser
    //----------------------------------------------------------------------------------------

    // Soft Bottoms
    if ( nSoftBottoms == 0 ) { nSoftBottoms_str = "nivf0"; }
    if ( nSoftBottoms >= 1 ) { nSoftBottoms_str = "nivf1"; }
        
    // nJets
    if ( nJets >= 2 && nJets <= 5 ){ nJets_str = "nj2to5"; }
    if ( nJets >= 6 ) { nJets_str = "nj6"; }
    if ( nJets >= 7 && nBottoms >= 1 ){ nJets_str = "nj7"; }

    // nBottoms
    if ( nBottoms == 0 ) { nBottoms_str = "nb0"; }
    if ( nBottoms == 1 ) { nBottoms_str = "nb1"; }
    if ( nBottoms >= 2 && mtb <  175 ) { nBottoms_str = "nb2"; }
    if ( nBottoms >= 3 && mtb >= 175 ) { nBottoms_str = "nb3"; }
    if ( nBottoms == 2 && mtb >= 175 ) { nBottoms_str = "nbeq2"; }
    
    //Ws
    if ( nWs == 0 ) { nWs_str = "nw0"; }
    if ( nWs == 1 && nBottoms != 1 ) { nWs_str = "nw1"; }
    if ( nWs == 2 && nBottoms != 1 ) { nWs_str = "nw2"; }
    if ( nWs >= 1 && nBottoms == 1 ) { nWs_str = "nwgeq1"; }

    //nResolvedTops
    if ( nResolvedTops == 0 ) { nResolvedTops_str = "nrt0"; }
    if ( nResolvedTops == 1 ) { nResolvedTops_str = "nrt1"; }   
    if ( nResolvedTops == 2 ) { nResolvedTops_str = "nrt2"; }   
    if ( nResolvedTops >= 1 && ( nBottoms_str == "nb1" || nBottoms_str == "nb2" ) ) { nResolvedTops_str = "nrtgeq1"; }

    //nMergedTops
    if ( nMergedTops == 0) { nMergedTops_str = "nt0"; }
    if ( nMergedTops == 1) { nMergedTops_str = "nt1"; } 
    if ( nMergedTops == 2) { nMergedTops_str = "nt2"; } 
    if ( nMergedTops >= 1 && ( nBottoms_str == "nb1" || nBottoms_str == "nb2" ) ) { nMergedTops_str = "ntgeq1"; }

    //ht
    if ( ht >= 1500 ) { ht_str = "htgt1500"; }
    if ( ht <  1000 ) { ht_str = "htlt1500"; }
    if ( ht >= 1000 && ht < 1300) { ht_str = "ht1000to1300"; }  
    if ( ht >= 1300 && ht < 1500) { ht_str = "ht1300to1500"; } 
    if ( ht >= 1000 && ht < 1500 && nBottoms_str == "nb3") { ht_str = "ht1000to1500"; }  

    //met
    if ( met >= 250 && met < 300 ) { met_str = "MET_pt250to300"; }  //conflict!! 250to350, 300to400,  

    if ( met >= 250 && met < 350 ) { met_str = "MET_pt250to350"; }  //conflict!! 250to300, 300to400, 
    if ( met >= 350 && met < 450 ) { met_str = "MET_pt350to450"; }  //conflict!! 300to400, 400to500
    if ( met >= 450 && met < 550 ) { met_str = "MET_pt450to550"; }  //conflict!! 400to500, 500to600, 500toinf,
    if ( met >= 550 && met < 650 ) { met_str = "MET_pt550to650"; }  //conflict!! 500to600, 650to750, 500toinf, 600toinf, 650toinf 

    if ( met >= 300 && met < 400 ) { met_str = "MET_pt300to400"; }  //conflict!! 250to300, 250to350, 350to450
    if ( met >= 400 && met < 500 ) { met_str = "MET_pt400to500"; }  //conflict!! 350to450, 450to550, 500toinf 
    if ( met >= 500 && met < 600 ) { met_str = "MET_pt500to600"; }  //conflict!! 450to550, 550to650, 500toinf, 550toinf 
    if ( met >= 650 && met < 750 ) { met_str = "MET_pt650to750"; }

    if ( met >= 500 ) { met_str = "MET_pt500toinf"; }
    if ( met >= 550 ) { met_str = "MET_pt550toinf"; }
    if ( met >= 600 ) { met_str = "MET_pt600toinf"; }
    if ( met >= 650 ) { met_str = "MET_pt650toinf"; }
    if ( met >= 750 ) { met_str = "MET_pt750toinf"; }

    std::vector<std::string> cuts = {nBottoms_str, nMergedTops_str, nResolvedTops_str, nWs_str, ht_str}; // version 1, hm  
                                                                     // nb3 version
                                                                    // lm  version
                                                             // nrtntnwgeq3 version
                                                             
    std::cout << "cuts " << cuts[0] << " " << cuts[1] << " " << cuts[2] << " " << cuts[3] << " " << cuts[4] << std::endl;


    //###########################################################################################

    // Looping in json file
    const std::string fileName = "dc_BkgPred_BinMaps_master.json";
    json json_;
    std::ifstream i(fileName);
    i >> json_;
    for (const auto& element : json_["unitSRNum"].items()){
        int k;

        for (k = 0; k < 5 ; k++){
            if (element.key().find(cuts[k]) == std::string::npos)
                break;                                   
        }

        if (k==5){
            int bin = std::stoi(std::string(element.value()));
            std::cout << " " <<  element.key()  << "-------" << bin  << std::endl;
        }
    }

    return 0;
}
