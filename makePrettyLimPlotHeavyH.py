import ROOT as r
from configForLimPlot import *
from configForLimPlotHiggs import *
from makePrettyLimPlot import drawCMS,setStyle
import math,os
r.gROOT.SetBatch()
r.gStyle.SetOptStat(0)
import pickle as pkl
from higgsxs import xsDict


def main():
    setStyle()
    analyses = ["Displaced vertices","MS Clusters","Displaced jets","Trackless jets"]
    massesH = [400,600,800]
    finalStates = ["4b","2b2nu"]
    outputDir = "higgsOutput"
    for finalState in finalStates:
        for massH in massesH:
            massesX = [massH/10,massH/2-50]
            if not os.path.exists(outputDir):
                os.mkdir(outputDir)
            makePlot(analyses,massH,massesX,finalState,outputDir)
    # analyses = ["Displaced vertices","MS Clusters"][1:]
    # massesH = [3000,3500,4000,4500]
    # finalStates = ["2b2nu"]
    # outputDir = "higgsOutputDM"
    # for finalState in finalStates:
    #     for massH in massesH:
    #         massesX = [massH/10,massH/2-50]
    #         if not os.path.exists(outputDir):
    #             os.mkdir(outputDir)
    #         makePlot(analyses,massH,massesX,finalState,outputDir)
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

