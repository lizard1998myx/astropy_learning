#Combine two images with inverse-variance weighting V2.2
#Yuxi Meng 2019-05-30
#

from astropy.io import fits

#test the combine function
def test_combine():
    imagelist = ["ppr2_briggs_-0.5-t0500-XX-image.fits",
                 "ppr2_briggs_-0.5-t0500-YY-image.fits"]
    beamlist = ["ppr2_briggs_0.5-XX-dirty_beamXX.fits",
                "ppr2_briggs_0.5-XX-dirty_beamYY.fits"]
    output = "ppr2_briggs_-0.5-t0500-image_astropy_combination_V2.2.fits"
    combine(imagelist, beamlist, output)

#calculate the inverse-variance weighting
#aggregate radom variables to minimize the variance of the weighted average
def inv_var_weighting ( ylist, sigmalist ):
    
	if len(ylist) != len(sigmalist):
		print("Unequal list length.")
		return
    
	numerator = 0	#define the numerator
	denominator = 0	#define the denominator

	for i in range(len(ylist)):
		numerator = numerator + (ylist[i]/(sigmalist[i]*sigmalist[i]))
		denominator = denominator + (1/(sigmalist[i]*sigmalist[i]))

	return numerator/denominator


#combine two images
def combine ( imagelist, beamlist, output ):

#	from astropy.io import fits

	if len(imagelist) != len(beamlist):
		print("Unequal list length.")
		return

	#open the first image as a basic
	hdul = fits.open(str(imagelist[0]))
	data = hdul[0].data

	ylist = []		#store a list of variables
	sigmalist = []	#store a list of variance

	for i in range(len(imagelist)):

		# read the data tables
		with fits.open(str(imagelist[i])) as imagehdul:
			imagedata = imagehdul[0].data
		with fits.open(str(beamlist[i])) as beamhdul:
			beamdata = beamhdul[0].data
		
		# make ylist and sigmalist
		# y = Image instead of Image/Beam
		# sigma = 1/Beam
		ylist.append(imagedata/beamdata)
		sigmalist.append(1/beamdata)

	#calculate
	hdul[0].data = inv_var_weighting(ylist, sigmalist)

	#save the changes
	hdul.writeto(str(output))
	hdul.close()

	return



test_combine()
