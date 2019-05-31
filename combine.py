#Combine two images with inverse-variance weighting V2.3
#Yuxi Meng 2019-05-31
#
# armory version

from astropy.io import fits

#an example of combining images
def example_combine():
	imagelist = ["image_XX.fits", "image_YY.fits"]
	beamlist = ["beam_XX.fits", "beam_YY.fits"]
	output = "combination_V2.0.fits"
	combine(imagelist, beamlist, output)
	return

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

	if len(imagelist) != len(beamlist):
		print("Unequal list length.")
		return

	#open the first image as a basic
	hdul = fits.open(str(imagelist[0]))
	data = hdul[0].data

	ylist = []
	sigmalist = []

	for i in range(len(imagelist)):

		# read the data
		with fits.open(str(imagelist[i])) as imagehdul:
			imagedata = imagehdul[0].data
		with fits.open(str(beamlist[i])) as beamhdul:
			beamdata = beamhdul[0].data
		
		# make ylist and sigmalist
		ylist.append(imagedata)
		sigmalist.append(1/beamdata)

	#calculate
	hdul[0].data = inv_var_weighting(ylist, sigmalist)

	#save the changes
	hdul.writeto(str(output))
	hdul.close()

	return

#this is nothing but a Easter egg! :)
def hello():
	print("hello")
	return
