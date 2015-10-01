"""
Functions to try out image vectorizing algorithms for vector cutting software
path.
"""

__author__ = 'kakit'

# # Moved OS dependent import to main_test()
# import platform
# OS = platform.system()
# # Get most precise time function
# if OS == "Windows":
#     from time import clock as time
# elif OS == "Linux":
#     from time import clock as time

from PIL import Image, ImageEnhance, ImageFilter, ImageOps, ImageChops, \
    ImageColor, ImageStat
from rasterIPS import raster_ips
import numpy as np


def vector_preprocess(image_file):
    """
    Filter an image to black and white lines only for vector pathing

    :param image_file: Filepath for image to be processed
    :type: String
    :return: Image filtered to black lines and white background only
    :rtype: PIL.Image.Image
    """

    return raster_ips(image_file)

def get_normals(pic, kernel_size=3):
    """
    Calculate the gradient of the incoming black and white line image.

    Creates a 3D array of the gradient, where the first 2 "channels" are X and
    Y vector components respectively. The third channel is only for RGB
    compatability, and is left empty.

    :param pic: Greyscale image
    :type: PIL.Image.Image

    :param kernel_size: 3x3 or 5x5 Sobel derivative convolution kernel, only
    accepts values 3 and 5
    :type: int

    :return: Height x Width x 3 sized numpy array of <X,Y,(0)> gradient data
    :rtype: numpy.array
    """

    # Define hori/vert convolution kernels
    if kernel_size == 3:
        hori_kernel = ImageFilter.Kernel((3, 3), [-1, -2, -1,
                                                  0, 0, 0,
                                                  1, 2, 1],
                                         scale=1, offset=127)
        vert_kernel = ImageFilter.Kernel((3, 3), [1, 0, -1,
                                                  2, 0, -2,
                                                  1, 0, -1],
                                         scale=1, offset=127)
    elif kernel_size == 5:
        hori_kernel = ImageFilter.Kernel((5, 5), [-1, -4, -6, -4, -1,
                                                  -2, -8, -12, -8, -2,
                                                  0, 0, 0, 0, 0,
                                                  2, 8, 12, 8, 2,
                                                  1, 4, 6, 4, 1],
                                         scale=5, offset=127)
        vert_kernel = ImageFilter.Kernel((5,5), [1, 2, 0, -2, -1,
                                                 4, 8, 0, -8, -4,
                                                 6, 12, 0, -12, -6,
                                                 4, 8, 0, -8, -4,
                                                 1, 2, 0, -2, -1],
                                         scale=5, offset=127)
    else:
        raise ValueError

    pic = pic.filter(ImageFilter.SMOOTH_MORE)

    # Pick out horizontal and vertical edges with convolution kernel
    hori_edges = pic.filter(hori_kernel)
    vert_edges = pic.filter(vert_kernel)

    # Put each set of edges on a different color channel
    hori_pix = np.array(hori_edges, dtype=np.uint8)
    vert_pix = np.array(vert_edges, dtype=np.uint8)
    blank_ch = np.zeros(hori_pix.shape, dtype=np.uint8)

    edge_pix = np.dstack((hori_pix, vert_pix, blank_ch))
    return edge_pix


def vector_ips(in_file):
    """
    Generate vector path lines from a pixel image for laser cutting toolpath

    :param in_file: Filepath for image to be vectorized
    :return: Original image in black and white marked with cutting path lines
    :type: PIL.Image.Image
    """

    # Get the picture ready to be vectorized
    pic = vector_preprocess(in_file)
    # Calculate normal vectors at each point
    normal_map = get_normals(pic, kernel_size=5)

    overlay = Image.fromarray(normal_map, "RGB")
    pic = pic.convert("RGB")
    pic = Image.blend(pic, overlay, .5)

    return pic


def main_test():
    """
    Run vectorizing algorithm on pictures in ./test_pics/vector/ and measures
    runtime performance. Saves the images with the toolpaths overlaid in the
    same folder.
    """
    import platform

    OS = platform.system()
    # Get most precise time function
    if OS == "Windows":
        from time import clock as time
    elif OS == "Linux":
        from time import clock as time

    start_time = time()
    n = 0
    in_file, out_file = "", ""
    while 1:
        if OS == "Windows":
            in_file = "test_pics\\vector\\vector_test" + str(n) + ".jpg"
            out_file = "test_pics\\vector\\vector_test" + str(n) + "out.jpg"
        elif OS == "Linux":
            in_file = "test_pics/vector/vector_test" + str(n) + ".jpg"
            out_file = "test_pics/vector/vector_test" + str(n) + "out.jpg"
        print("Image " + str(n))

        try:
            start = time()
            pic = vector_ips(in_file)
            print("Size: " + str(pic.size))
            print("Time: " + str(time() - start))
            pic.save(out_file)

        except IOError:
            break
        n += 1
    print("Total time taken: " + str(time() - start_time))

if __name__ == "__main__":
    main_test()
