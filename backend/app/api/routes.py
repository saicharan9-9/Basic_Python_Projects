from fastapi import APIRouter

router = APIRouter(prefix="/api")


@router.get("/ping")
async def ping():
	return {"message": "pong"}