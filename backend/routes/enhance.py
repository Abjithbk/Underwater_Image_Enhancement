from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import io
import base64
from PIL import Image

from services.model_runner import ModelRunner
from services.matrics import compute_metrics

router = APIRouter()

#Load training weights
model_runner = ModelRunner(
    model_path="weights/underwater_best.pth"
)

@router.post("/enhance")
async def enhance_image(file: UploadFile = File(...)):

    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="File must be an image"
        )

    try:
        contents = await file.read()
        print("Step 1: file read ok")

        original = Image.open(
            io.BytesIO(contents)
        ).convert("RGB")
        print(f"Step 2: image opened — {original.size}")

        # Pass directly to model
        # model_runner handles resize internally
        enhanced = model_runner.enhance(original)
        print("Step 3: model ran ok")

        # Resize back to original size
        enhanced = enhanced.resize(
            original.size, Image.LANCZOS
        )
        print("Step 4: resize ok")

        # Compute metrics
        psnr_val, ssim_val = compute_metrics(
            original, enhanced
        )
        print(f"Step 5: metrics — psnr:{psnr_val:.2f} ssim:{ssim_val:.4f}")

        # Encode to base64
        buffer = io.BytesIO()
        enhanced.save(buffer, format="PNG")
        encoded = base64.b64encode(
            buffer.getvalue()
        ).decode("utf-8")
        print("Step 6: encoding ok")

        return JSONResponse({
            "enhanced_image": f"data:image/png;base64,{encoded}",
            "psnr": round(psnr_val, 2),
            "ssim": round(ssim_val, 4)
        })

    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
def health():
    return {"status": "ok"}