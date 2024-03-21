import ROOT as r
from configForLimPlot import *
import math,os
r.gROOT.SetBatch()
r.gStyle.SetOptStat(0)
import pickle as pkl
def drawCMS(x,y,dx=0.1,size=0.06):
    latex = r.TLatex()
    latex.SetNDC(1)
    latex.SetTextSize(size);
    latex.SetTextAlign(12);
    latex.SetTextFont(62);#bold
    latex.DrawLatex(x,y,"CMS")
    #
    # latex = r.TLatex()
    # latex.SetNDC(1)
    # latex.SetTextSize(size);
    # latex.SetTextAlign(12);
    # latex.SetTextFont(52);#italic
    # latex.DrawLatex(x+dx,y-0.005,"Preliminary")

    return

def setStyle():
    r.gROOT.SetBatch(r.kTRUE)
    r.gStyle.SetLineStyleString(11,"40 20");
    r.gStyle.SetOptStat(0)
    r.gStyle.SetOptFit(0)
    r.gStyle.SetLabelFont(42,"xyz")
    r.gStyle.SetLabelSize(0.05,"xyz")
    r.gStyle.SetTitleFont(42,"xyz")
    r.gStyle.SetTitleFont(42,"t")
    r.gStyle.SetTitleSize(0.05,"xyz")
    r.gStyle.SetTitleSize(0.05,"t")

    r.gStyle.SetPadBottomMargin(0.14)
    r.gStyle.SetPadLeftMargin(0.14)

    r.gStyle.SetPadGridX(0)
    r.gStyle.SetPadGridY(0)
    r.gStyle.SetPadTickX(1)
    r.gStyle.SetPadTickY(1)

    r.gStyle.SetTitleOffset(1,'y')
    r.gStyle.SetLegendTextSize(0.04)
    r.gStyle.SetGridStyle(3)
    r.gStyle.SetGridColor(14)

    r.gStyle.SetMarkerSize(1.0) #large markers
    r.gStyle.SetHistLineWidth(2) # bold lines
    r.gStyle.SetLineStyleString(2,"[12 12]") # postscript dashes

    return

def main():
    setStyle()
    analyses = ["Displaced vertices","Delayed jets","Trackless jets","Displaced jets","MS Clusters"][:-1]
    massesZ = [3000,3500,4000,4500]
    finalStates = ["4b"]
    outputDir = "zPrimeOutputReweight"
    for finalState in finalStates:
        for massZ in massesZ:
            massesX = [massZ/10,massZ/2-50]
            if not os.path.exists(outputDir):
                os.mkdir(outputDir)
            makePlot(analyses,massZ,massesX,finalState,outputDir)
    analyses = ["Displaced vertices","Trackless jets","Delayed jets","Displaced jets","MS Clusters"][:-1]
    massesZ = [3000,3500,4000,4500]
    finalStates = ["2b2nu"]
    outputDir = "zPrimeOutputReweight"
    for finalState in finalStates:
        for massZ in massesZ:
            massesX = [massZ/10,massZ/2-50]
            if not os.path.exists(outputDir):
                os.mkdir(outputDir)
            makePlot(analyses,massZ,massesX,finalState,outputDir)
def scaleGraph(graph,scaleX,scaleY):
    for i in range(graph.GetN()):
        graph.GetY()[i] *= scaleY
        graph.GetX()[i] *= scaleX

def stripGraph(graph,minX,maxX,minY,maxY):
    removePoints = []
    for i in range(graph.GetN()):
        if graph.GetX()[i] < minX or graph.GetX()[i] > maxX:
            removePoints.append(i)
        if graph.GetY()[i] < minY or graph.GetY()[i] > maxY:
            removePoints.append(i)
    for i in removePoints[::-1]:
        graph.RemovePoint(i)
    # get graphs and legends

