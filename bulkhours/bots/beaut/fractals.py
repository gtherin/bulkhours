import numpy as np
from pylab import imshow, show
from timeit import default_timer as timer

# from numba import jit


# @jit
def mandel(x, y, max_iters):
    """
    Given the real and imaginary parts of a complex number,
    determine if it is a candidate for membership in the Mandelbrot
    set given a fixed number of iterations.
    """
    c = complex(x, y)
    c0 = complex(0.285, 0.01)
    z = 0.0j
    for i in range(max_iters):
        z = z * z + c + c0
        if (z.real * z.real + z.imag * z.imag) >= 4:
            return i

    return max_iters


# @jit
def create(min_x, max_x, min_y, max_y, image, iters):
    """
    Iterates over all the pixels in the image, computing the complex coordinates from the pixel coordinates, and calls the mandel function at each pixel. The return value of mandel is used to color the pixel.
    """
    height = image.shape[0]
    width = image.shape[1]

    pixel_size_x = (max_x - min_x) / width
    pixel_size_y = (max_y - min_y) / height

    for x in range(width):
        real = min_x + x * pixel_size_x
        for y in range(height):
            imag = min_y + y * pixel_size_y
            color = mandel(real, imag, iters)
            image[y, x] = color


def get(min_x=-2.3, max_x=0.7, min_y=-1.5, max_y=1.5, iters=20):
    """Next we create a 1536x1024 pixel image as a numpy array of bytes.
    We then call create_fractal with appropriate coordinates to fit the whole mandelbrot set."""
    image = np.zeros((1536, 1536), dtype=np.uint8)
    create(min_x, max_x, min_y, max_y, image, iters)
    return image


class Mandel:
    def __init__(self):
        self.images = {}

    def get(self, iters):
        if iters not in self.images:
            self.images[iters] = get(iters=iters)
        return self.images[iters]

    def show(self, ax, iters, cmap):
        import matplotlib.pyplot as plt

        ax.imshow(self.get(iters), cmap=plt.cm.get_cmap(cmap))
        ax.set_axis_off()
        return ax