def makePlot(analyses,massH,massesX,finalState,outputDir):
    if "2" in finalState:
        dummyHist = r.TH1D("dummy",";c#tau_{X} [mm];#sigma #it{B} [fb]",100,0.1,100000)
    else:
        dummyHist = r.TH1D("dummy",";c#tau_{X} [mm];#sigma #it{B}^{2} [fb]",100,0.1,100000)
    oC = r.TCanvas("c","",1300,900)

    oC.SetLeftMargin(left)
    oC.SetRightMargin(right)
    oC.SetTopMargin(top)
    oC.SetBottomMargin(0.15); 
    dummyHist.GetXaxis().SetTitleOffset(1.3);
    dummyHist.SetLineColor(r.kBlack)
    dummyHist.SetLineWidth(0)
    # dummyHist.GetXaxis().SetTitleSize(0.04);
    # dummyHist.GetYaxis().SetTitleSize(0.04);
    oC.SetLogx()
    oC.SetLogy()
    dummyHist.Draw()
    dummyHist.SetMaximum(4000000)
    dummyHist.SetMinimum(0.04)
    leg = r.TLegend(0.35,0.7,0.85,0.89)
    leg.SetBorderSize(0)
    if "2nu" in finalState:
        legTitle = "H #rightarrow XX' #rightarrow "+finalState.replace("2nu"," + Inv")
    else:
        legTitle = "H #rightarrow XX #rightarrow "+finalState.replace("2nu"," + Inv")
    legends = []
    y=y_start
    for analysis in analyses:
        iFile = inputFiles[analysis]
        rFile = r.TFile(iFile)
        graphDrawn = False
        for massX in massesX:
            graph=None
            if analysis == "Delayed jets":
                if massX*1./massH < 0.2: continue
            elif analysis == "Displaced vertices":
                if massX*1./massH < 0.2: continue
            elif analysis == "Trackless jets":
                if massH < 500:
                    if massX*1./massH < 0.2: continue
            # if analysis == "Displaced jets":
            #     if massH == 400 and "2nu" in finalState:
            #         rFileT = r.TFile("displacedJets/H2b2nu_M400.root")
            #         graph = rFileT.Get(inputGraphs[analysis].format(massH,massX,finalState))
            graph = rFile.Get(inputGraphs[analysis].format(massH,massX,finalState))
            print (analysis,graph)
            if not(graph): continue
            graphDrawn = True
            graph.SetFillStyle(0)
            graph.SetFillColor(0)
            graph.SetMarkerStyle(2)
            graph.SetLineColor(colours[analysis])
            graph.SetLineStyle(styles[int(math.ceil(10*(massX*1./massH)))])
            graph.SetMarkerColor(colours[analysis])
            graph.SetLineWidth(2)
            if analysis == "MS Clusters":
                scaleGraph(graph,1000,1000)
            stripGraph(graph,0.2,1E6,-1,2E5)
            legText = "{} m_{{H_{{D}}}} = {}, m_{{X}} = {}".format(analysisNames[analysis],massH,massX)
            graph.Draw("sameL")
        if graphDrawn:
            leg = r.TLegend(x,y-dy_leg,x+dx,y)
            leg.SetBorderSize(0)
            leg.SetTextSize(legtxt+0.005)
            leg.AddEntry(graph,"#bf{"+analysisNames[analysis]+"}","l")
            leg.Draw()
            legends.append(leg)
            y-=dy_leg # update y
            y-=dy_misc
            # y-=dy_decay
            latex2.DrawLatex(x+dx1,y,arXiv[analysis])
            y-=dy_arxiv
    xsValue = xsDict[float(massH)][0]*1000
    xs = r.TLine(dummyHist.GetXaxis().GetXmin(),xsValue,dummyHist.GetXaxis().GetXmax(),xsValue)
    xs.SetLineStyle(3)
    xs.Draw("same")
    leg = r.TLegend(x,y-dy_leg,x+dx,y)
    leg.SetBorderSize(0)
    leg.SetTextSize(legtxt+0.005)
    leg.AddEntry(xs,"H_{D} cross section","l")
    leg.Draw()

    y = y_start-0.03
    xMassLeg = x-0.4 
    import array
    dummyGraphs = []
    for massX in massesX[::-1]:
        dummyGraph = r.TGraph(2,array.array("d",[0,1]),array.array("d",[0,1]))
        dummyGraph.SetLineColor(r.kBlack)
        dummyGraph.SetLineStyle(styles[int(math.ceil(10*(massX*1./massH)))])
        legMass = r.TLegend(xMassLeg,y-dy_leg*1.1+0.05,xMassLeg+dx,y+0.05)
        legMass.SetBorderSize(0)
        legMass.SetTextSize(legtxt+0.005)
        legMass.AddEntry(dummyGraph,"m_{{H_{{D}}}} = {} GeV, m_{{X}} = {} GeV".format(massH,massX),"l")
        y -= dy_leg*1.25
        legMass.Draw()
        legends.append(legMass)
        dummyGraphs.append(dummyGraph)

    # latex = r.TLatex()
    # latex.DrawLatex(dummyHist.GetXaxis().GetXmin()*(2),dummyHist.GetMaximum()*0.3,legTitle)
    # latex.DrawLatex(dummyHist.GetXaxis().GetXmax()*(0.0015),dummyHist.GetMaximum()*1.15,"CMS")
    # latex.DrawLatex(600,5,"#bf{m_{H} = 4 TeV}")
    # latex.DrawLatex(600,3,"#bf{m_{X'} = 1.95 TeV}")
    latex = r.TLatex()
    latex.SetNDC(1)
    latex.DrawLatex(dummyHist.GetXaxis().GetXmin()*(2),dummyHist.GetMaximum()*0.3,legTitle)
    xCMS,yCMS=left+0.04,1-top-0.06
    drawCMS(xCMS,yCMS)
    # latex.SetTextSize(0.04)
    latex.DrawLatex(1-right-0.31,1-top+0.02,"#bf{132 - 140 fb^{-1} (13 TeV)}")
    latexTitle = r.TLatex()
    latexTitle.SetNDC(1)
    latexTitle.SetTextSize(0.035)
    latexTitle.DrawLatex(1-right+0.03,1-top,"#bf{95% CL upper limits}")
    # latexTitle.DrawLatex()
    oC.SaveAs(outputDir+"/higgsSummary_{}_{}.pdf".format(massH,finalState))
if __name__=="__main__":
    main()
