import numpy as np
from PIL import Image
from skimage.metrics import peak_signal_noise_ratio, structural_similarity

def compute_metrics(original:Image.Image,enhanced:Image.Image) -> tuple[float,float]:
    """
    Returns (psnr, ssim) between original and enhanced image.

    PSNR: measures pixel difference — higher is better
          >30dB good, >40dB excellent

    SSIM: measures structure preservation — range 0 to 1
          >0.7 good, >0.9 excellent
    """

    #Make sure both images are same

    if original.size != enhanced.size:
        enhanced = enhanced.resize(original.size,Image.LANCZOS)

    orig_arr = np.array(original.convert("RGB"))
    enh_arr = np.array(enhanced.convert("RGB"))

    # data_range=255 because pixels go from 0 to 255
    psnr_val = peak_signal_noise_ratio(
        orig_arr, enh_arr, data_range=255
    )

    # channel_axis=2 tells skimage axis 2 is the RGB channel axis
    ssim_val = structural_similarity(
        orig_arr, enh_arr,
        data_range=255,
        channel_axis=2
    )

    return psnr_val,ssim_val