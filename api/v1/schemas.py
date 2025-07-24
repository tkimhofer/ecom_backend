from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Any
from datetime import datetime

class RawOrderOut(BaseModel):
    """
        Data Transfer Object (DTO) for exposing raw order data.

        This Pydantic model is used to serialize and validate raw order entries
        returned from the database before they are sent to the API consumer.
        It ensures only relevant and safe fields are exposed.

        Attributes:
            uid (int): Unique identifier for the raw order record.
            payload (Any): The original JSON payload received from the source system.
                Use `dict` instead of `Any` if strict typing is preferred.
            source_system (str): Identifier for the origin of the data, e.g., 'shop_frontend'.
            ingested_at (datetime): Timestamp indicating when the payload was stored in the raw layer.

        ConfigDict:
            from_attributes = True - Enables ORM-to-Pydantic conversion using `from_orm()`.
    """

    uid: int
    payload: Optional[Any]  # included only on request (e.g., for debugging)
    source_system: str
    ingested_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OrderLineCreate(BaseModel):
    id: int
    sku: str
    product: str
    variant: str
    line_item_group: Optional[str] = None
    contract_id: Optional[str] = ""
    current_price: float
    current_tax: float
    current_tax_rate: str
    quantity: int
    fulfillment_status: Optional[datetime] = None
    remaining_quantity: Optional[int] = None


class OrderCreate(BaseModel):
    id: int
    customer_id: int
    current_line_items_quantity: int
    current_total_price: float
    current_total_tax: float
    current_total_weight: float
    fulfillment_status: str
    payment_status: str
    refund_status: Optional[str] = None
    created_at: Optional[datetime] = None
    cancelled_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    gclid: Optional[str] = None
    landing_page_url: Optional[str] = None
    line_items: List[OrderLineCreate]


class OrderLineOut(BaseModel):
    id: int
    order_id: int
    sku: str
    product: str
    variant: str
    line_item_group: Optional[str]
    contract_id: Optional[str]
    current_price: float
    current_tax: float
    current_tax_rate: str
    quantity: int
    fulfillment_status: Optional[datetime]
    remaining_quantity: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class OrderOut(BaseModel):
    id: int
    customer_id: int
    current_line_items_quantity: int
    current_total_price: float
    current_total_tax: float
    current_total_weight: float
    fulfillment_status: str
    payment_status: str
    refund_status: Optional[str]
    created_at: datetime
    cancelled_at: Optional[datetime]
    closed_at: Optional[datetime]
    gclid: Optional[str]
    landing_page_url: Optional[str]
    line_items: List[OrderLineOut]

    model_config = ConfigDict(from_attributes=True)