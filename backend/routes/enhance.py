from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from io import BytesIO
from utils.image_utils import decode_image, encode_image_to_bytes
from services.pipeline import enhance_pipeline

router = APIRouter()


@router.post("/enhance")
async def enhance_image(file: UploadFile = File(...)):
    """
    Upload an underwater image and receive an enhanced version.
    
    - Accepts: JPEG, PNG image files
    - Returns: Enhanced image as JPEG
    """
    # Validate file type
    if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload a JPEG or PNG image."
        )

    # Read the uploaded file bytes
    file_bytes = await file.read()

    # Decode bytes → OpenCV image (numpy array)
    try:
        image = decode_image(file_bytes)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Run the enhancement pipeline
    enhanced_image = enhance_pipeline(image)

    # Encode enhanced image back to bytes
    result_bytes = encode_image_to_bytes(enhanced_image, format="JPEG")

    # Return as streaming image response
    return StreamingResponse(
        BytesIO(result_bytes),
        media_type="image/jpeg",
        headers={"Content-Disposition": "inline; filename=enhanced.jpg"}
    )


@router.get("/enhance/info")
def enhancement_info():
    """Returns info about the enhancement pipeline being used."""
    return {
        "pipeline": "Classical Image Processing",
        "steps": [
            {
                "step": 1,
                "name": "White Balance",
                "description": "Corrects blue-green color cast by boosting the red channel"
            },
            {
                "step": 2,
                "name": "CLAHE",
                "description": "Adaptive contrast enhancement applied to the lightness channel"
            },
            {
                "step": 3,
                "name": "Unsharp Masking",
                "description": "Sharpens edges to recover detail lost due to light scattering"
            }
        ],
        "phase": "Phase 1 - Classical Processing"
    }