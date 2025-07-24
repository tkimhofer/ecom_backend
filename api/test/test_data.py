import commentjson, datetime
from api.models import Order, OrderLine, RawOrder
from api.db import SessionLocal
import os
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent
data_path_str = os.path.join(BASE_PATH, "shopify_order_examples.json")

db = SessionLocal()

def place_dummy_into_raw():
    db = SessionLocal()

    with open(data_path_str, "r") as f:
        data = commentjson.load(f)

    try:
        for order in data["orders"]:
            raw = RawOrder(
                payload=order,
                source_system="shop_frontend",
                ingested_at=datetime.datetime.utcnow()
            )
            db.add(raw)
        db.commit()
    finally:
        db.close()
