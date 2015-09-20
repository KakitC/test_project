"""
Functions to perform image processing for raster engrave image.
"""
__author__ = 'kakit'

import platform
OS = platform.system()
if OS == "Windows":
    from time import clock as time
elif OS == "Linux":
    from time import clock as time

from PIL import Image, ImageOps, ImageFilter, ImageChops, ImageEnhance, \
    ImageStat

def raster_ips(in_file, out_file):
    """ Convert an image to greyscale, and tweak the contrast/brightness and
    low-pass filter until it is ready to be sent to the laser as a power/speed
    bitmap.
    :param in_file: <string> relative file path and name of input image
    :param out_file: <string> directory and name of output image
    :return: True, exception based failure
    """

    # Main processing blocks, filters
    with Image.open(in_file) as pic:
        # Debug
        print("Size: " + str(pic.size))
        start = time()

        pic = pic.convert(mode="L")  # To greyscale

        edges = pic.filter(ImageFilter.CONTOUR)  # Pick out edges
        edges = edges.filter(ImageFilter.SMOOTH_MORE)  # Smooth noise

        pic = pic.filter(ImageFilter.SMOOTH_MORE)  # Smooth noise in original

        # Brightness leveling for dark images
        brightness = ImageStat.Stat(pic).mean
        if brightness[0] < 100:
            pic = ImageEnhance.Brightness(pic).enhance(1.75)
        elif brightness[0] < 120:
            pic = ImageEnhance.Brightness(pic).enhance(1.2)

        pic = ImageChops.multiply(pic, edges)  # Recombine edges for crispness
        pic = ImageOps.posterize(pic, 1)  # Down from grey to black and white
        pic = ImageOps.autocontrast(pic)  # Convert grey to white, black same

        pic.save(out_file)

        print("Time: " + str(time() - start))
        print("")

    return True

start_time = time()
n = 0
while 1:
    if OS == "Windows":
        in_file = "test_pics\\raster\\raster_test" + str(n) + ".jpg"
        out_file = "test_pics\\raster\\raster_test" + str(n) + "out.jpg"
    elif OS == "Linux":
        in_file = "test_pics/raster/raster_test" + str(n) + ".jpg"
        out_file = "test_pics/raster/raster_test" + str(n) + "out.jpg"
    print(str(n))

    try:
        raster_ips(in_file, out_file)
    except IOError:
        break
    n += 1

print("Time taken: " + str(time() - start_time))