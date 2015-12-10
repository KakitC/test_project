"""
Functions to try out image processing code for raster engrave software path.
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
import numpy as np
import cProfile

# def closest_color(value):
#     array = [0, 255]
#     idx = (np.abs(array - value)).argmin()
#     return array[idx]

# TODO Optimize this function
def dither_floyd(img):
    """ Perform Floyd-Steinberg dithering on an image, converting greyscale to
    black and white dots.

    :param img: Input image
    :type img: PIL.Image.Image
    :return: Dithered image
    :rtype: PIL.Image.Image
    """

    img_pix = np.array(img, dtype=np.uint8)

    for i in range(img_pix.shape[0]):
        for j in range(img_pix.shape[1]):
            old_px = img_pix[i][j]
            new_px = 0 if old_px < 128 else 255
            img_pix[i][j] = new_px
            err = old_px - new_px

            if j+1 < img_pix.shape[1]:
                img_pix[i][j+1] += err * 7 >> 4
            if i+1 < img_pix.shape[0]:
                img_pix[i+1][j] += err * 5 >> 4
                if j > 0:
                    img_pix[i+1][j-1] += err * 3 >> 4
                if j+1 < img_pix.shape[1]:
                    img_pix[i+1][j+1] += err * 1 >> 4

    return Image.fromarray(img_pix, "L")


def dither_sierra_lite(img):
    """ Perform Floyd-Steinberg dithering on an image, converting greyscale to
    black and white dots.

    :param img: Input image
    :type img: PIL.Image.Image
    :return: Dithered image
    :rtype: PIL.Image.Image
    """

    #img_pix = np.array(img, dtype=np.uint8)
    img_pix = np.array(img)

    for i in range(img_pix.shape[0]):
        for j in range(img_pix.shape[1]):
            old_px = img_pix[i][j]
            new_px = 0 if old_px < 128 else 255
            img_pix[i][j] = new_px
            err = old_px - new_px

            if j+1 < img_pix.shape[1]:
                #img_pix[i][j+1] += err >> 1
                img_pix[i][j+1] += err /2.
            if i+1 < img_pix.shape[0]:
                #img_pix[i+1][j] += err >> 2
                img_pix[i+1][j] += err /4.
                if j > 0:
                    #img_pix[i+1][j-1] += err >> 2
                    img_pix[i+1][j-1] += err /4.

    return Image.fromarray(img_pix, "L")


def dither_ordered(img):
    # map = np.array([[1,3],
    #                 [4,2]]) / 5. * 255

    map = np.array([[1,8,4],
                    [7,6,3],
                    [5,2,9]]) / 10. * 255

    # map = np.array([[1,9,3,11],
    #                 [13,5,15,7],
    #                 [4,12,2,10],
    #                 [16,8,14,6]]) / 17. * 255

    map_shape_i = map.shape[0]
    map_shape_j = map.shape[1]

    # img_pix = np.array(img, dtype=np.uint8)
    img_pix = np.array(img)

    for i in range(img_pix.shape[0]):
        for j in range(img_pix.shape[1]):
            img_pix[i][j] = 255 if img_pix[i][j] > map[i % map_shape_i][j % map_shape_j] else 0

    return Image.fromarray(img_pix, "L")


def raster_dither(in_file):
    """ Convert an image to greyscale, and process it before performing
    dithering algorithm to prepare for laser cutting as a bitmap.

    :param in_file: <string> relative file path and name of input image
    :return: Dithered image converted to raster bitmap
    """

    with Image.open(in_file) as pic:
        pic = pic.convert(mode="L")  # To greyscale

        # Image brightness leveling
        brightness = ImageStat.Stat(pic).mean
        if brightness[0] < 100:
            pic = ImageEnhance.Brightness(pic).enhance(1.75)
        elif brightness[0] < 120:
            pic = ImageEnhance.Brightness(pic).enhance(1.2)

        #pic = dither_floyd(pic)
        #pic = dither_sierra_lite(pic)
        pic = dither_ordered(pic)

        return pic


def raster_ips(in_file):
    """ Convert an image to greyscale, and tweak the contrast/brightness and
    low-pass filter until it is ready to be sent to the laser as a power/speed
    bitmap.
    :param in_file: <string> relative file path and name of input image
    :return: Image converted to raster bitmap
    """

    # Main processing blocks, filters
    with Image.open(in_file) as pic:
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

        return pic


# Main test function
def main_test():
    """
    Runs laser rasterizing algorithm on images in ./test_pics/raster/ and
    measures runtime performance. Saves processed the black and white images in
    the same folder.
    """
    start_time = time()
    n = 0
    in_file, out_file = "", ""
    while 1:
    #while n < 3:
        if OS == "Windows":
            in_file = "test_pics\\raster\\raster_test" + str(n) + ".jpg"
            #out_file = "test_pics\\raster\\raster_test" + str(n) + "out.jpg"
            out_file = "test_pics\\raster\\raster_test" + str(n) + "outDither.jpg"
        elif OS == "Linux":
            in_file = "test_pics/raster/raster_test" + str(n) + ".jpg"
            out_file = "test_pics/raster/raster_test" + str(n) + "out.jpg"
        print(str(n))

        try:
            start = time()

            with Image.open(in_file) as pic:
                print("Size: " + str(pic.size))

            #pic = raster_ips(in_file)
            pic = raster_dither(in_file)
            pic.save(out_file)

            print("Time: " + str(time() - start))
            print("")

        except IOError:
            break
        n += 1

    print("Time taken: " + str(time() - start_time))

# Run the script
if __name__ == "__main__":
    # main_test()
    import pyximport
    pyximport.install()
    import rasterIPScython
    rasterIPScython.main_test()