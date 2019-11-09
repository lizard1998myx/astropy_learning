#!/bin/bash

ls ../aux/*.mkf > mkf_name.txt

# export HEADAS=/home/yuxi/Software/heasoft-6.26.1/x86_64-pc-linux-gnu-libc2.27/
# . $HEADAS/headas-init.sh

export CALDB=/root/Workshop/15032000/calib #please change this path according to your condition
export CALDBCONFIG=/root/Workshop/15032000/calib/caldb.config #please change this path according to your condition
export CALDBALIAS=/root/Workshop/15032000/calib/alias_config.fits #please change this path according to your condition
echo $CALDB

name="yuxi_beta_ad15032000g200170h" #output name

xselect @g2.txt
deadtime ${name}_g2.pi  exposure=EXPOSURE deadcol=G2_DEADT < mkf_name.txt
deadtime ${name}_g2_bgd.pi  exposure=EXPOSURE deadcol=G2_DEADT < mkf_name.txt
ascaarf ${name}_g2.pi rmffile=gis2v4_0.rmf outfile=${name}_g2.arf point=yes clobber=yes simple=yes # get the arf file
grppha infile="${name}_g2.pi" outfile="${name}_g2_grp.pha" clobber=yes chatter=0 comm="chkey ANCRFILE ${name}_g2.arf& chkey RESPFILE gis2v4_0.rmf& chkey BACKFILE ${name}_g2_bgd.pi& exit" # get the spectrum, with its response and background files
grppha infile="${name}_g2_grp.pha" outfile="${name}_g2_grp_sys.pi" clobber=yes chatter=0 comm="systematics 0-1023 0.01 & group min 20 & exit" # add 1% systematic error into 0-1023 channels, and rebin the spectrum with the minimum 20 counts

rm mkf_name.txt

exit 0
