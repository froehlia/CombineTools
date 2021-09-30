import ROOT
def SetupPad(): # -> TPad
    """
    Create a default TPad for drawing plots

    coordinates:
       |             |
    y3 +-------------+
       |     pad1    |
    y2 |-------------|
       |     rp1     |
    y1 +-------------+
       x1            x2

    """
    yplot = 0.65
    yratio = 0.34
    y3 = 0.99
    y2 = y3-yplot
    y1 = y2-yratio
    x1 = 0.01
    x2 = 0.99

    m_pad = ROOT.TPad("pad", "plot pad", x1, y1, x2, y3)

    m_pad.SetTopMargin(0.05);
    m_pad.SetBottomMargin(0.12);
    m_pad.SetLeftMargin(0.14);
    m_pad.SetRightMargin(0.05);

    return m_pad

def draw_texts(pad, config):
    """
    draw info text on a given pad.
    """
    upper_text = config.get('cms_text_upper','CMS')
    lower_text = config.get('cms_text_lower','Preliminary')
    run_parameters = config.get('cms_text_run_parameters','137 fb^{-1} (13 TeV)')
    align = config.get('cms_text_align','left')
    # settings
    x = 0
    y = 0
    textalign = 0

    if (align == "left"):
        x = pad.GetLeftMargin() + 0.04
        y = 1 - 1.75 * pad.GetTopMargin()
        textalign = 13
    if (align == "right"):
        x = 1.-pad.GetRightMargin() - 0.04
        y = 1 - 1.75 * pad.GetTopMargin()
        textalign = 33
    h = pad.GetHNDC()
    # create and draw texts
    cms_text = ROOT.TLatex(3.5, 24, upper_text)
    cms_text.SetNDC()
    cms_text.SetTextAlign(textalign)
    cms_text.SetX(x)
    cms_text.SetY(y)
    cms_text.SetTextFont(62)
    cms_text.SetTextSize(0.05/h)
    cms_text.Draw()
    ROOT.SetOwnership(cms_text, 0)
    prelim_text = ROOT.TLatex(3.5, 24, lower_text)
    prelim_text.SetNDC()
    prelim_text.SetTextAlign(textalign)
    prelim_text.SetX(x)
    prelim_text.SetY(y-cms_text.GetTextSize()*1.1)
    prelim_text.SetTextFont(52)
    prelim_text.SetTextSize(0.76 * cms_text.GetTextSize())
    prelim_text.Draw()
    ROOT.SetOwnership(prelim_text, 0)
    info_text = ROOT.TLatex(3.5, 24, run_parameters)
    info_text.SetNDC()
    info_text.SetTextAlign(33)
    info_text.SetX(1.-pad.GetRightMargin())
    info_text.SetY(1.)
    info_text.SetTextFont(42)
    info_text.SetTextSize(0.04/h)
    info_text.Draw()
    ROOT.SetOwnership(info_text, 0)

def get_cms_style(): # -> TStyle
    """
    Get plot style used in CMS
    uses style guidline defined in
    https://twiki.cern.ch/twiki/bin/viewauth/CMS/Internal/FigGuidelines
    especially definitions from
    https://twiki.cern.ch/twiki/pub/CMS/Internal/FigGuidelines/tdrstyle.C
    """
    # settings
    top_margin = 0.07
    bottom_margin = 0.12
    left_margin = 0.13
    right_margin = 0.06
    width = 600
    height = 600

    cmsstyle = ROOT.TStyle('CMS_Style', 'Style for CMS publishing')
    # canvas
    cmsstyle.SetCanvasBorderMode(0)
    cmsstyle.SetCanvasColor(0)
    cmsstyle.SetCanvasDefH(height)
    cmsstyle.SetCanvasDefW(width)
    cmsstyle.SetCanvasDefX(0)
    cmsstyle.SetCanvasDefY(0)
    # pad
    cmsstyle.SetPadBorderMode(0)
    cmsstyle.SetPadColor(0)
    cmsstyle.SetPadGridX(False)
    cmsstyle.SetPadGridY(False)
    cmsstyle.SetGridColor(0)
    cmsstyle.SetGridStyle(3)
    cmsstyle.SetGridWidth(1)
    # frame
    cmsstyle.SetFrameBorderMode(0)
    cmsstyle.SetFrameBorderSize(1)
    cmsstyle.SetFrameFillColor(0)
    cmsstyle.SetFrameFillStyle(0)
    cmsstyle.SetFrameLineColor(1)
    cmsstyle.SetFrameLineStyle(1)
    cmsstyle.SetFrameLineWidth(1)
    # stat box
    cmsstyle.SetOptFile(0)
    cmsstyle.SetOptStat(0)
    # margins
    cmsstyle.SetPadTopMargin(top_margin)
    cmsstyle.SetPadBottomMargin(bottom_margin)
    cmsstyle.SetPadLeftMargin(left_margin)
    cmsstyle.SetPadRightMargin(right_margin)
    # global title
    cmsstyle.SetOptTitle(0)
    cmsstyle.SetTitleFont(42)
    cmsstyle.SetTitleColor(1)
    cmsstyle.SetTitleTextColor(1)
    cmsstyle.SetTitleFillColor(10)
    cmsstyle.SetTitleFontSize(0.05)
    # axis
    cmsstyle.SetAxisColor(1, "XYZ")
    cmsstyle.SetStripDecimals(True)
    cmsstyle.SetTickLength(0.03, "XYZ")
    cmsstyle.SetNdivisions(510, "XYZ")
    cmsstyle.SetPadTickX(1)
    cmsstyle.SetPadTickY(1)
    # axis title
    cmsstyle.SetTitleColor(1, "XYZ")
    cmsstyle.SetTitleFont(42, "XYZ") # Set relative font size
    cmsstyle.SetTitleSize(0.05, "XYZ")
    cmsstyle.SetTitleXOffset(1.1)
    cmsstyle.SetTitleYOffset(1.1)
    # axis labels
    cmsstyle.SetLabelColor(1, "XYZ")
    cmsstyle.SetLabelFont(42, "XYZ") # Set relative font size
    cmsstyle.SetLabelOffset(0.007, "XYZ")
    cmsstyle.SetLabelSize(0.04, "XYZ")
    # postscript
    cmsstyle.SetPaperSize(20.,20.)
    cmsstyle.SetHatchesLineWidth(5)
    cmsstyle.SetHatchesSpacing(0.05)

    return cmsstyle
