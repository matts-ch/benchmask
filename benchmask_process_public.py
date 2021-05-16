__author__ = "Matthias Schibli"
__license__ = "GPL"
__version__ = "1.0"
__email__ = "matts-ch@gmx.ch"

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import urllib
import urllib.parse
import json
from datetime import datetime
import glob, os

from collections import OrderedDict
from wwo_hist import retrieve_hist_data
import chart_studio
import chart_studio.plotly as py
from plotly.validators.scatter.marker import SymbolValidator


mainplot=1
upload=0

# base folder
folderpath=r'C:\Users\mschi\data_logging'
cwd=os.getcwd()

# this folder will not be included in the analysis
exception='archiv'


# since files/columns are labelled with the product, define it here
# particulate matter sensor produc
pm_sensor='SEN4x'

# serial number of particulate matter sensor
pm_serial='A08CE0662575E320'

# differential sensor product
dp_sensor='SDP3x'
# serial number of differential pressure sensor
dp_serial='168225279115263'

#flow sensor product
flow_sensor='SFM3019'

# flow sensor serial
flow_serial='2038001832'

# direction of flow (mainly used to filter input data: naming convention of folders!)
in_out='ou'

# replace parts of the folder names with more readable names
nameswap={'odlo': 'Odlo Community Mask',
                                        'Cilander':'Cilander Community Mask',
                                        '2layerCotton':'DIY Cotton Community Mask',
                                        'ffp2_shen_huan_':'FFP2/KN95',
                                        'ffp2_shen_huan_taped':'FFP2/KN95 Taped',
                                        'flatmask':'Flat-Fabric Style Mask',
                                        'flatmask_taped':'Flat-Fabric Style Mask Taped',
                                        'Livingguard':'Lvinguard Pro Community Mask (wrong size)',
                                        'Livingguard_taped':'Lvinguard Pro Community Mask (wrong size) Taped',
                                        'Livipro':'Livipro Community Mask',
                                        'Livipro_taped':'Livipro Community Mask Taped',
                                        'nomask':'No Mask',
                                        'one_way_bad_nosepiece_taped':'Surgical Mask, bad Nosepiece Taped',
                                        'one_way_good_nosepiece':'Surgical Mask, good Nosepiece',
                                        'one_way_bad_nosepiece':'Surgical Mask, bad Nosepiece',
                                        'sensiflat':'Flat-Fabric Mask cheap',
                                        'Couture_grey':'Community Mask with integrated Filter',
          'Couture_grey_tape_chin':'Community Mask with integrated Filter',
          'Couture_grey_tape_chin_nose':'Community Mask with Filter, taped Nose',
          'Couture_grey_tape_chin_nose_border':'Community Mask with Filter, taped Nose and Border',
          'Couture_grey_tape_chin_nose_border_match':'Community Mask with Filter, taped Nose and Border Match',
          'Kraftwerk':'Kraftwerk Community Mask'}




# dimensions of the box in meters
box=0.365*0.565*0.33

# volume of head (measured by submerging the head in water -> displacement in m3)
head=0.11**2*np.pi*0.1+0.11**2*np.pi*0.03

# net volume
volume=box-head

# decay rate without mask to adjust for parasitic particle deposition in the rest of the setup (->zero offset correction)
# uncomment print((1.-np.exp(m))) statement
zero_p_rate=0.00051169268990*1.2

# pressure compensation factor. Additional parasitic particle deposition per 1 Pa pressure difference increase
# can be tested with decreased opening (without mask)
# uncomment print((1.-np.exp(m))) statement and divide by pressure, then adjust slightly for best fit
zero_p_1Pa=0.003081958917033223/45*0.64

# theoretical decay rate with a mask with 100% filtration efficiency_pm1 (warning: magic number: 20=volume flow
hundred_p_rate=(20/1000/60)/volume

# target/norm flow rate, dp and efficiency will be normalized to this value
norm_flow_rate= 20

init=0

dplist=[]
mlist=[]
labellist=[]
flowlist=[]
typelist=[]
efficiency_pm1list=[]
efficiency_pm1list0=[]
efficiency_pm1list2=[]


def replacestring(instring,swaplist):
    try:
        return swaplist[instring]
    except:
        return instring

# plotting function to benchmark the fit
def fit_plot(data, label, style):
    nr=data
    x = range(0, len(nr))
    y = np.log(nr)
    m, b = np.polyfit(x, y, 1)

    plt.figure()

    if style=='log':

        plt.plot(x, m * x + b, label='fit')
        plt.plot(x, y, '.', label='measurement')
        plt.ylabel('log(concentration)')
    elif style=='semilog':

        plt.semilogy(x, np.exp(m * x + b), label='fit')
        plt.semilogy(x, np.exp(y), '.', label='measurement')
        plt.ylabel('concentration')
    else:
        plt.plot(x, np.exp(m * x + b), label='fit')
        plt.plot(x, np.exp(y), '.', label='measurement')
        plt.ylabel('concentration')
    plt.xlabel('samples')

    plt.legend()

    #str = str.replace(/ [ ^ -/] / g, '');

    plt.savefig(style+'_fit_' + label + '.png')
    plt.close('all')

    return m


