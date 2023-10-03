from datetime import datetime, timedelta
from random import randint
from models.models import Category, Product, Sale, Inventory, InventoryChangeLog
from db.database import SessionLocal

DATABASE_URL = "sqlite:///_ecommerce.db"

db = SessionLocal()


categories_data = [
    {"name": "electronics"},
    {"name": "furniture"},
    {"name": "cars"},
    {"name": "kitchen"},
    # Add more category data if needed
]

# Sample data for products
products_data = [
    {
        "name": "Iphone",
        "description": "A premium quality mobile phone",
        "price": 200000.99,
        "category_id": 1,
    },
    {
        "name": "Bed",
        "description": "Gives uninterrupted sleep",
        "price": 15000.00,
        "category_id": 2,
    },
    {
        "name": "Refrigerator",
        "description": "A high quality cooling machine",
        "price": 20999.99,
        "category_id": 1,
    },
    {
        "name": "Audi A6",
        "description": "A world class car",
        "price": 250000.00,
        "category_id": 3,
    },
    {
        "name": "Sofa Set",
        "description": "A world class sofa set",
        "price": 10000.00,
        "category_id": 2,
    },
    {
        "name": "Oven",
        "description": "A high quality oven",
        "price": 22222.00,
        "category_id": 4,
    },
    # Add more product data if needed
]

db.bulk_save_objects([Category(**data) for data in categories_data])
db.commit()

db.bulk_save_objects([Product(**data) for data in products_data])
db.commit()

sales_data = []

start_date = datetime(2021, 8, 1)
end_date = datetime(2022, 11, 30)

while start_date <= end_date:
    for product in db.query(Product).all():
        quantity_sold = randint(1, 10)

        hours = randint(0, 23)
        minutes = randint(0, 59)

        sale_timestamp = datetime(
            start_date.year, start_date.month, start_date.day, hours, minutes
        )

        sale = Sale(
            product_id=product.id,
            sale_timestamp=sale_timestamp,
            quantity_sold=quantity_sold,
        )
        sales_data.append(sale)
    start_date += timedelta(days=1)

inventory_data = []

for product in db.query(Product).all():
    initial_stock = randint(20, 100)
    low_stock_alert_threshold = 10
    inventory = Inventory(
        product_id=product.id,
        current_stock=initial_stock,
        low_stock_alert_threshold=low_stock_alert_threshold,
    )
    inventory_data.append(inventory)


inventory_change_logs_data = []
start_date = datetime(2021, 8, 1)

for product in db.query(Product).all():
    for _ in range(5):
        quantity_change = randint(0, 50)
        new_quantity = (
            product.inventory[0].current_stock + quantity_change
            if product.inventory
            else quantity_change
        )
        timestamp = datetime(2022, randint(1, 12), randint(1, 30), hours, minutes)

        change_log = InventoryChangeLog(
            product_id=product.id,
            quantity_change=quantity_change,
            new_quantity=new_quantity,
            timestamp=timestamp,
        )
        inventory_change_logs_data.append(change_log)


def populate_database():
    try:
        db.bulk_save_objects(sales_data)

        db.bulk_save_objects(inventory_data)

        db.bulk_save_objects(inventory_change_logs_data)

        db.commit()
        print("Sample data has been inserted into the database.")
    except Exception as e:
        db.rollback()
        print("Error:", str(e))
    finally:
        db.close()


if __name__ == "__main__":
    populate_database()
