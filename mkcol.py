#making columns with astropy V1.1
#Yuxi Meng 2019-05-22


#An example
#
#for parameter in range(5):
#    file_in = "image_" + parameter + "_in.xml"
#    file_out = "image_" + parameter + "_out.xml"
#    ra_cen = 12.2574702070
#    dec_cen = -19.9815841286
#    mkcol(file_in, file_out, ra_cen, dec_cen)


#make SNR, area, sep columns from an input votable
#save the output to a new file
#
#separation is the angular separation of the source and the center
#coordinates of the center should be in degrees and fk5 system
#
def mkcol( file_in, file_out, ra_cen, dec_cen ):
    #inport the vot file
    from astropy.io.votable import parse_single_table
    from astropy.table import Table
    t = parse_single_table(str(file_in)).to_table()
    print("reading the file: " + str(file_in))
    print("please wait")

    #new column of SNR and area (in the unit of beam)
    t['SNR'] = t['peak_flux']/t['local_rms']
    t['area'] = t['int_flux']/t['peak_flux']

    #calculating separation
    import numpy as np
    from astropy import units as u
    from astropy.coordinates import Angle
    from astropy.coordinates import SkyCoord

    c0 = SkyCoord(Angle(ra_cen * u.deg), Angle(dec_cen * u.deg), frame='fk5')
    seplist = []

    for i in range(len(t)):
        c = SkyCoord(Angle(t['ra'][i] * u.deg), Angle(t['dec'][i] * u.deg), frame='fk5')
        sep = c.separation(c0)
        seplist.append(sep.degree)
    t['sep'] = seplist
    t['sep'].unit = 'deg'

    #saving file
    from astropy.io.votable import from_table, writeto
    votable = from_table(t)
    writeto(votable, str(file_out))
    print(str(file_out) + "saved successfully :)")
    print()

    return;


