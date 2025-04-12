from datetime import datetime

from pydantic import BaseModel


class PlanLabourRequest(BaseModel):
    first_labour: bool
    due_date: datetime
    labour_name: str | None = None


class PaymentPlanLabourRequest(BaseModel):
    payment_plan: str


class CompleteLabourRequest(BaseModel):
    end_time: datetime | None = None
    notes: str | None = None


class SendInviteRequest(BaseModel):
    invite_email: str
    labour_id: str
