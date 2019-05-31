#Getting statistics from table file V2.2
#Yuxi Meng 2019-05-31
#
# armory version

from astropy.io.votable import parse_single_table, from_table, writeto
from astropy.table import Table
import numpy as np

#an example of making a csv table
def example_stat():

	#create a empty table 't' with columns needed
	t = Table(names=('filename', 'source_count', 
		         'SNR_mean', 'SNR_std', 'SNR_med',
		         'peak_flux_mean', 'peak_flux_std', 'peak_flux_med',
		         'local_rms_mean', 'local_rms_std', 'local_rms_med',
		         'psf_a', 'psf_b'),
		  meta={'name': 'first table'},
		  dtype=('U25', 'i4', 'f8', 'f8', 'f8', 'f8', 'f8', 'f8',
		         'f8', 'f8', 'f8', 'f8', 'f8'))

	#getting information from each votable file to the output table
	for j in ["all", "sub"]:
	    for i in [-2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2]:
		file_in = "image_" + str(i) + "_" + str(j) + ".vot"
		t.add_row(stat(str(file_in), 
		               ['SNR', 'peak_flux', 'local_rms'],
		               ['psf_a', 'psf_b']))

	#saving file (in csv)
	t.write("output.csv")

	return


#  import filename and two list of column names
#
#  return a list with the following quantities:
#  filename (string) and source count
#  mean, std, median value of columns from 'stat_col_names'
#  median value of columns from 'single_col_names'
#
def stat( file_name, stat_col_names, single_col_names ):

	#import the vot file
	t = parse_single_table(str(file_name)).to_table()
	print("+ reading the file: " + str(file_name))

	#calculate the statistics, put them into list 'info'
	#you can use np.round(i, j) to simplify the data

	#get file name and source count (number of rows)
	print("- filename and source count")
	info = [file_name, len(t)]

	#get mean, standard dev, and median of some columns
	for col_name in stat_col_names:
		print("- mean, std and median of " + str(col_name))
		info.append(np.nanmean(t[str(col_name)]))
		info.append(np.nanstd(t[str(col_name)]))
		info.append(np.nanmedian(t[str(col_name)]))

	#get median of some columns
	for col_name in single_col_names:
		print("- median of " + str(col_name))
		info.append(np.median(t[str(col_name)]))

	print(info)
	print()

	return info


#  extra: saving numpy table in the format of votable
def savevot( table, output_name ):
	writeto(from_table(table), str(output_name))
	print(str(output_name) + "saved in votable successfully!")
	return
