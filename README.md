# Chandra-Image-Processing
Chandra image processing tools for UROP Project
Tools:

Header.py: stores all python functions required for tools to work

find_average_brightness.py: creates modified image of given data to substract the average brightness radially with given width(width greater than 500 requires modifing rbins in Header.py

find_center.py: finds and returns the calculated center of the data as well as image of the center ( most chandra data with TE exposure and ccd_id 7 data seems to try and center observation near 4100 4100)

find_radial_profile.py: calculates and returns graph plotting average brightness from the center of the provided data

make_image.py: creates base image with no alterations of provided chandra data

Inputs:

recommended inputs for all files: 

./file.py "directory in which data is located" "Name of _evt2.fits file" x-sample_cordinate_of_center(recommended default 4100) y-sample_cordinate_of_center(recommended default 4100) (following inputs only needed for find brightness file) width_of_image(max 250 unless RBINS is modified) lower_limit_of_surfbrightness_bar upper_limit_of_surfbrightness_bar

quotes are strings and underscored inputs are integers or doubles (they are converted to float by the tools)
