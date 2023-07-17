# try:
if 1:
    import torch
    from .processing_image import Preprocess  # noqa
    from .visualizing_image import SingleImageViz  # noqa
    from .modeling_frcnn import GeneralizedRCNN  # noqa
    from .utils import Config  # noqa
    from . import utils  # noqa
# except ImportError:
#    print("torch is not installed")


# for visualizing output
def showarray(a, fmt="jpeg"):
    import PIL.Image
    import io
    import numpy as np
    from IPython.display import Image, display

    a = np.uint8(np.clip(a, 0, 255))
    f = io.BytesIO()
    PIL.Image.fromarray(a).save(f, fmt)
    display(Image(data=f.getvalue()))
