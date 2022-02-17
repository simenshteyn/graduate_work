from uuid import UUID

from pydantic import BaseModel, condecimal


class CreatePaymentByCryptogram(BaseModel):
    """ Model for creating payment by card cryptogram (first time pay)."""
    payment_id: UUID
    account_id: UUID
    amount: condecimal(decimal_places=2)
    ip_address: str
    card_cryptogram: str


class CreatePaymentByToken(BaseModel):
    """ Mode for creating payment with payment token (recurring payments)."""
    payment_id: UUID
    account_id: UUID
    amount: condecimal(decimal_places=2)
    recurring_token: str


class CreatePaymentByBillUUID(BaseModel):
    """ Model for creating payment with bill UUID (UUIDs are the same)."""
    bill_id: UUID
