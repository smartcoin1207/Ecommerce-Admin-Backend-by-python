from typing import Dict, List
from pydantic import BaseModel


class SalesDataBase(BaseModel):
    sale_date: str
    product_name: str
    quantity_sold: int


class SalesDataResponse(BaseModel):
    sales_data: List[SalesDataBase]


class RevenueBase(BaseModel):
    revenue_per_interval: Dict[str, float]
    average_revenue: float


class RevenueResponse(BaseModel):
    revenue_data: RevenueBase


class InventoryStatusBase(BaseModel):
    product_id: int
    product_name: str
    current_stock: int
    is_low_stock: bool


class InventoryStatusResponse(BaseModel):
    inventory: List[InventoryStatusBase]


class InventoryUpdateResponse(BaseModel):
    product_name: str
    updated_quantity: int


class InventoryChangeLogBase(BaseModel):
    product_name: str
    timestamp: str | None
    new_quantity: int
    quantity_change: int


class InventoryChangeLogResponse(BaseModel):
    inventory_changes: List[InventoryChangeLogBase]


class ProductCreateRequest(BaseModel):
    name: str
    description: str
    price: float
    category_name: str
    initial_stock: int
    low_stock_alert_threshold: int


class ProductCreateResponse(BaseModel):
    name: str
    description: str
    price: float
    category_id: int
