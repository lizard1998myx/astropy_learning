#making subsets with astropy V1.1
#Yuxi Meng 2019-05-31
#
# armory version

from astropy.io.votable import parse_single_table, from_table, writeto
from astropy.table import Table

#an example of using mksub
def example_mksub():
	for parameter in range(5):
	    file_in = "image_" + str(parameter) + "_in.vot"
	    file_out = "image_" + str(parameter) + "_out.vot"
	    mksub(file_in, file_out)
	return

#make a subset from the input file
#save the output to a new file
#
#the rule of subset is separation <= 10.0 in this example
#you should edit the functions for other purpose
#
def mksub( file_in, file_out ):

	#import the vot file
	t = parse_single_table(str(file_in)).to_table()
	print("reading the file: " + str(file_in))
	print("the original file has " + str(len(t)) + " rows")
	print("please wait")

	dellist = []

	#rule of making subset (edit here)
	for i in range(len(t)):
		if t['sep'][i] >= 10.0:
			dellist.append(i)

	del t[dellist]
	print(str(len(dellist)) + " rows deleted")
	print("the subset has " + str(len(t)) + " rows")

	#saving file
	votable = from_table(t)
	writeto(votable, str(file_out))
	print("subset created :)")
	print()

	return
