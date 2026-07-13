# Image Enhancement

An underwater image enhancement project with a FastAPI backend and a SvelteKit frontend. The app lets you upload an image, runs it through a trained U-Net model, and returns an enhanced version along with basic quality metrics.

## What it does

- Upload an image from the web UI
- Send the image to the backend for AI-based enhancement
- Return the enhanced image as a PNG data URL
- Display PSNR and SSIM metrics for the result

## Project Structure

- `backend/` contains the FastAPI app, model loading, preprocessing, and metric calculation
- `frontend/` contains the SvelteKit UI for uploading and previewing images
- `notebook/` contains the training and experimentation notebook used for the project
- `backend/weights/underwater_best.pth` stores the trained model weights used by the API

## Tech Stack

- FastAPI
- PyTorch
- Pillow
- SvelteKit
- TypeScript

## API Endpoints

- `GET /` returns a simple backend status message
- `GET /api/health` returns API health information
- `POST /api/enhance` accepts an image file and returns the enhanced image plus PSNR and SSIM values

## Running Locally

### Backend

1. Create and activate a Python environment.
2. Install dependencies from `backend/requirements.txt`.
3. Start the API server from the `backend/` folder.

Example:

```bash
pip install -r backend/requirements.txt
uvicorn main:app --reload
```

The backend runs on `http://127.0.0.1:8000` by default.

### Frontend

1. Install dependencies in the `frontend/` folder.
2. Start the SvelteKit dev server.

Example:

```bash
cd frontend
npm install
npm run dev
```

The frontend expects the backend at `http://127.0.0.1:8000` unless `VITE_API_URL` is set.

## Notes

- The backend enables CORS for the common local development ports used by SvelteKit.
- The enhancement route currently focuses on underwater images, but the upload endpoint accepts any valid image file.
- The result preview and metrics are handled in the frontend after the backend response is received.