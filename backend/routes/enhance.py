from fastapi import APIRouter , UploadFile,File,HTTPException
from fastapi.responses import JSONResponse
import io,base64
from PIL import Image
from services.preprocessor import preprocess_image
from services.model_runner import ModelRunner
from services.matrics import compute_metrics

router = APIRouter()

model_runner = ModelRunner()

@router.post("/enhance")
async def enhance_image(file:UploadFile = File(...)):

    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="File must be an image in JPG,PNG,WEBP,etc..."
        )
    
    try:
         # Step 1 — read raw bytes from uploaded file
        contents = await file.read()
          # Step 2 — bytes → PIL Image
        # io.BytesIO wraps bytes as a file-like object
        # so PIL can open it without saving to disk

        original = Image.open(io.BytesIO(contents)).convert("RGB")
        # Step 3 — resize to 256x256 for model input

        preprocessed = preprocess_image(original)
        # Step 4 — run through U-Net

        enhanced = model_runner.enhance(preprocessed)

         # Step 5 — resize enhanced image back to original size

        enhanced = enhanced.resize(original.size,Image.LANCZOS)

         # Step 6 — compute quality scores

        psnr_val,ssim_val = compute_metrics(original,enhanced)

        # Step 7 — convert enhanced PIL image → base64 string
        # base64 = text-safe encoding that can travel inside JSON

        buffer = io.BytesIO()
        enhanced.save(buffer,format="PNG")
        encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")

        return JSONResponse({
            "enhanced_image" : f"data:image/png;base64,{encoded}",
            "psnr":round(psnr_val,2),
            "ssim":round(ssim_val,4)
        })
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    

