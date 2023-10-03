from fastapi import HTTPException
from sqlalchemy import func

from sqlalchemy.orm import Session, aliased
from datetime import date, datetime, timedelta
from collections import defaultdict
from models import Category, Inventory, InventoryChangeLog, Sale, Product
from utils.validations import get_interval_duration_and_format


def get_product_by_name(db: Session, product_name: str):
    product = db.query(Product).filter(Product.name == product_name).first()
    if product is None:
        raise HTTPException(
            status_code=404, detail="Product not found with the provided name"
        )
    return product


def get_category_id_by_name(db: Session, category_name: str):
    category = db.query(Category).filter(Category.name == category_name).first()
    if category is None:
        raise HTTPException(
            status_code=404, detail="Category not found with the provided name"
        )
    return category.id


def get_sales_data(
    db: Session,
    start_date: str,
    end_date: str,
    product_name: str,
    category_name: str = None,
):
    sales = aliased(Sale)
    products = aliased(Product)

    query = db.query(sales, products.name.label("product_name")).join(
        products, sales.product_id == products.id
    )

    if start_date and end_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)

        query = query.filter(
            func.DATE(sales.sale_timestamp) >= start_date,
            func.DATE(sales.sale_timestamp) < end_date,
        )

    if product_name is not None:
        product = get_product_by_name(db, product_name)
        query = query.filter(sales.product_id == product.id)

    if category_name is not None:
        category_id = get_category_id_by_name(db, category_name)
        query = query.filter(products.category_id == category_id)

    sales_data = query.all()

    result = []
    for sale, product_name in sales_data:
        result.append(
            {
                "sale_date": sale.sale_timestamp.strftime("%m/%d/%Y, %H:%M:%S"),
                "product_name": product_name,
                "quantity_sold": sale.quantity_sold,
            }
        )

    return result


def calculate_revenue_by_interval(
    db: Session,
    start_date: str = "2020-01-01",
    end_date: str = date.today(),
    interval: str = "annual",
    category_name: str = None,
):
    start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
    end_datetime = datetime.strptime(end_date, "%Y-%m-%d")

    interval_duration, interval_format = get_interval_duration_and_format(interval)

    if not (interval_duration or interval_format):
        raise HTTPException(
            status_code=400,
            detail="Invalid basis. Allowed values: daily, weekly, monthly, annual",
        )

    revenue_per_interval = defaultdict(float)
    total_revenue = 0.0

    if start_date and end_date:
        current_datetime = start_datetime
        while current_datetime <= end_datetime:
            next_datetime = current_datetime + interval_duration
            if next_datetime.year % 4 == 0:
                next_datetime += timedelta(days=1)
            if next_datetime > end_datetime:
                break

            query = db.query(Sale).filter(
                func.DATE(Sale.sale_timestamp) >= current_datetime,
                func.DATE(Sale.sale_timestamp) < next_datetime,
            )

            if category_name is not None:
                category_id = get_category_id_by_name(db, category_name)
                query = query.join(Sale.product).filter(
                    Product.category_id == category_id
                )

            sales = query.all()
            interval_revenue = sum(
                sale.quantity_sold * sale.product.price for sale in sales
            )

            interval_label = (
                current_datetime.strftime(interval_format)
                + " - "
                + next_datetime.strftime(interval_format)
            )

            revenue_per_interval[interval_label] += interval_revenue

            total_revenue += interval_revenue

            current_datetime = next_datetime

    if start_datetime and end_datetime:
        duration_days = (end_datetime - start_datetime).days + 1
        average_revenue = total_revenue / duration_days
    else:
        average_revenue = 0.0

    return {
        "revenue_per_interval": dict(revenue_per_interval),
        "average_revenue": average_revenue,
    }


def get_inventory_status(db: Session, low_stock_threshold: int = 10):
    products = db.query(Product).all()

    inventory_status = []
    for product in products:
        current_stock = product.inventory[0].current_stock if product.inventory else 0
        is_low_stock = current_stock < low_stock_threshold
        inventory_status.append(
            {
                "product_id": product.id,
                "product_name": product.name,
                "current_stock": current_stock,
                "is_low_stock": is_low_stock,
            }
        )

    return inventory_status


def update_inventory(db: Session, product_name: str, quantity_to_add: int):
    product = get_product_by_name(db, product_name)

    current_quantity = product.inventory[0].current_stock
    new_quantity = current_quantity + quantity_to_add

    product.inventory[0].current_stock = new_quantity

    change_log = InventoryChangeLog(
        product_id=product.id,
        quantity_change=quantity_to_add,
        new_quantity=new_quantity,
    )

    db.add(product)
    db.add(change_log)

    db.commit()
    db.refresh(product)

    return {"product_name": product.name, "updated_quantity": new_quantity}


def get_inventory_changes_by_time_range(
    db: Session,
    start_date: str,
    end_date: str,
    product_name: str = None,
):
    query = db.query(InventoryChangeLog, Product.name.label("product_name")).join(
        Product, InventoryChangeLog.product_id == Product.id
    )

    if start_date and end_date:
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")

        query = query.filter(
            InventoryChangeLog.timestamp >= start_date_obj,
            InventoryChangeLog.timestamp <= end_date_obj,
        )

    if product_name is not None:
        query = query.filter(Product.name == product_name)

    query = query.order_by(InventoryChangeLog.timestamp)

    change_log = query.all()

    result = [
        {
            "timestamp": change.timestamp.strftime("%m/%d/%Y, %H:%M:%S"),
            "product_name": product_name,
            "quantity_change": change.quantity_change,
            "new_quantity": change.new_quantity,
        }
        for change, product_name in change_log
    ]

    return result


def create_product(
    db: Session,
    name: str,
    description: str,
    price: float,
    category_name: str,
    initial_stock: int,
    low_stock_alert_threshold: int,
):
    category_id = get_category_id_by_name(db, category_name)

    product = Product(
        name=name, description=description, price=price, category_id=category_id
    )

    inventory = Inventory(
        product=product,
        current_stock=initial_stock,
        low_stock_alert_threshold=low_stock_alert_threshold,
    )

    db.add(product)
    db.add(inventory)
    db.commit()
    db.refresh(product)

    return product
