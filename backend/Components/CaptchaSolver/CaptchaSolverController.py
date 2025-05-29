from fastapi import APIRouter, UploadFile, File, HTTPException
from CaptchaSolverHelper import solve_captcha_image, solve_captcha_bytes
import tempfile

router = APIRouter()

@router.post("/captcha/solve-file")
async def solve_from_file(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        result = solve_captcha_image(tmp_path)
        return {"solved_text": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/captcha/solve-bytes")
async def solve_from_bytes(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        result = solve_captcha_bytes(image_bytes)
        return {"solved_text": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))