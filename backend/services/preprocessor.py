from PIL import Image

MODEL_INPUT_SIZE = (256,256)

def preprocess_image(image : Image.Image) -> Image.Image:

    """
    prepare image for U - NET  Architecture
    Not in rgba its in RGB
    """
    if image.mode != "RGB":
        image = image.convert("RGB")

    resized = image.resize(MODEL_INPUT_SIZE,Image.LANCZOS)

    return resized


