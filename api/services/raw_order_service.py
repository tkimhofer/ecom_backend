from api.models import RawOrder
from api.v1.schemas import RawOrderOut
from api.db import Session
from typing import Optional


class RawOrderService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, payload: dict) -> RawOrderOut:
        """
            Create a new raw order entry in the database.

            This method takes a raw payload dictionary (e.g., mimicking the structure
            sent from the frontend or an external API), stores it in the `raw_orders` table,
            and returns a Data Transfer Object (DTO) suitable for exposure via the API layer.

            Args:
                payload (dict): The raw JSON payload containing order data.

            Returns:
                RawOrderOut: A Pydantic DTO representing the created raw order, with only
                relevant fields exposed.

            Example:
                payload = {
                    "orders": [...],
                    "shop_id": 123,
                    "received_at": "2025-07-22T15:30:00Z"
                }

                service = RawOrderService(db)
                raw_order_dto = service.create(payload)
        """
        raw_order = RawOrder(payload=payload)
        self.db.add(raw_order)
        self.db.commit()
        self.db.refresh(raw_order)

        return RawOrderOut.from_orm()

    def get_by_uid(self, uid: int) -> Optional[RawOrderOut]:
        raw_order = self.db.query(RawOrder).filter(RawOrder.uid == uid).first()
        if not raw_order:
            return None
        return RawOrderOut.from_orm(raw_order)
