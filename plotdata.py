# plot the data made by summary.py
# 2019-05-31 Yuxi Meng

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# read two files
file_default = pd.read_csv('output_default.csv')
file_minuv40 = pd.read_csv('output_minUV40.csv')


def datainput(ax, xstring, ystring, **param_dict):
    """
    datainput()
    
    put the data into an axis
    this axis is used for future plotting
    parameter can be set as well (optional)
    
    data are from the two given files
    color and label are given
    """
    
    xstring = str(xstring)
    ystring = str(ystring)
    #ylabel = str(ylabel)
    
    ax.plot(file_default[xstring][:9],
             file_default[ystring][:9],
             'xkcd:pink',
             **param_dict, label='default_all')
    ax.plot(file_default[xstring][-9:],
             file_default[ystring][-9:],
             'xkcd:light red',
             **param_dict, label='default_center')
    ax.plot(file_minuv40[xstring][:9],
             file_minuv40[ystring][:9],
             'xkcd:sky blue',
             **param_dict, label='minuv40_all')
    ax.plot(file_minuv40[xstring][-9:],
             file_minuv40[ystring][-9:],
             'xkcd:blue',
             **param_dict, label='minuv40_center')
    #ax.set_ylabel(ylabel)
    #ax.legend(loc='best')
    return


"""
The plotting is done with following steps:
    
    1.set up the figure and axis(es)
    2.load the data with datainput() function
    3.edit the title, label, legend etc.
    4.some special consideration (e.g. annotation)
    5.arrange and show the figure
    
2019-05-31 Sgt.Lizard
"""

# First Figure: major plot of noise feature
#
fig0, ax0 = plt.subplots()
datainput(ax0, 'local_rms_mean', 'psf_b')

# set the note and legend
ax0.set_title('Noise Feature')
ax0.set_ylabel('Synthesis Beam (arcsec)')
ax0.set_xlabel('Local RMS')
ax0.legend(loc='lower right')
ax0.grid()

# special: set the annotation of briggs value

# adjust the location of annotation
annotate_x = [-0.0008, -0.0015, -0.002,
              -0.002, -0.002, -0.002,
              -0.002, -0.002, -0.002]
annotate_y = [2, -50, 0, 0, 0, 0, 0, 0, 0]

# make annotations
for i in range(9):   
    ax0.annotate(str(file_default['briggs'][i]),
                 (file_default['local_rms_mean'][i] + annotate_x[i],
                  file_default['psf_b'][i] + annotate_y[i]))

# arrange the figure
fig0.tight_layout()


# Second Figure: 2x2 subplots
#
fig1, ((ax1, ax2),(ax3,ax4)) = plt.subplots(2,2)

# 1st plot: source count
datainput(ax1, 'briggs', 'source_count')
ax1.set_ylabel('Source Count')
#ax1.grid()
ax1.set_yticks(np.arange(500, 3001, 500))

# 2nd plot: SNR
datainput(ax2, 'briggs', 'SNR_mean')
ax2.set_ylabel('SN ratio')
ax2.set_yticks(np.arange(12, 17.1, 1))


# 3rd plot: local_rms
datainput(ax3, 'briggs', 'local_rms_mean')
ax3.set_ylabel('Local RMS')
ax3.set_xlabel('Briggs')

# 4th plot: peak_flux
datainput(ax4, 'briggs', 'peak_flux_mean')
ax4.set_ylabel('Peak Flux')
ax4.set_xlabel('Briggs')

fig1.tight_layout()
plt.show()