# loop over all raw data folders
for folder in [x[0] for x in os.walk(folderpath)]:

    if init==1:
        # skip exception folders (use for data which shall not be processed)
        if exception in folder:
            pass
        else:

            label=folder[len(folderpath)+1:]

            # naming convenction for selection of in/out direction
            if label[0:2]==in_out:


                os.chdir(folder)
                for file in glob.glob("*.edf"):
                    # select particulate matter data (replace with SPS3x, I used another product named SEN4x
                    if pm_sensor in file:
                        datafile=file
                        typemask=label[str.find(label,'_')+1:-1]

                        # read data from CSV file (maybe adjust skiprows depending on header)
                        data=pd.read_csv(datafile, skiprows=9, sep= '\t')
                        # select corresponding data column, for the different particle sizes
                        nr = data['NumbConc_0p5_'+pm_sensor+'_'+pm_serial]
                        x = range(0,len(nr))
                        y = np.log(nr)
                        # actual data fitting is done in semilog space
                        m0, b = np.polyfit(x, y, 1)

                        nr = data['NumbConc_2p5_'+pm_sensor+'_'+pm_serial]
                        x = range(0,len(nr))
                        y = np.log(nr)
                        m2, b = np.polyfit(x, y, 1)

                        nr = data['NumbConc_1p0_'+pm_sensor+'_'+pm_serial]
                        x = range(0,len(nr))
                        y = np.log(nr)

                        m=fit_plot(nr, label, 'semilog')


                    # read data of differential pressure sensor
                    if dp_sensor in file:
                        datafile=file

                        data=pd.read_csv(datafile, skiprows=9, sep= '\t')

                        dp = data['DP_'+dp_sensor+'_'+dp_serial]
                        if len(dp)>1:
                            dp=abs(np.median(dp))


                    if flow_sensor in file:
                        datafile=file

                        data=pd.read_csv(datafile, skiprows=9, sep= '\t')


                        flow = data['F_'+flow_sensor+'_'+flow_serial]
                        if len(flow)>1:
                            flow=abs(np.median(flow))

                # for setup calibration, use this raw value
                # print((1. - np.exp(m)))


                # compute efficiency, normalized by offset and maximum theoretical efficiency
                efficiency_pm1=100 * ((1 - np.exp(m))-zero_p_rate-zero_p_1Pa*dp) / hundred_p_rate
                efficiency_pm05=100 * ((1 - np.exp(m0))-zero_p_rate-zero_p_1Pa*dp) / hundred_p_rate
                efficiency_pm25=100 * ((1 - np.exp(m2))-zero_p_rate-zero_p_1Pa*dp) / hundred_p_rate

                # normalize with flow rate (try to adjust real flow rate close to norm_flow_rate,
                # the linear normalization is likely to fail for big adjustments
                efficiency_pm1=efficiency_pm1/flow*norm_flow_rate
                efficiency_pm05=efficiency_pm05/flow*norm_flow_rate
                efficiency_pm25=efficiency_pm25/flow*norm_flow_rate

                print(replacestring(typemask, nameswap)+label[-1:],int(efficiency_pm05),
                      int(efficiency_pm1),int(efficiency_pm25) , 0.1*int(dp*10), 0.1*int(10*flow), sep='\t')


                dplist.append(dp/flow*norm_flow_rate)

                labellist.append(label)
                flowlist.append(flow)
                efficiency_pm1list.append( efficiency_pm1 )
                efficiency_pm1list0.append( efficiency_pm05 )
                efficiency_pm1list2.append( efficiency_pm25 )

                typelist.append(typemask)

    init=1

import pylab
NUM_COLORS = len(set(typelist))

cm = pylab.get_cmap('hsv')
for i in range(NUM_COLORS):
    color = cm(1.*i/NUM_COLORS)


def legend_without_duplicate_labels(ax):
    handles, labels = ax.get_legend_handles_labels()
    unique = [(h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]]
    ax.legend(*zip(*unique))


import plotly.express as px

def customLegend(fig, nameSwap):
    for i, dat in enumerate(fig.data):
        for elem in dat:
            if elem == 'name':
                print(fig.data[i].name)
                fig.data[i].name = nameSwap[fig.data[i].name]
    return(fig)


def renamelist(inlist, nameSwap):
    outlist=[]
    for elem in inlist:

        try:
            outlist.append(nameSwap[elem])
        except:
            outlist.append(elem)
    return(outlist)


