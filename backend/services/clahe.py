import cv2
import numpy as np


def apply_clahe(image: np.ndarray, clip_limit: float = 2.0, tile_size: int = 8) -> np.ndarray:
    """
    Apply CLAHE (Contrast Limited Adaptive Histogram Equalization).
    
    Unlike regular histogram equalization, CLAHE:
    - Works on small local tiles rather than the whole image
    - Limits contrast amplification to avoid noise boosting
    - Preserves local detail while improving overall contrast
    
    We apply it to the L (lightness) channel in LAB color space
    to avoid shifting colors while enhancing contrast.
    """
    # Convert BGR to LAB color space
    # LAB separates lightness (L) from color (A=green-red, B=blue-yellow)
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

    # Split into L, A, B channels
    l, a, b = cv2.split(lab)

    # Create CLAHE object
    clahe = cv2.createCLAHE(
        clipLimit=clip_limit,
        tileGridSize=(tile_size, tile_size)
    )

    # Apply CLAHE only to the L (lightness) channel
    l_enhanced = clahe.apply(l)

    # Merge enhanced L back with original A and B
    lab_enhanced = cv2.merge([l_enhanced, a, b])

    # Convert back to BGR
    return cv2.cvtColor(lab_enhanced, cv2.COLOR_LAB2BGR)