import ROOT
import array
import root_cosmetics as cosmetics
import utils
import sys


config = utils.get_config(sys.argv[1])
# Settings
file_name = config.get('file_name')                         # file name of fit diagnostics output
channel = config.get('channel')                             # channel
xbins = config.get('xbins')                                 # binning of distribution (maybe I can  remove this)
prefix = config.get('shapes','shapes_fit_b/')               # name of shapes
                                                                #   ('shapes_prefit' = prefit)
                                                                #   ('shapes_fit_b'  = background only)
                                                                #   ('shapes_fit_s'  = signal+background)
background_samples = config.get('background_samples',[])    # background samples in the form {'name':'', 'title':'', 'color':0}
signal_sample = config.get('signal_sample',{})                # signal sample in the form {'name':'', 'title':'', ...}
b_logy = config.get('b_logy', False)                        # draw logarithmic y axis?
x_axis_title = config.get('x_axis_title','Mass [TeV]')    # x axis title
y_axis_title = config.get('y_axis_title','Events/TeV')      # y axis title

f = ROOT.TFile(file_name)
nbins = len(xbins) - 1
xbins = array.array('d',xbins) # convert xbins list to array
# get data
h_data = f.Get(prefix + channel + '/data').Clone()
h_data.SetLineColor(1)
h_data.SetMarkerStyle(8)
# get background shapes
h_bkg_list = []
for sample in background_samples:
    h_bkg = f.Get(prefix + channel + '/' + sample['name']).Clone()
    h_bkg.SetTitle(sample['title'])
    h_bkg.SetDirectory(0)
    h_bkg.SetBins(nbins,xbins)
    h_bkg_list.append(h_bkg)
    h_bkg.SetFillColor(sample['color'])
    h_bkg.SetLineWidth(0)
# get total background shape for uncertainty drawing
h_err = f.Get(prefix + channel + '/total_background').Clone()
h_err.SetDirectory(0)
h_err.SetBins(nbins, xbins)
# get signal
h_signal = f.Get("shapes_fit_s/" + channel +'/' + signal_sample['name']).Clone()
h_signal.SetDirectory(0)
h_signal.SetBins(nbins, xbins)
h_signal.Scale(f.Get("shapes_prefit/" + channel + "/BstarToTW2400LH").Integral()/h_signal.Integral())
h_signal.SetLineColor(1)
h_signal.SetLineStyle(2)
h_signal.SetLineWidth(2)

f.Close()
del f

g_ratio = ROOT.TGraphErrors(h_err.GetNbinsX())
g_ratio_err = ROOT.TGraphErrors(h_err.GetNbinsX())

for i in range(1,nbins+1):
    err_tot = h_err.GetBinError(i)
    err_num = h_data.GetErrorY(i-1)
    x = ROOT.Double(0)
    num = ROOT.Double(0) # numerator for ratio plot
    den = h_err.GetBinContent(i) # denominator for ratio plot
    h_data.GetPoint(i-1, x, num)
    x = h_err.GetBinCenter(i)
    w = h_err.GetBinWidth(i) # bin width
    ratio_err_bkg = err_tot / den     # relative error on background
    ratio_err_data = err_num / num    # relative error on data
    g_ratio.SetPoint(i-1, x, num / den)
    g_ratio.SetPointError(i-1, w/2., ratio_err_data * (num/den))
    g_ratio_err.SetPoint(i-1, x,1.)
    g_ratio_err.SetPointError(i-1, w/2., ratio_err_bkg)
    num /= w
    err_num /= w
    h_data.SetPoint(i-1, x, num)
    h_data.SetPointError(i-1, 0, 0, err_num, err_num)

style = cosmetics.get_cms_style()
style.cd()

h_bkg_stack = ROOT.THStack("hs","")
for h_bkg in h_bkg_list:
    h_bkg.Scale(1., 'width')
    h_bkg_stack.Add(h_bkg, 'hist')

