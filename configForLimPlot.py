import ROOT as r

colours = {"Displaced vertices":r.kMagenta+1,"Delayed jets":r.kRed,"MS Clusters":r.kSpring+9,"Displaced jets":r.kOrange-5,"Trackless jets":r.kBlue}
inputFiles = {"Displaced vertices":"displacedVertices/EXO-19-013_all_limits_2024_01_31.root","Delayed jets":"delayedJets/zPrimeReweight_1D.root","MS Clusters":"MSClusters/limits_zPrime.root","Trackless jets":"DarkSector_EXO_21_014_v3/zPrime/Exclusion_zPrime.root","Displaced jets": "displacedJets/ZPMerged.root"}
inputGraphs = {"Displaced vertices":"ZprimetoLLPto{2}_M{0}_{1}","Delayed jets":"quant-1.0/zPrime_{0}_{2}_{1}_graph","MS Clusters":"h_zPrime_mZ_{0}_mX_{1}_{2}_obs","Trackless jets":"zPrimeTo{2}_vs_ctau_mZ_{0}_mX_{1}","Displaced jets": "ZP{2}_M{0}_MX{1}_observed"}
analysisNames = {"Displaced vertices":"Displaced vertices","Delayed jets":"Delayed jets","MS Clusters": "MS Clusters","Displaced jets":"Displaced jets","Trackless jets":"Trackless and OOT jets"}
styles = {1:2,5:1,4:1}
arXiv = {"Displaced vertices":"Phys. Rev. D 104, (2021) 052011","Delayed jets":"Phys. Lett. B 797 (2019) 134876","MS Clusters": "arXiv 2402.01898","Displaced jets":"Phys. Rev. D 104, (2021) 012015","Trackless jets":"JHEP 07 (2023) 210"}

left,right,top,bottom=0.15,0.28,0.08,0.15
font=42
legtxt=0.03
latex1 = r.TLatex()# for analysis title
latex1.SetNDC(1)
latex1.SetTextSize(legtxt+0.005);
latex1.SetTextAlign(11);#xy specifies left,center
latex1.SetTextFont(font);#same as leg
latex2 = r.TLatex() # for analysis arxiv
latex2.SetNDC(1)
latex2.SetTextSize(0.025);
latex2.SetTextAlign(11);#xy specifies left,center
latex2.SetTextFont(font);#same as leg
dx = 0.1#(1-left-right-0.1)#/len(samples) # size of legends in x
x = 1-right +0.01 # x start of legend
dx1 = 0.025
dy_leg   = legtxt*1.3 #size of legend in y
dy_misc = dy_leg*0.6 # misc padding btw leg and decay mode
dy_decay  = dy_leg*1.0 #dy between decay mode and arxiv
dy_arxiv = dy_leg*1.0 #dy between arxiv and title(legend)
y_start = 1-top #-0.1*dy_leg # start of first title in y
