import cv2
import numpy as np


def apply_white_balance(image: np.ndarray) -> np.ndarray:
    """
    Fix the blue-green color cast in underwater images.
    Underwater light absorbs red first, so we boost the red channel
    and slightly reduce blue to restore natural color balance.
    """
    # Split into B, G, R channels
    b, g, r = cv2.split(image)

    # Calculate the mean of each channel
    r_mean = np.mean(r)
    g_mean = np.mean(g)
    b_mean = np.mean(b)

    # Overall mean across all channels
    overall_mean = (r_mean + g_mean + b_mean) / 3

    # Scale each channel so its mean matches the overall mean
    # This compensates for the red channel being too weak underwater
    r_scale = overall_mean / (r_mean + 1e-6)
    g_scale = overall_mean / (g_mean + 1e-6)
    b_scale = overall_mean / (b_mean + 1e-6)

    # Apply scaling and clip to valid range [0, 255]
    r = np.clip(r * r_scale, 0, 255).astype(np.uint8)
    g = np.clip(g * g_scale, 0, 255).astype(np.uint8)
    b = np.clip(b * b_scale, 0, 255).astype(np.uint8)

    return cv2.merge([b, g, r])