h_err.Scale(1., "width")

# drawing
c = ROOT.TCanvas("postfit_canvas","postfit_canvas",600,600)
c.cd()
pad_top = cosmetics.SetupRatioPadTop()
pad_top.Draw()
c.cd()
pad_bot = cosmetics.SetupRatioPad()
pad_bot.Draw()
pad_top.cd()
pad_top.SetLogy(b_logy)

h_bkg_stack.SetMaximum(max(h_bkg_stack.GetMaximum()*3, h_data.GetMaximum())*3)
h_bkg_stack.SetMinimum(1e-1)
h_err.SetFillColor(921)
h_err.SetLineWidth(0)
h_err.SetFillStyle(3005)
h_bkg_stack.Draw()
h_bkg_stack.GetYaxis().SetTitle(y_axis_title);
h_bkg_stack.GetXaxis().SetLabelSize(h_bkg_stack.GetXaxis().GetLabelSize()/0.65) # adapt label size to smaller the pad
h_bkg_stack.GetYaxis().SetLabelSize(h_bkg_stack.GetYaxis().GetLabelSize()/0.65)
h_bkg_stack.GetXaxis().SetTitleSize(h_bkg_stack.GetXaxis().GetTitleSize()/0.65)
h_bkg_stack.GetYaxis().SetTitleSize(h_bkg_stack.GetYaxis().GetTitleSize()/0.65)
h_bkg_stack.GetYaxis().SetTitleOffset(1.)
h_err.Draw("E2SAME")
h_signal.Draw("HIST SAME")
h_data.Draw("PZSAME")

leg_ylow = 0.725-0.075*len(h_bkg_list)
leg = ROOT.TLegend(0.55,leg_ylow,0.95,0.9)
leg.SetBorderSize(0)
leg.SetFillStyle(0)
leg.AddEntry(h_data, "Data", "pl")
for h_bkg in reversed(h_bkg_list):
    leg.AddEntry(h_bkg, h_bkg.GetTitle(), "f")
leg.AddEntry(h_err, "Tot. uncertainty", "f")
leg.AddEntry(h_signal, signal_sample['title'], "l")
leg.Draw()

cosmetics.draw_texts(pad_top,config)

ROOT.gPad.RedrawAxis()

pad_bot.cd()
pad_bot.SetLogy(False)
g_ratio_err.GetXaxis().SetLimits(h_err.GetXaxis().GetXmin(), h_err.GetXaxis().GetXmax())
g_ratio_err.SetFillColor(921)
g_ratio_err.GetYaxis().SetRangeUser(0.35, 1.65)
g_ratio_err.GetYaxis().CenterTitle()
g_ratio_err.GetYaxis().SetTitle("data/bkg")
g_ratio_err.GetXaxis().SetTitle(x_axis_title)
g_ratio_err.GetXaxis().SetLabelSize(g_ratio_err.GetXaxis().GetLabelSize()/0.32) # adapt label size to smaller the pad
g_ratio_err.GetYaxis().SetLabelSize(g_ratio_err.GetYaxis().GetLabelSize()/0.32)
g_ratio_err.GetXaxis().SetTitleSize(g_ratio_err.GetXaxis().GetTitleSize()/0.32)
g_ratio_err.GetYaxis().SetTitleSize(g_ratio_err.GetYaxis().GetTitleSize()/0.32)
g_ratio_err.GetYaxis().SetTitleOffset(.5)
g_ratio_err.GetXaxis().SetNdivisions(505)
g_ratio_err.GetYaxis().SetNdivisions(505)
g_ratio.SetMarkerStyle(8)
g_ratio_err.Draw("A2")
g_ratio.Draw("SAME PZ0")
ROOT.gPad.RedrawAxis()

plot_name = channel
# c.Print(hist_name+".eps")
# c.Print(hist_name+".png")
c.Print(str(plot_name+".pdf"))
