import sys
sys.path.append('/home/lizard/python/armory')

from astropy.table import Table
from mkcol import mkcol, cen_coord
from mksub import mksub
from summary import summary

def main():
	print(str(sys.argv))
	for i in range(2, len(sys.argv)):
		expandtable(sys.argv[1], sys.argv[i])
	return
	
def expandtable(fitsname, tablename):
	fitsname = str(fitsname)
	tablename = str(tablename)
	[ra_cen, dec_cen] = cen_coord(fitsname)
	mkcol(tablename, tablename.replace('comp', 'all'), ra_cen, dec_cen)
	mksub(tablename.replace('comp', 'all'), tablename.replace('comp', 'sub'))
	return

main()
