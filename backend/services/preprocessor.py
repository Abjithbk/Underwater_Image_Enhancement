from PIL import Image

# Same size as training
MODEL_INPUT_SIZE = (256, 256)

def preprocess_image(image: Image.Image) -> Image.Image:
    """
    Prepares image for UnderwaterNet.
    NO normalization — matches training exactly!
    """
    if image.mode != "RGB":
        image = image.convert("RGB")

    # Resize to model input size
    resized = image.resize(MODEL_INPUT_SIZE, Image.LANCZOS)

    return resized