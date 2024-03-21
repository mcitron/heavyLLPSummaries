import ROOT as r
from configForLimPlot import colours,styles,analysisNames

inputFiles = {"Displaced vertices":"displacedVertices/EXO-19-013_all_limits_2024_01_31.root","MS Clusters":"MSClusters/limits_cluster_heavyHiggs.root","Displaced jets":"displacedJets/HeavyHiggs_merged.root","Trackless jets":"DarkSector_EXO_21_014_v3/HeavyHiggs/Exclusion_HeavyHiggs.root"}
inputGraphs = {"Displaced vertices":"HtoLLPto{2}_M{0}_{1}","Delayed jets":"quant-1.0/zPrime_{0}_{2}_{1}_graph","MS Clusters":"h_HeavyHiggsToLLPTo{2}_mH_{0}_mX_{1}_obs","Displaced jets":"H{2}_M{0}_MX{1}_observed","Trackless jets":"HeavyHiggsTo{2}_vs_ctau_mH_{0}_mX_{1}"}
