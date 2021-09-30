import ROOT
import root_cosmetics as cosmetics
import csv
import yaml
import sys

def find_intersection(g1, g2): # -> float # can put this somewhere else?
    """
    find intersection of two TGraphs, assuming only one intersection.
    returns x value of intersection
    """
    precision = 0.01
    max_calls = 10000
    x1 = g1.GetHistogram().GetXaxis().GetXmin()
    x2 = g1.GetHistogram().GetXaxis().GetXmax()
    calls = 0
    while ((abs(x1-x2) > precision) and (calls < max_calls)):
        # find intersection using Newton bisection method
        y1 = g1.Eval(x1) - g2.Eval(x1)
        y2 = g1.Eval((x1+x2)/2) - g2.Eval((x1+x2)/2)
        if (y1*y2 < 0): x2 = (x1+x2)/2
        else: x1 = (x1+x2)/2
        calls += 1

    if (calls >= max_calls):
      print 'WARNING: find_interseciont() terminated because max calls was reached.'

    return (x1+x2)/2


def get_graph(file_name): # -> TGraph
    """
    create TGraph from .csv file.
    returns TGraph
    """
    g = ROOT.TGraph()
    with open(file_name) as csvfile:
        i = 0
        reader = csv.DictReader(csvfile)
        for row in reader:
            g.SetPoint(i,float(row['mass']),float(row['central']))
            i +=1
    return g


def get_error_graph(file_name): # -> TGraphErrors
    """
    create TGraphErrors from .csv file.
    returns TGraphErrors
    """
    g = ROOT.TGraphErrors()
    with open(file_name) as csvfile:
        i = 0
        reader = csv.DictReader(csvfile)
        for row in reader:
            g.SetPoint(i,float(row['mass']),float(row['central']))
            g.SetPointError(i,0.0,float(row['err']))
            i += 1
    return g

