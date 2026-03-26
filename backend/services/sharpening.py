import cv2
import numpy as np

def apply_sharpening(image : np.ndarray,strength:float = 1.0) -> np.ndarray:
     """
    Sharpen the image to recover detail lost due to light scattering underwater.
    
    Uses Unsharp Masking technique:
    1. Create a blurred version of the image (the 'mask')
    2. Subtract blur from original to get edges/details
    3. Add those details back to the original with a strength factor
    
    Formula: sharpened = original + strength * (original - blurred)
    """
     blurred = cv2.GaussianBlur(image,(0,0),sigmaX=3)

     sharpened = cv2.addWeighted(
          image,1+strength,
          blurred,-strength,0
     )

     return np.clip(sharpened,0,255).astype(np.uint8)

def apply_laplacian_sharpen(image:np.ndarray) -> np.ndarray:
     """
    Alternative: Laplacian-based sharpening using a convolution kernel.
    
    This kernel detects edges by computing the second derivative.
    Adding it back to the original sharpens edges.
    
    Kernel:
    [ 0, -1,  0]
    [-1,  5, -1]
    [ 0, -1,  0]
    """
     kernel = np.array([
          [0,-1,0],
          [-1,5,-1],
          [0,-1,0]
     ],dtype=np.float32)

     sharpened = cv2.filter2D(image,-1,kernel)
     return np.clip(sharpened, 0, 255).astype(np.uint8)