#Combine two images with inverse-variance weighting V1.0
#Yuxi Meng 2019-05-29
#
# Terrible version & very very slow
# but it works

def test_combine():
    imagelist = ["ppr2_briggs_-0.5-t0500-XX-image.fits",
                 "ppr2_briggs_-0.5-t0500-YY-image.fits"]
	#however, this is not primary beam
    beamlist = ["ppr2_briggs_-0.5-t0500-XX-model.fits",
                "ppr2_briggs_-0.5-t0500-YY-model.fits"]
    output = "ppr2_briggs_-0.5-t0500-image_astropy_combination.fits"
    combine(imagelist, beamlist, output)


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



def combine ( imagelist, beamlist, output ):

	from astropy.io import fits

	if len(imagelist) != len(beamlist):
		print("Unequal list length.")
		return

	#open the first image as a basic
	hdul = fits.open(str(imagelist[0]))
	data = hdul[0].data
	[a, b, xsize, ysize] = data.shape

	imagedata = []
	beamdata = []

	#read the data
	for i in range(len(imagelist)):
		imagedata.append((fits.open(str(imagelist[i])))[0].data)
		beamdata.append((fits.open(str(beamlist[i])))[0].data)

	#check if the data table equals

	#make ylist and sigmalist by reading data
	for x in range(xsize):
		for y in range(ysize):
			ylist = []
			sigmalist = []
			for i in range(len(imagelist)):
				ylist.append(imagedata[i][0,0,x,y]/beamdata[i][0,0,x,y])
				sigmalist.append(1/beamdata[i][0,0,x,y])
			data[0,0,x,y] = inv_var_weighting(ylist, sigmalist)
			print(str(x) + ", " + str(y))

	hdul[0].data = data
	hdul.writeto(str(output))

	hdul.close()

	return


test_combine()
