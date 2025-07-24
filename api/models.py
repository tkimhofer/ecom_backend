from api.db import Base
import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

class RawOrder(Base):
    __tablename__ = "raw_orders"

    uid = Column(Integer, primary_key=True, index=True)
    payload = Column(JSONB)  # original JSON as-is
    source_system = Column(String, default="shop_frontend")
    ingested_at = Column(DateTime, default=datetime.datetime.utcnow)

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer)
    current_lineitems_quantity = Column(Integer)
    current_total_price = Column(Float)
    current_total_tax = Column(Float)
    current_total_weight = Column(Float)
    fulfillment_status = Column(String, default="ordered")
    payment_status = Column(String, default="paid")
    refund_status = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    cancelled_at = Column(DateTime, default=None)
    closed_at = Column(DateTime, default=None)
    gclid = Column(String, nullable=True)
    landing_page_url = Column(String, nullable=True)
    line_items = relationship("OrderLine", backref="order")


class OrderLine(Base):
    __tablename__ = "order_lines"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    sku = Column(String)
    product = Column(String)
    variant = Column(String)
    line_item_group = Column(String)  # this defines a bundle
    contract_id = Column(String)      # non-empty in case of recurrent/subscription order
    current_price = Column(Float)
    current_tax = Column(Float)
    current_tax_perc = Column(String)
    quantity = Column(Integer)
    fulfillment_status = Column(DateTime, default=datetime.datetime.utcnow)
    remaining_quantity = Column(Integer)
