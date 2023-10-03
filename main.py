from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date
from crud import (
    calculate_revenue_by_interval,
    create_product,
    get_inventory_changes_by_time_range,
    get_inventory_status,
    get_sales_data,
    update_inventory,
)

from database import Base, SessionLocal, engine
from schemas import (
    InventoryChangeLogResponse,
    InventoryStatusResponse,
    InventoryUpdateResponse,
    ProductCreateRequest,
    ProductCreateResponse,
    RevenueResponse,
    SalesDataResponse,
)
from utils.validations import valid_start_end_dates


app = FastAPI()
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/sales/", response_model=SalesDataResponse)
def get_sales(
    start_date: Annotated[str, Query(description="Start date (YYYY-MM-DD)")] = None,
    end_date: Annotated[str, Query(description="End date (YYYY-MM-DD)")] = None,
    product_name: Annotated[str, Query(description="Product name")] = None,
    category_name: Annotated[str, Query(description="Category name")] = None,
    db: Session = Depends(get_db),
):
    if not valid_start_end_dates(start_date, end_date):
        raise HTTPException(
            status_code=400, detail="Invalid start_date or end_date (YYYY-MM-DD)"
        )

    sales_data = get_sales_data(db, start_date, end_date, product_name, category_name)

    if not sales_data:
        raise HTTPException(
            status_code=404, detail="No sales data found for the specified criteria"
        )

    return {"sales_data": sales_data}


@app.get("/revenue/", response_model=RevenueResponse)
def analyze_revenue(
    start_date: Annotated[
        str, Query(description="Start date (YYYY-MM-DD)")
    ] = "2020-01-01",
    end_date: Annotated[str, Query(description="End date (YYYY-MM-DD)")] = date.today(),
    interval: Annotated[
        str, Query(description="Filter on basis (daily, weekly, monthly, annual)")
    ] = "annual",
    category_name: Annotated[str, Query(description="Category name")] = None,
    db: Session = Depends(get_db),
):
    if not valid_start_end_dates(start_date, end_date):
        raise HTTPException(
            status_code=400, detail="Invalid start_date or end_date (YYYY-MM-DD)"
        )

    revenue_data = calculate_revenue_by_interval(
        db, start_date, end_date, interval, category_name
    )

    return {"revenue_data": revenue_data}


@app.get("/inventory/", response_model=InventoryStatusResponse)
def view_inventory_status(
    low_stock_threshold: Annotated[int, Query(description="Low stock threshold")] = 10,
    db: Session = Depends(get_db),
):
    inventory_status = get_inventory_status(db, low_stock_threshold)
    return {"inventory": inventory_status}


@app.post("/inventory/update/", response_model=InventoryUpdateResponse)
def update_inventory_level(
    product_name: Annotated[str, Query(description="Product name")] = None,
    quantity_to_add: Annotated[int, Query(description="Quantity to add")] = 0,
    db: Session = Depends(get_db),
):
    product = update_inventory(db, product_name, quantity_to_add)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


@app.get("/inventory/changes/", response_model=InventoryChangeLogResponse)
def get_inventory_changes_in_time_range(
    start_date: Annotated[
        str, Query(description="Start date time (YYYY-MM-DD )")
    ] = None,
    end_date: Annotated[str, Query(description="End date time (YYYY-MM-DD)")] = None,
    product_name: Annotated[str, Query(description="Product name")] = None,
    db: Session = Depends(get_db),
):
    if not valid_start_end_dates(start_date, end_date):
        raise HTTPException(
            status_code=400,
            detail="Invalid date/time format. Please use the format YYYY-MM-DD",
        )

    changes = get_inventory_changes_by_time_range(
        db, start_date, end_date, product_name
    )

    if not changes:
        raise HTTPException(
            status_code=404,
            detail="No inventory changes found for the specified criteria",
        )

    return {"inventory_changes": changes}


@app.post("/products/", response_model=ProductCreateResponse)
def register_product(
    request_data: ProductCreateRequest,
    db: Session = Depends(get_db),
):
    name = request_data.name
    description = request_data.description
    price = request_data.price
    category_name = request_data.category_name
    initial_stock = request_data.initial_stock
    low_stock_alert_threshold = request_data.low_stock_alert_threshold

    product = create_product(
        db,
        name,
        description,
        price,
        category_name,
        initial_stock,
        low_stock_alert_threshold,
    )

    if not product:
        raise HTTPException(status_code=500, detail="Failed to create the product")

    return product
