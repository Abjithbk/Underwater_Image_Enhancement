import numpy as np
from services.white_balance import apply_white_balance
from services.clahe import apply_clahe
from services.sharpening import apply_sharpening


def enhance_pipeline(image: np.ndarray) -> np.ndarray:
    """
    Full classical enhancement pipeline for underwater images.
    
    Order matters:
    1. White Balance first — fix color cast before contrast work
    2. CLAHE second     — enhance contrast on color-corrected image
    3. Sharpening last  — sharpen after contrast is set
    """
    # Step 1: Fix blue-green color cast
    image = apply_white_balance(image)

    # Step 2: Boost contrast locally using CLAHE
    image = apply_clahe(image, clip_limit=2.0, tile_size=8)

    # Step 3: Sharpen to recover detail lost from scattering
    image = apply_sharpening(image, strength=0.5)

    return image