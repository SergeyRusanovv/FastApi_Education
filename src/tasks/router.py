from fastapi import APIRouter, Depends
from auth.base_config import current_user
from tasks.tasks import send_email_report_dashboard

router = APIRouter(prefix="/report")


@router.get("/dashboard")
async def get_dashboard(user=Depends(current_user)):
    send_email_report_dashboard.delay(user.username)
    return {"status": 200, "data": "Письмо отправлено", "detail": None}
