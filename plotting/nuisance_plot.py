import ROOT
import root_cosmetics
import sys
import pandas as pd


"""
Create nuisance pull plot from .csv file.
"""

file_name = sys.argv[1]
# read .csv file as pandas dataframe
df = pd.read_csv(file_name)
df = df.iloc[::-1].reset_index()

style = root_cosmetics.get_cms_style()
style.cd()

g_postfit_b = ROOT.TGraphAsymmErrors() # post-fit NP of background only fit
g_postfit_b.SetLineColor(ROOT.kBlack)
g_postfit_b.SetMarkerStyle(20)
g_postfit_b.SetMarkerColor(ROOT.kBlack)
g_postfit_s = ROOT.TGraphAsymmErrors() # post-fit NP of signal+background fit
g_postfit_s.SetLineColor(ROOT.kGray+1)
g_postfit_s.SetMarkerStyle(20)
g_postfit_s.SetMarkerColor(ROOT.kGray+1)
h = ROOT.TH1F("h","axis",df.shape[0],0,df.shape[0]) # use histogram to draw NP names on y-axis
h.SetFillStyle(0)
h.SetFillColor(0)

# fill graphs
for i, row in df.iterrows():
    g_postfit_b.SetPoint(i,row["postfit_b"],i+0.35)
    g_postfit_b.SetPointError(i,row["postfit_b_up"],row["postfit_b_down"],0,0)
    g_postfit_s.SetPoint(i,row["postfit_s"],i+0.65)
    g_postfit_s.SetPointError(i,row["postfit_s_up"],row["postfit_s_down"],0,0)
    h.GetXaxis().SetBinLabel(i+1,df["label"][i])
    h.SetBinContent(i, -20) # set bin content to some negative value to hide histogram

# create legend
leg = ROOT.TLegend(0.3,0.95,0.9,0.99)
leg.SetNColumns(2)
leg.SetBorderSize(0)
leg.SetFillStyle(0)
leg.SetTextSize(0.025)
leg.SetTextFont(42)
leg.AddEntry(g_postfit_b, "background only fit","pl")
leg.AddEntry(g_postfit_s, "signal+background fit","pl")

c = ROOT.TCanvas("nuisance_canvas","nuisance_canvas",600,800)
pad = ROOT.TPad("pad","pad",0.01,0.01,0.99,0.99)
pad.SetTopMargin(0.05)
pad.SetBottomMargin(0.075)
pad.SetLeftMargin(0.25)
pad.SetRightMargin(0.05)
pad.Draw()
pad.cd()
# Draw 1 and 2 sigma bands as boxes
box_68 = ROOT.TBox(-1,0,1,df.shape[0])
box_68.SetFillStyle(1001)
box_68.SetFillColor(ROOT.kGreen+1)
box_95 = ROOT.TBox(-2,0,2,df.shape[0])
box_95.SetFillStyle(1001)
box_95.SetFillColor(ROOT.kOrange)

h.Draw("hbar") # draw horizontal histogram to get the axis right
h.GetYaxis().SetTitle("nuisance parameter pull")
h.GetXaxis().SetLabelSize(0.033)
h.GetYaxis().SetLabelSize(0.033)
h.GetYaxis().SetTitleSize(0.04)
h.GetYaxis().SetTitleOffset(0.9)
h.GetYaxis().CenterTitle(True)
h.GetYaxis().SetRangeUser(-2.49,2.49)
box_95.Draw()
box_68.Draw()
g_postfit_s.Draw("PSAME")
g_postfit_b.Draw("PSAME")
leg.Draw()
ROOT.gPad.RedrawAxis()

plot_name = file_name.replace('.csv','')
c.Print(str(plot_name+'.pdf'))
