from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from random import randint
from models import Category, Product, Sale, Inventory, InventoryChangeLog
from database import SessionLocal

# Replace 'your_database_url' with the actual database URL
DATABASE_URL = "sqlite:///_ecommerce.db"


# Initialize the database session
db = SessionLocal()


categories_data = [
    {"name": "Personal Care"},
    {"name": "Beverages"},
    {"name": "Dairy"},
    {"name": "Bakery"},
    # Add more category data if needed
]

# Sample data for products
products_data = [
    {
        "name": "Soap",
        "description": "This is a premium soap",
        "price": 19.99,
        "category_id": 1,
    },
    {
        "name": "Bottle",
        "description": "This is a carbonated soft drink",
        "price": 29.99,
        "category_id": 2,
    },
    {
        "name": "Conditioner",
        "description": "This is a high quality conditioner",
        "price": 39.99,
        "category_id": 1,
    },
    {
        "name": "Milk",
        "description": "This is a healthy milk",
        "price": 25.00,
        "category_id": 3,
    },
    {
        "name": "Bread",
        "description": "This is a whole wheat bread",
        "price": 15.00,
        "category_id": 4,
    },
    {
        "name": "Yogurt",
        "description": "This is a low fat yogurt",
        "price": 20.00,
        "category_id": 3,
    },
    # Add more product data if needed
]

db.bulk_save_objects([Category(**data) for data in categories_data])
db.commit()

# Add products to the database
db.bulk_save_objects([Product(**data) for data in products_data])
db.commit()

# Sample data for sales
sales_data = []

# Generate random sales data for a period of time
start_date = datetime(2021, 8, 1)
end_date = datetime(2022, 11, 30)

while start_date <= end_date:
    for product in db.query(Product).all():
        quantity_sold = randint(1, 10)

        # Generate random hours and minutes
        hours = randint(0, 23)
        minutes = randint(0, 59)

        # Combine date, hours, and minutes
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

# Sample data for inventory
inventory_data = []

# Initialize inventory data for each product
for product in db.query(Product).all():
    initial_stock = randint(20, 100)
    low_stock_alert_threshold = 10
    inventory = Inventory(
        product_id=product.id,
        current_stock=initial_stock,
        low_stock_alert_threshold=low_stock_alert_threshold,
    )
    inventory_data.append(inventory)

# Sample data for inventory change logs
inventory_change_logs_data = []

start_date = datetime(2021, 8, 1)

# Generate inventory change logs
for product in db.query(Product).all():
    for _ in range(5):  # Generate 5 random change logs per product
        quantity_change = randint(0, 50)  # Random quantity change
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


# Function to populate the database with sample data
def populate_database():
    try:
        # Add sales to the database
        db.bulk_save_objects(sales_data)

        # Add inventory to the database
        db.bulk_save_objects(inventory_data)

        # Add inventory change logs to the database
        db.bulk_save_objects(inventory_change_logs_data)

        # Commit the changes
        db.commit()
        print("Sample data has been inserted into the database.")
    except Exception as e:
        db.rollback()
        print("Error:", str(e))
    finally:
        db.close()


if __name__ == "__main__":
    populate_database()
