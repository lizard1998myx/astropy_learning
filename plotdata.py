# plot the data made by summary.py V1.1
# 2019-06-01 Yuxi Meng

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# read files
file_default = pd.read_csv('output_default.csv')
file_minuv20 = pd.read_csv('output_minuv20.csv')
file_minuv40 = pd.read_csv('output_minuv40.csv')
file_minuv80 = pd.read_csv('output_minuv80.csv')

def plotter(ax, xlist, ylist, color, label, **param_dict):
    """
    plotter()
    
    basic plotter
    automatically plot two lines
    
    they are of same color but different styles
    """
    ax.plot(xlist[:9], ylist[:9], **param_dict,
            color=color, marker='.', linestyle='dashed',
            label=str(label)+"_all")
    ax.plot(xlist[-9:], ylist[-9:],
            color=color, marker='.', **param_dict,
            label=str(label)+"_center")
    
    return

def datainput(ax, xstring, ystring, **param_dict):
    """
    datainput()
    
    put the data into an axis
    this axis is used for future plotting
    parameter can be set as well (optional)
    the plot will be gridded
    use ax.grid() again to cancel it
    
    data are from the two given files
    color and label are given
    """
    
    xstring = str(xstring)
    ystring = str(ystring)
    
    # default red
    plotter(ax, file_default[xstring], file_default[ystring],
            "xkcd:red", "default", **param_dict)
 
    # minuv 20 golden
    plotter(ax, file_minuv20[xstring], file_minuv20[ystring],
            "xkcd:golden", "minuv20", **param_dict)
        
    # minuv 40 green
    plotter(ax, file_minuv40[xstring], file_minuv40[ystring],
            "xkcd:green", "minuv40", **param_dict)
    
    # minuv 80 blue
    plotter(ax, file_minuv80[xstring], file_minuv80[ystring],
            "xkcd:blue", "minuv80", **param_dict)
    
    ax.grid()
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
fig0, ax0 = plt.subplots(figsize=(10, 8))
datainput(ax0, 'local_rms_mean', 'psf_b')

# set the note and legend
ax0.set_title('Noise Feature')
ax0.set_ylabel('Synthesis Beam (arcsec)')
ax0.set_xlabel('Local RMS')
ax0.legend(loc='lower right')

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
fig1, ((ax1, ax2),(ax3,ax4)) = plt.subplots(2,2, figsize=(10, 8))

# 1st plot: local_rms
datainput(ax1, 'briggs', 'local_rms_mean')
ax1.set_ylabel('Local RMS')
ax1.set_xlabel('Briggs Parameter')
ax1.grid()
ax1.legend()

# 2nd plot: peak_flux
datainput(ax2, 'briggs', 'peak_flux_mean')
ax2.set_ylabel('Peak Flux')
ax2.set_xlabel('Briggs Parameter')
ax2.grid()

# 3rd plot: source count
datainput(ax3, 'briggs', 'source_count')
ax3.set_ylabel('Source Count')
ax3.set_xlabel('Briggs Parameter')
ax3.grid()
ax3.set_yticks(np.arange(500, 3001, 500))

# 4th plot: SNR
datainput(ax4, 'briggs', 'SNR_mean')
ax4.set_ylabel('SN ratio')
ax4.set_xlabel('Briggs Parameter')
ax4.grid()
ax4.set_yticks(np.arange(12, 17.1, 1))

# arrange and show the figure
fig1.tight_layout()
plt.show()
