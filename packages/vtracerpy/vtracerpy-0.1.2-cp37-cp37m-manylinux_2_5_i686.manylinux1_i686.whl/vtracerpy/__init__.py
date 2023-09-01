from .vtracerpy import *
import numpy as np
import cv2

__doc__ = vtracerpy.__doc__
if hasattr(vtracerpy, "__all__"):
    __all__ = vtracerpy.__all__

def image_to_svg(image: np.ndarray,
                 colormode: str = 'color',
                 color_precision: int = 8,
                 layer_difference: int = 16,
                 hierarchical: str = 'stacked',
                 path_precision: int = 8,
                 mode: str = 'spline',
                 corner_threshold: int = 60,
                 length_threshold: float = 4.0,
                 max_iterations: int = 10,
                 splice_threshold: int = 45,
                 filter_speckle: int = 4)->str:
    """
    Convert an image to SVG format with specified parameters.

    Parameters:
    - image: (np.ndarray)The input image with shape (H,W,3) to be converted to SVG format.
    - colormode (str, optional): True color image `color` (default) or Binary image `bw`.
    - color_precision (int, optional): Number of significant bits to use in an RGB channel. Defaults to 8.
    - layer_difference (int, optional): Color difference between gradient layers. Defaults to 16.
    - hierarchical (str, optional): Hierarchical clustering. Can be `stacked` (default) or non-stacked `cutout`. Only applies to color mode.
    - path_precision (int, optional): Parameter not described in provided options. Defaults to 8.
    - mode (str, optional): Curve fitting mode. Can be `pixel`, `polygon`, `spline`. Defaults to 'spline'.
    - corner_threshold (int, optional): Minimum momentary angle (degree) to be considered a corner. Defaults to 60.
    - length_threshold (float, optional): Perform iterative subdivide smooth until all segments are shorter than this length. Defaults to 4.0.
    - max_iterations (int, optional): Parameter not described in provided options. Defaults to 10.
    - splice_threshold (int, optional): Minimum angle displacement (degree) to splice a spline. Defaults to 45.
    - filter_speckle (int, optional): Discard patches smaller than X px in size. Defaults to 4.

    Returns:
    - str: The SVG representation of the input image.
    """
    if colormode == 'bw':
        if len(image.shape)==3:
            image = image[:,:,0]
        image = np.ascontiguousarray(image)
        result = binary_image_to_svg(
            image=image,
            path_precision=path_precision,
            mode=mode,
            corner_threshold=corner_threshold,
            length_threshold=length_threshold,
            max_iterations=max_iterations,
            splice_threshold=splice_threshold,
            filter_speckle=filter_speckle)
    elif colormode == 'color':
        image = np.ascontiguousarray(image)
        result = color_image_to_svg(
            image=image,
            layer_difference=layer_difference,
            filter_speckle=filter_speckle,
            color_precision=color_precision,
            hierarchical=hierarchical,
            path_precision=path_precision,
            mode=mode,
            corner_threshold=corner_threshold,
            length_threshold=length_threshold,
            max_iterations=max_iterations,
            splice_threshold=splice_threshold)
    return result