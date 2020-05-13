#!/bin/bash

echo 'Doing all calculations'

python ShapeNormGen.py ../condor/2016_1apr2020/result.root 2016
python Prediction.py ../condor/2016_1apr2020/result.root 2016
python ShapeSyst.py ../condor/2016_1apr2020/result.root 2016
python MCSyst.py ../condor/2016_1apr2020/result.root 2016
mkdir outputs/2016
mv outputs/*.png outputs/2016
mv outputs/*.txt outputs/2016

python ShapeNormGen.py ../condor/2017_1apr2020/result.root 2017
python Prediction.py ../condor/2017_1apr2020/result.root 2017
python ShapeSyst.py ../condor/2017_1apr2020/result.root 2017
python MCSyst.py ../condor/2017_1apr2020/result.root 2017
mkdir outputs/2017
mv outputs/*.png outputs/2017
mv outputs/*.txt outputs/2017

python ShapeNormGen.py ../condor/2018_1apr2020/result.root 2018
python Prediction.py ../condor/2018_1apr2020/result.root 2018
python ShapeSyst.py ../condor/2018_1apr2020/result.root 2018
python MCSyst.py ../condor/2018_1apr2020/result.root 2018
mkdir outputs/2018
mv outputs/*.png outputs/2018
mv outputs/*.txt outputs/2018

rm outputs/*.root

python Run2Prediction.py ../condor/2016_1apr2020/result.root ../condor/2017_1apr2020/result.root ../condor/2018_1apr2020/result.root
python Comparison.py /uscms/homes/c/caleb/archive/zinv_results/2020-04-09/prediction_histos/