if mainplot:

    typelist2 = renamelist(typelist, nameswap)
    sizelist = [40.] * len(typelist)

    raw_symbols = SymbolValidator().values
    namestems = []
    namevariants = []
    symbols = []
    for i in range(0, len(raw_symbols), 3):
        name = raw_symbols[i + 2]
        symbols.append(raw_symbols[i])
        namestems.append(name.replace("-open", "").replace("-dot", ""))
        namevariants.append(name[len(namestems[-1]):])

    namestems = np.unique(namestems)

    symbols = namestems[0:len(np.unique(typelist2))]

    symbols = ['bowtie',
               'circle', 'circle-cross', 'cross', 'diamond',
               'hexagon', 'hourglass', 'octagon', 'square', 'star',
               'triangle-down', 'x', ]
    nameswap2 = dict(zip(np.unique(typelist2), symbols))
    symbols2 = renamelist(typelist2, nameswap2)
    data = np.array([typelist2, efficiency_pm1list, dplist, sizelist])
    plotdata = pd.DataFrame(data=data.T)
    plotdata.columns = ['type', 'eff', 'dp', 'markersize']
    plotdata['symbols'] = symbols2
    plotdata['size'] = sizelist
    plotdata['PM0.5 efficiency_pm1 [%]'] = np.array(efficiency_pm1list0).astype('int')
    plotdata['PM1.0 efficiency_pm1 [%]'] = np.array(efficiency_pm1list).astype('int')
    plotdata['PM2.5 efficiency_pm1 [%]'] = np.array(efficiency_pm1list2).astype('int')
    plotdata['Differential Pressure [Pa]'] = np.array(dplist).astype('int')
    plotdata['Actual Volumeflow'] = (np.array(flowlist) * 100).astype('int') / 100.
    plotdata = plotdata.sort_values(by='type')
    # plotdata=plotdata[0:2]
    fig = px.scatter(plotdata, x="eff", y="dp", color="type",
                     size='size',
                     # symbol=symbols2[0:len(plotdata)],
                     symbol='type',
                     symbol_sequence=symbols,
                     labels={'eff':'Filtration efficiency_pm1 [%]',
                             'dp':'Differential Pressure [Pa]'},
                     title="Mask Benchmarking")


    fig.show()

    #
    arrleny = 10

    # add some remarks to the plot
    fig.add_annotation(
        x=95,
        y=8,
        xref="x",
        yref="y",
        text="Ideal Mask",
        showarrow=True,
        font=dict(
            family="Arial",
            size=24,
            color="#ffffff"
        ),
        align="center",
        arrowhead=1,
        arrowsize=0.6,
        arrowwidth=8,
        arrowcolor="#636363",
        axref='x',
        ayref='y',
        ax=95,
        ay=2,
        bordercolor="lightblue",
        borderwidth=2,
        borderpad=4,
        bgcolor="lightblue",
        opacity=0.8
    )

    fig.add_annotation(
        x=55,
        y=2,
        xref="x",
        yref="y",
        text="Ideal Mask",
        showarrow=True,
        font=dict(
            family="Arial",
            size=24,
            color="#ffffff"
        ),
        align="center",
        arrowhead=1,
        arrowsize=0.6,
        arrowwidth=8,
        arrowcolor="#636363",
        axref='x',
        ayref='y',
        ax=95,
        ay=2,
        bordercolor="lightblue",
        borderwidth=2,
        borderpad=4,
        bgcolor="lightblue",
        opacity=0.8
    )

    fig.add_annotation(
        x=95,
        y=5,
        xref="x",
        yref="y",
        text="Harder to Breath",
        showarrow=False,
        font=dict(
            family="Arial",
            size=16,
            color="#ffffff"
        ),
        align="center",

        bordercolor="lightblue",
        borderwidth=0,
        borderpad=4,
        bgcolor="#ff7f0e",
        opacity=0.8
    )

    fig.add_annotation(
        x=75,
        y=2,
        xref="x",
        yref="y",
        text="Less Efficient",
        showarrow=False,
        font=dict(
            family="Arial",
            size=16,
            color="#ffffff"
        ),
        align="center",

        bordercolor="lightblue",
        borderwidth=0,
        borderpad=4,
        bgcolor="#ff7f0e",
        opacity=0.8
    )

    fig.show()


    if upload:

        tabledata=plotdata.drop(columns=['markersize', 'eff', 'dp'])
        html=tabledata.to_html()
        print(html)

        username = 'user' # your username
        api_key = 'key' # your api key - go to profile > settings > regenerate key
        chart_studio.tools.set_credentials_file(username=username, api_key=api_key)

        # several plots for poor mans load balancing ;-)
        py.plot(fig, filename = 'overview', auto_open=True)
        py.plot(fig, filename = 'overview2', auto_open=True)
        py.plot(fig, filename = 'overview3', auto_open=True)

        # py.plot(fig, filename = 'Couture', auto_open=True)
        # py.plot(fig, filename = 'Kraftwerk', auto_open=True)