def makePlot(analyses,massZ,massesX,finalState,outputDir):
    if "2" in finalState:
        dummyHist = r.TH1D("dummy",";c#tau_{X} [mm];95% CL upper limit on #sigma #it{B} [fb]",100,0.1,100000)
    else:
        dummyHist = r.TH1D("dummy",";c#tau_{X} [mm];95% CL upper limit on #sigma #it{B}^{2} [fb]",100,0.1,100000)
    oC = r.TCanvas("c","",1300,900)

    oC.SetLeftMargin(left)
    oC.SetRightMargin(right)
    oC.SetTopMargin(top)
    oC.SetBottomMargin(bottom)

    # oC.SetBottomMargin(0.15); 
    dummyHist.GetXaxis().SetTitleOffset(1.3);
    # dummyHist.GetXaxis().SetTitleSize(0.04);
    # dummyHist.GetYaxis().SetTitleSize(0.04);
    oC.SetLogx()
    oC.SetLogy()
    dummyHist.Draw()
    dummyHist.SetMaximum(2000)
    dummyHist.SetMinimum(0.002)
    leg = r.TLegend(0.4,0.7,0.89,0.89)
    leg.SetBorderSize(0)
    if "2nu" in finalState:
        legTitle = "Z' #rightarrow XX' #rightarrow "+finalState.replace("2nu"," + Inv")
    else:
        legTitle = "Z' #rightarrow XX #rightarrow "+finalState.replace("2nu"," + Inv")

    legends = []
    y=y_start
    for analysis in analyses:
        iFile = inputFiles[analysis]
        rFile = r.TFile(iFile)
        graphDrawn = False
        for massX in massesX:
            graph=None
            if analysis == "Delayed jets":
                if massX*1./massZ < 0.2: continue
            graph = rFile.Get(inputGraphs[analysis].format(massZ,massX,finalState))
            # if analysis == "Displaced jets" and finalState == "4b":
            #     graph = rFile.Get(inputGraphs[analysis].format(massZ,massX,finalState))
            # else:
            if not(graph): continue
            graphDrawn = True
            graph.SetFillStyle(0)
            graph.SetFillColor(0)
            graph.SetMarkerStyle(2)
            graph.SetLineColor(colours[analysis])
            graph.SetLineStyle(styles[int(math.ceil(10*(massX*1./massZ)))])
            graph.SetLineWidth(2)
            graph.SetMarkerColor(colours[analysis])
            print (finalState,analysis,massX)
            if analysis == "MS Clusters":
                scaleGraph(graph,1000,1000)
            if analysis == "Delayed jets":
                stripGraph(graph,100,1E6,-1,100)
            stripGraph(graph,-1,1E6,-1,100)
            # legText = "{} m_{{Z'}} = {}, m_{{X}} = {}".format(analysisNames[analysis],massZ,massX)
            graph.Draw("sameL")
            # leg.AddEntry(graph,legText)
        # dummyGraph = r.TGraph()
        # dummyGraph.SetLineColor(colours[analysis])
        if graphDrawn:
            leg = r.TLegend(x,y-dy_leg,x+dx,y)
            leg.SetBorderSize(0)
            leg.SetTextSize(legtxt+0.005)
            leg.AddEntry(graph,analysisNames[analysis],"l")
            leg.Draw()
            legends.append(leg)
            y-=dy_leg # update y
            y-=dy_misc
            # y-=dy_decay
            latex2.DrawLatex(x+dx1,y,arXiv[analysis])
            y-=dy_arxiv
    xsDict = pkl.load(open("zPrime_xs.pkl","r"))
    xsValue = xsDict[float(massZ)][0]
    # latexXs = r.TLatex()
    # latexXs.SetTextSize(0.025)
    # latexXs.DrawLatex(dummyHist.GetXaxis().GetXmax()*0.08,xsValue*1.2,"Z'_{SSM} cross section")
    xs = r.TLine(dummyHist.GetXaxis().GetXmin(),xsValue,dummyHist.GetXaxis().GetXmax(),xsValue)
    xs.SetLineStyle(3)
    xs.Draw("same")

    leg = r.TLegend(x,y-dy_leg,x+dx,y)
    leg.SetBorderSize(0)
    leg.SetTextSize(legtxt+0.005)
    leg.AddEntry(xs,"Z'_{SSM} cross section","l")

    leg.Draw()

    y = y_start-0.03
    xMassLeg = x-0.4 
    import array
    dummyGraphs = []
    for massX in massesX[::-1]:
        dummyGraph = r.TGraph(2,array.array("d",[0,1]),array.array("d",[0,1]))
        dummyGraph.SetLineColor(r.kBlack)
        dummyGraph.SetLineStyle(styles[int(math.ceil(10*(massX*1./massZ)))])
        # dummyGraph.SetLineStyle(styles[int(math.ceil(10*(massX*1./massZ)))])
        legMass = r.TLegend(xMassLeg,y-dy_leg*1.1,xMassLeg+dx,y)
        legMass.SetBorderSize(0)
        legMass.SetTextSize(legtxt+0.005)
        legMass.AddEntry(dummyGraph,"m_{{Z'}} = {} GeV, m_{{X}} = {} GeV".format(massZ,massX),"l")
        y -= dy_leg*1.25
        legMass.Draw()
        legends.append(legMass)
        dummyGraphs.append(dummyGraph)

    latex = r.TLatex()
    latex.SetNDC(1)
    latex.DrawLatex(dummyHist.GetXaxis().GetXmin()*(2),dummyHist.GetMaximum()*0.3,legTitle)
    xCMS,yCMS=left+0.04,1-top-0.05
    drawCMS(xCMS,yCMS)
    # latex.DrawLatex(dummyHist.GetXaxis().GetXmax()*(0.0015),dummyHist.GetMaximum()*1.15,"CMS")
    # latex.DrawLatex(600,5,"#bf{m_{Z'} = 4 TeV}")
    # latex.DrawLatex(600,3,"#bf{m_{X'} = 1.95 TeV}")
    latex.DrawLatex(1-right-0.31,1-top+0.02,"#bf{132 - 140 fb^{-1} (13 TeV)}")
    latex.SetTextSize(0.04)
    oC.SaveAs(outputDir+"/zPrimeSummary_{}_{}.pdf".format(massZ,finalState))
if __name__=="__main__":
    main()
