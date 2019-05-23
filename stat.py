#Getting stat from votable file V1.0
#Yuxi Meng 2019-05-22

#import filename and a list of column names
#return a string with mean, std and median value
def stat( file_name, col_names ):
    #import the vot file
    from astropy.io.votable import parse_single_table
    from astropy.table import Table
    t = parse_single_table(str(file_name)).to_table()
    print("reading the file: " + str(file_name))

    #calculate the statistics
    import numpy as np

    info = ("\n======\n"
           + "Filename: " + str(file_name) + '\n'
           + "quantity of data: " + str(len(t))
           + '\n\n')

    for col_name in col_names:
        info = (info + "-- " + str(col_name) + " --\n"
               + "mean = " + str(np.mean(t[str(col_name)])) + '\n'
               + "std  = " + str(np.std(t[str(col_name)])) + '\n'
               +"med  = " + str(np.median(t[str(col_name)])) +'\n'
               + '\n')
    print(info)

    return info

#getting the string to put in the stat file
info = ""
for i in range(5):
    file_in = "image_" + str(i) + "_out.vot"
    info = info + stat(str(file_in), ['SNR', 'peak_flux', 'local_rms'])

#put the string in the file
fo = open("log_minUV40_briggs", "w")
fo.write(info)
fo.close