def get_config(config_file): # -> dict # can be moved to utils
    """
    read configuration from file
    """
    with open(config_file, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
            return config
        except yaml.YAMLError as exc:
            print(exc)
            raise Exception("{}: Unable to parse config file!".format(sys.argv[0]))

# --- Settings
# note: this is not very elegant, but I was lazy coding something nicer, sorry ...
config = get_config(sys.argv[1])

limit_file_name = config.get('limit_file_name')                                 # name of the observed and expected limits input file
theory_file_name = config.get('theory_file_name')                               # name of the theory prediction input file
compare_graphs = config.get('compare_graphs',[])                                # additional graphs in the form {'file':'', 'color':0, 'title':''}
b_logy = config.get('b_logy',True)                                              # draw logarithmic y axis
b_theory_err = config.get('b_theory_err',False)                                 # draw theory curve with errors
expected_title = config.get('expected_title','Median expected' )                # name of expected curve in legend
theory_title = config.get('theory_title', 'Theory')
x_axis_title = config.get('x_axis_title','M_{tW} [TeV]')                        # x axis title
y_axis_title = config.get('y_axis_title','#sigma(b*)')                          # y axis title

# --- Create TGraphs
style = cosmetics.get_cms_style()
style.cd()
g_expected = ROOT.TGraph()                  # expected limits
g_observed = ROOT.TGraph()                  # observed limits
g_expected_68 = ROOT.TGraphAsymmErrors()    # 1 sigma band
g_expected_95 = ROOT.TGraphAsymmErrors()    # 2 sigma band
g_theory = ROOT.TGraphErrors()              # theory prediction
g_compares = []                             # list holding expect limits for comparison

# ---  Read data from csv
i = 0
with open(limit_file_name) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        g_expected.SetPoint(i,float(row['mass']),float(row['central']))
        g_observed.SetPoint(i,float(row['mass']),float(row['observed']))
        g_expected_68.SetPoint(i,float(row['mass']),float(row['central']))
        g_expected_68.SetPointError(i,0.,0.,float(row['low_68']),float(row['high_68']))
        g_expected_95.SetPoint(i,float(row['mass']),float(row['central']))
        g_expected_95.SetPointError(i,0.,0.,float(row['low_95']),float(row['high_95']))
        i += 1

# --- Plotting
c = ROOT.TCanvas('limit_canvas','limit_canvas',600,600)
pad = cosmetics.SetupPad() # get default pad
pad.Draw()
pad.cd()
pad.SetLogy(b_logy)
# set cosmetics for TGraphs
# expected
g_expected.SetLineWidth(2)
g_expected.SetLineStyle(7)
g_expected.SetLineColor(ROOT.kBlack)
# 1 sigma
g_expected_68.SetFillStyle(1001)
g_expected_68.SetFillColor(ROOT.kGreen + 1) # recommended color
# 2 sigma
g_expected_95.SetFillStyle(1001)
g_expected_95.SetFillColor(ROOT.kOrange) # recommended color
# observed
g_observed.SetLineWidth(2)
g_observed.SetLineStyle(1)
g_observed.SetLineColor(ROOT.kBlack)
# draw TGraphs
g_expected_95.Draw('A3')
g_expected_68.Draw('SAME3')
g_expected.Draw('SAME')
g_observed.Draw('SAME')
# set y-axis range
xmin = ROOT.Double(0)
xmax = ROOT.Double(0)
ymin = ROOT.Double(0)
ymax = ROOT.Double(0)
g_expected.GetPoint(0, xmin,ymin);
g_expected.GetPoint(i-1, xmax,ymax);
ymax = max(10., g_expected.GetHistogram().GetMaximum()) * 3;
ymin = min(0.001, g_expected.GetHistogram().GetMinimum()) * 0.33;
# add theory curve if given
if (theory_file_name != ''):
    # create theory graph from .csv file
    theory_draw_options = ''
    theory_legend_options = ''
    if (b_theory_err):
        g_theory = get_error_graph(theory_file_name)
        theory_draw_options = 'SAMEL3'
        theory_legend_options = 'fl'
    else:
        g_theory = get_graph(theory_file_name)
        theory_draw_options = 'SAME'
        theory_legend_options = 'l'
    # set cosmetics
    g_theory.SetLineWidth(2)
    g_theory.SetLineStyle(1)
    g_theory.SetLineColor(ROOT.kRed)
    g_theory.SetFillColor(ROOT.kRed-7)
    g_theory.SetFillStyle(3001)
    # draw
    g_theory.Draw(theory_draw_options)
    # create theory graph legend
    pred_leg = ROOT.TLegend(0.55,0.87,0.95,0.92) # this might be a problem ...
    pred_leg.SetBorderSize(0)
    pred_leg.SetFillStyle(0)
    pred_leg.SetTextSize(0.033)
    pred_leg.SetTextFont(42)
    pred_leg.AddEntry(g_theory, theory_title, theory_legend_options)
    pred_leg.Draw()

# create legends for observed and expected limits
obs_leg = ROOT.TLegend(0.55,0.77,0.95,0.87)
obs_leg.SetBorderSize(0)
obs_leg.SetFillStyle(0)
obs_leg.SetTextSize(0.033)
obs_leg.SetTextFont(62)
obs_leg.SetHeader('95% CL upper limits')
obs_leg.SetTextFont(42)
obs_leg.AddEntry(g_observed, 'Observed', 'l')
obs_leg.Draw()
exp_leg_ylow = 0.59 - len(compare_graphs) * 0.06 # calculate lower edge of legend based on number of entries
exp_leg = ROOT.TLegend(0.55,exp_leg_ylow,0.95,0.77)
exp_leg.SetBorderSize(0)
exp_leg.SetFillStyle(0)
exp_leg.SetTextSize(0.033)
# add additional expected limits if given
if len(compare_graphs)> 0:
    exp_leg.SetTextFont(62)
    exp_leg.SetHeader('Median expected')
    exp_leg.SetTextFont(42)
    for j in range(0,len(compare_graphs)):
        g_compare = get_graph(compare_graphs[j]['file'])
        g_compare.SetLineWidth(2)
        g_compare.SetLineStyle(7)
        g_compare.SetLineColor(compare_graphs[j]['color'])
        g_compare.Draw('SAME')
        exp_leg.AddEntry(g_compare, compare_graphs[j]['title'], 'l')
    exp_leg.AddEntry(g_expected, expected_title, 'l')
    exp_leg.AddEntry(g_expected_68, '68% expected', 'f')
    exp_leg.AddEntry(g_expected_95, '95% expected', 'f')
else:
  exp_leg.SetTextFont(42);
  exp_leg.AddEntry(g_expected, expected_title, 'l')
  exp_leg.AddEntry(g_expected_68, '68% expected', 'f')
  exp_leg.AddEntry(g_expected_95, '95% expected', 'f')
exp_leg.Draw();
# setup axes
g_expected_95.GetHistogram().SetXTitle(x_axis_title)
g_expected_95.GetHistogram().SetYTitle(y_axis_title)
g_expected_95.GetHistogram().GetYaxis().SetTitleOffset(1.25)
g_expected_95.GetHistogram().GetXaxis().SetLimits(xmin,xmax)
g_expected_95.GetHistogram().GetYaxis().SetRangeUser(ymin,ymax)

# draw cms logo and run information
cosmetics.draw_texts(pad, config)
# safe as figure
pad.RedrawAxis()
plot_name = limit_file_name.replace('.csv','')
#c.Print(plot_name+'.eps');
#c.Print(plot_name+'.png');
c.Print(str(plot_name+'.pdf'))

# calculated expected and observed mass limits
if (theory_file_name != ''):
    print 'expected: {} TeV'.format(find_intersection(g_expected, g_theory))
    print 'observed: {} TeV'.format(find_intersection(g_observed, g_theory))
