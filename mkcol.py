#making columns with astropy V1.3
#Yuxi Meng 2019-05-31
#
# armory version

from astropy import units as u
from astropy.io import fits
from astropy.io.votable import parse_single_table, from_table, writeto
from astropy.table import Table
from astropy.coordinates import Angle, SkyCoord
import numpy as np

#an example of using mkcol & cen_coord
def example_mkcol():
	for parameter in range(5):
		file_in = "image_" + parameter + "_comp.vot"
		file_out = "image_" + parameter + "_all.vot"
		[ra_cen, dec_cen] = cen_coord("image_" + parameter +".fits")
		mkcol(file_in, file_out, ra_cen, dec_cen)


#make SNR, area, sep columns from an input votable
#save the output to a new file
#
#separation is the angular separation of the source and the center
#coordinates of the center should be in degrees and fk5 system
#
def mkcol( file_in, file_out, ra_cen, dec_cen ):

	#import the vot file
	t = parse_single_table(str(file_in)).to_table()
	print("reading the file: " + str(file_in))
	print("please wait")

	#new column of SNR and area (in the unit of beam)
	t['SNR'] = t['peak_flux']/t['local_rms']
	t['area'] = t['int_flux']/t['peak_flux']

	#calculating separation


	c0 = SkyCoord(Angle(ra_cen * u.deg), Angle(dec_cen * u.deg), frame='fk5')
	seplist = []

	for i in range(len(t)):
		c = SkyCoord(Angle(t['ra'][i] * u.deg),
			     Angle(t['dec'][i] * u.deg), frame='fk5')
		sep = c.separation(c0)
		seplist.append(sep.degree)
	t['sep'] = seplist
	t['sep'].unit = 'deg'

	#saving file
	votable = from_table(t)
	writeto(votable, str(file_out))
	print(str(file_out) + "saved successfully :)")
	print()

	return


#to read the central ra and dec from the fits header
#
def cen_coord( file_name ):
	with fits.open(str(file_name)) as hdul:
		hdr = hdul[0].header
		ra_cen  = hdr['CRVAL1']
		dec_cen = hdr['CRVAL2']
	return [ra_cen, dec_cen]

